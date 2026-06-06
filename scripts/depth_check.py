"""Verify the depth upgrades: real procedure links, study resources, IT routing."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import Engine  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

# 1) Caregiving — full depth
r = Engine().run(WorkerProfile(skills="nursing, 3 years", sector_interest="Nursing Care", years_experience=3, japanese_level="none"))
proc = r.results["procedure"].data
prep = r.results["prep"].data
print("=== PROCEDURE ===")
print("steps:", len(proc["steps"]), "| skills_test:", (proc.get("skills_test") or {}).get("test_name"))
print("step-2 resources:", [x["name"] for x in proc["steps"][1]["resources"]])
print("\n=== PREP ===")
print("resources:", len(prep.get("resources", [])), "| plan milestones:", len(prep.get("plan", [])))
print("sample resource:", prep["resources"][0]["name"], "->", prep["resources"][0]["url"])
print("\n=== JOBS ===")
print("count:", len(r.results["jobs"].data.get("jobs", [])))

# 2) IT — should redirect to Engineer visa
rit = Engine().run(WorkerProfile(skills="software developer, python, 4 yrs", sector_interest="Software / IT", years_experience=4, japanese_level="N4"))
pit = rit.results["pathway"].data
print("\n=== IT ROUTING ===")
print("verdict:", pit.get("eligibility_verdict"), "| has non_ssw guidance:", bool(pit.get("non_ssw")))
print("summary:", rit.results["pathway"].summary)
