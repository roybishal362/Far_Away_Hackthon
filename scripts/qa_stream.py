"""QA: consume the SSE stream and verify normal vs redirect runs behave correctly."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402
from api.main import app  # noqa: E402

c = TestClient(app)


def run(profile):
    steps, result = [], None
    with c.stream("POST", "/run/stream", json=profile) as resp:
        event = None
        for line in resp.iter_lines():
            if not line:
                continue
            if line.startswith("event:"):
                event = line[6:].strip()
            elif line.startswith("data:"):
                data = json.loads(line[5:].strip())
                if event == "step":
                    steps.append((data["agent"], data["kind"]))
                elif event == "result":
                    result = data
    return steps, result


print("=== NURSING (SSW) ===")
s, res = run({"skills": "nursing", "sector_interest": "Nursing Care", "years_experience": 3, "japanese_level": "none"})
print("agents in results:", list(res["results"].keys()))
print("skip steps:", [a for a, k in s if k == "skip"], "| stream completed:", res is not None)

print("\n=== IT (redirect) ===")
s2, res2 = run({"skills": "software developer python", "sector_interest": "Software / IT", "years_experience": 4, "japanese_level": "N4"})
print("results keys:", list(res2["results"].keys()))
print("verdict:", res2["results"]["pathway"]["data"].get("eligibility_verdict"))
print("skip steps:", [a for a, k in s2 if k == "skip"], "| stream completed:", res2 is not None)
