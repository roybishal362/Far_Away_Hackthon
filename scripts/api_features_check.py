"""Test the new endpoints: /chat, /save + /plan, /dossier, /resume."""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402
from api.main import app  # noqa: E402

c = TestClient(app)

# chat
r = c.post("/chat", json={"question": "Can I bring my family on SSW and how much is JFT-Basic in India?"})
print("CHAT:", r.status_code, "->", r.json()["answer"][:120], "| cites:", len(r.json()["citations"]))

# save + plan
sid = c.post("/save", json={"results": {"x": 1}, "grounding_score": 1.0}).json()["id"]
got = c.get(f"/plan/{sid}").json()
print("SAVE/PLAN:", sid, "-> reload ok:", got.get("grounding_score") == 1.0)

# dossier
plan = {"results": {"synthesis": {"data": {"summary": "Great path", "salary": {"min": 180000, "max": 250000}, "fees": [], "disclaimer": "Guidance only."}},
                    "procedure": {"data": {"steps": [{"step": "Pass JFT-Basic", "resources": [{"name": "JFT", "url": "https://x", "purpose": "test"}]}]}}}}
pdf = c.post("/dossier", json={"plan": plan, "profile": {"skills": "nursing"}})
print("DOSSIER:", pdf.status_code, "| pdf bytes:", len(pdf.content), "| starts %PDF:", pdf.content[:4] == b"%PDF")

# resume (text file)
resume_txt = b"Bishal Roy. B.Sc Nursing. 3 years hospital nursing experience. JLPT N5."
rr = c.post("/resume", files={"file": ("resume.txt", io.BytesIO(resume_txt), "text/plain")})
print("RESUME:", rr.status_code, "->", rr.json())
