"""Verify smart routing (HR -> Specialist visa), resume personalization, job ranking."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import Engine  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

# 1) HR -> should route to 'specialist' (not vague)
hr = Engine().run(WorkerProfile(skills="HR generalist, recruiting, 5 yrs", sector_interest="Human Resources", years_experience=5, japanese_level="N4"))
pw = hr.results["pathway"].data
print("HR verdict:", pw.get("eligibility_verdict"), "| route:", (pw.get("non_ssw") or {}).get("name"))
print("HR summary:", (hr.results["pathway"].summary or "")[:170])
print("HR agents:", list(hr.results.keys()))

# 2) Resume-driven + job ranking
prof = WorkerProfile(
    skills="nursing", sector_interest="Nursing Care", years_experience=3, japanese_level="N4",
    resume_text="Registered nurse, 3 years ICU at Apollo Hospital Delhi. Certified in elderly/geriatric care. JLPT N4. Seeking caregiving roles in Japan.",
)
r = Engine().run(prof)
jobs = r.results["jobs"].data.get("jobs", [])
print("\nRanked jobs (title, match%):")
for j in jobs[:5]:
    print(f"  {j.get('match')}% - {(j.get('title') or '')[:45]}")
