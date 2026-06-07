"""QA: pid validation (path traversal) + save/load with profile."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402
from api.main import app  # noqa: E402

c = TestClient(app)

# save WITH profile, then load — profile should round-trip
sid = c.post("/save", json={"result": {"grounding_score": 1.0, "results": {}}, "profile": {"skills": "nursing"}}).json()["id"]
got = c.get(f"/plan/{sid}").json()
print("save/load id:", sid, "| profile.skills round-trip:", (got.get("profile") or {}).get("skills"))

# path-traversal / bad ids -> 400 (never read files)
print("dots pid '/plan/aa..bb':", c.get("/plan/aa..bb").status_code, "(expect 400)")
print("bang pid '/plan/!!!':", c.get("/plan/!!!").status_code, "(expect 400)")
print("valid-but-missing '/plan/abcdef12':", c.get("/plan/abcdef12").status_code, "(expect 404)")
