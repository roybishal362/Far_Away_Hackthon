# 🌉 Kakehashi (架け橋) — an autonomous AI bridge for Indian workers to Japan

> **FAR AWAY 2026 · Theme: Agentic & Autonomous Systems**
> A source-grounded multi-agent system that guides Indian skilled workers through Japan's
> **Specified Skilled Worker (SSW)** journey — *every answer cited from official sources, every claim measured.*

Built on the real **Aug-2025 India–Japan Human Resource Exchange Partnership** (50,000 Indian
workers → Japan) and the **India–Japan AI Cooperation Initiative** ("AI talent mobility",
"trustworthy AI"). It helps **both** governments: India sends workers, Japan fills its labor shortage.

---

## Why it's different
- **Real or nothing.** Every tool returns real data or honestly says "not configured" — it *cannot* fabricate (enforced in the type system). Live jobs come from a real jobs API; SSW rules are grounded in official `ssw.go.jp` / MOFA pages with citations.
- **Proven, not claimed.** A built-in ablation measures our grounded agents vs. a plain LLM:
  **accuracy 14% → 71%, hallucinations 6 → 0** (against a gold set of official facts).
- **Autonomous multi-agent.** 5 specialized agents (Pathway · Jobs · Procedure · Prep · Journey) orchestrated, each reasoning + calling a real tool + citing sources, streamed live to the UI.

## Architecture
```
frontend/         Next.js 14 + TS + Tailwind + Framer Motion (polished product UI)
   └─ talks to ─▶ FastAPI (api/) ── SSE stream of the live agent timeline
api/main.py       /run, /run/stream (SSE), /eval, /health
core/             UI-agnostic brain (swap the UI without touching this)
  engine.py       orchestrates agents, computes the Source-Grounding Score
  agents/         pathway · jobs · procedure · prep · journey
  tools/          real-data clients: jobs (JSearch), estat (gov stats), flights (Amadeus)
  rag/            official SSW facts, BM25-retrieved, every passage cited
  eval/           gold checklist + grounded-vs-ungrounded ablation (the proof)
  security/       AES/Fernet encryption-at-rest
config.py         loads keys from .env / secrets; honest no-key degradation
```
See [ARCHITECTURE.md](ARCHITECTURE.md) for the full design.

## Run it locally

### 1) Backend (Python 3.12+)
> On Windows use **`py`** (the launcher); plain `python` may hit the Microsoft Store alias.
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# create .env (see below), then start the server:
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload --port 8000
```
Check it: open http://localhost:8000/health

### 2) Frontend (Node.js 18+)
```powershell
cd frontend
npm install
copy .env.local.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
```
Open http://localhost:3000

### `.env` (backend, gitignored — never commit)
```
GROQ_API_KEY=...            # console.groq.com (free) — the agents' brain
JSEARCH_API_KEY=...         # OpenWeb Ninja JSearch (free tier) — live jobs
ESTAT_APP_ID=...            # e-stat.go.jp (free) — gov labor statistics
# AMADEUS_CLIENT_ID/SECRET  # flights — Round 2 (paid tier)
```

## Proof / evaluation
`POST /eval` (or the "Run ablation" button) runs the same question two ways and scores both
against a gold set of official SSW facts. The gap *is* the evidence that grounding works.

## Status
- ✅ Round 1: agents, RAG grounding, real jobs + gov stats, ablation proof, FastAPI + Next.js UI.
- 🔜 Round 2: Amadeus flights, more sectors, PDF dossier export, multilingual (EN/HI/JA).

---
*Smoke tests: `python scripts/smoke.py` (full pipeline) · `python scripts/eval_smoke.py` (ablation).*
