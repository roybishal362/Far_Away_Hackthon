"""Kakehashi API (FastAPI).

Endpoints:
  GET  /health        liveness + which real tools are configured
  POST /run           full run (blocking) -> structured result
  POST /run/stream    Server-Sent Events: streams the live agent timeline, then the result
  POST /eval          grounded-vs-ungrounded ablation (the proof)

Run locally:  uvicorn api.main:app --reload --port 8000
"""
from __future__ import annotations

import json
import queue
import threading
from io import BytesIO

from fastapi import Body, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel

from config import SETTINGS
from core import chat as chat_mod
from core import resume as resume_mod
from core import store
from core.agents._common import profile_text
from core.dossier import build as build_dossier
from core.engine import Engine, RunResult
from core.eval.harness import run_ablation
from core.types import Citation, WorkerProfile

app = FastAPI(title="Kakehashi API", version="0.1.0")

# Dev-open CORS so the Next.js dev server can call us. Restrict in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProfileIn(BaseModel):
    skills: str = ""
    sector_interest: str = ""
    years_experience: float = 0.0
    japanese_level: str = "none"
    education: str = ""
    origin_city: str = "Delhi"
    target_city: str = "Tokyo"
    lang: str = "en"


def _profile(p: ProfileIn) -> WorkerProfile:
    return WorkerProfile(**p.model_dump())


def _cite(c: Citation) -> dict:
    return {"url": c.source_url, "title": c.title, "snippet": c.snippet}


def _result_dict(r: RunResult) -> dict:
    return {
        "grounding_score": r.grounding_score(),
        "metrics": r.metrics,
        "results": {
            name: {
                "agent": ar.agent,
                "ok": ar.ok,
                "error": ar.error,
                "summary": ar.summary,
                "data": ar.data,
                "confidence": ar.confidence,
                "grounded": ar.grounded(),
                "citations": [_cite(c) for c in ar.citations],
            }
            for name, ar in r.results.items()
        },
    }


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "llm": "groq" if SETTINGS.groq_api_key else "not-configured",
        "tools": {
            "jobs": bool(SETTINGS.jsearch_api_key),
            "estat": bool(SETTINGS.estat_app_id),
            "flights": bool(SETTINGS.amadeus_client_id and SETTINGS.amadeus_client_secret),
        },
    }


@app.post("/run")
def run(p: ProfileIn) -> dict:
    return _result_dict(Engine().run(_profile(p)))


@app.post("/run/stream")
def run_stream(p: ProfileIn) -> StreamingResponse:
    profile = _profile(p)
    q: queue.Queue = queue.Queue()
    DONE = object()

    def on_step(agent: str, step) -> None:
        q.put(("step", {"agent": agent, "label": step.label, "detail": step.detail, "kind": step.kind}))

    def worker() -> None:
        try:
            result = Engine().run(profile, on_step=on_step)
            q.put(("result", _result_dict(result)))
        except Exception as exc:  # surface, don't hang the stream
            q.put(("error", {"message": str(exc)}))
        finally:
            q.put((DONE, None))

    threading.Thread(target=worker, daemon=True).start()

    def gen():
        yield _sse("start", {"agents": ["pathway", "jobs", "procedure", "prep", "journey"]})
        while True:
            kind, data = q.get()
            if kind is DONE:
                break
            yield _sse(kind, data)

    return StreamingResponse(gen(), media_type="text/event-stream")


@app.post("/eval")
def eval_endpoint(p: ProfileIn) -> dict:
    return run_ablation(_profile(p)).to_dict()


class ChatIn(BaseModel):
    question: str
    profile: ProfileIn | None = None
    history: list[dict] = []


@app.post("/chat")
def chat_endpoint(c: ChatIn) -> dict:
    pt = profile_text(_profile(c.profile)) if c.profile else ""
    lang = c.profile.lang if c.profile else "en"
    return chat_mod.answer(c.question, profile_text=pt, history=c.history, lang=lang)


@app.post("/resume")
async def resume_endpoint(file: UploadFile = File(...)) -> dict:
    raw = await file.read()
    name = (file.filename or "").lower()
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(raw))
            text = "\n".join((pg.extract_text() or "") for pg in reader.pages)
        except Exception:
            text = ""
    else:
        text = raw.decode("utf-8", errors="ignore")
    return resume_mod.extract(text)


@app.post("/dossier")
def dossier_endpoint(payload: dict = Body(...)) -> Response:
    pdf = build_dossier(payload.get("plan", {}), payload.get("profile", {}))
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=kakehashi-dossier.pdf"},
    )


@app.post("/save")
def save_endpoint(payload: dict = Body(...)) -> dict:
    return {"id": store.save(payload)}


@app.get("/plan/{pid}")
def plan_endpoint(pid: str) -> dict:
    plan = store.load(pid)
    if not plan:
        raise HTTPException(status_code=404, detail="plan not found")
    return plan
