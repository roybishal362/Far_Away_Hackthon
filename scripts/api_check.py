"""Validate a full /run through the FastAPI layer. Run: python scripts/api_check.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402
from api.main import app  # noqa: E402

c = TestClient(app)
r = c.post("/run", json={
    "skills": "nursing, 3 years",
    "sector_interest": "caregiving",
    "years_experience": 3,
    "japanese_level": "none",
    "origin_city": "Delhi",
    "target_city": "Tokyo",
})
d = r.json()
print("HTTP", r.status_code, "| grounding_score", d["grounding_score"])
for k, v in d["results"].items():
    print(f"  {k}: ok={v['ok']} grounded={v['grounded']} citations={len(v['citations'])} conf={v['confidence']}")
