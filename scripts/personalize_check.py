"""Confirm Pathway gives DIFFERENT, personalized output per profile."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.pathway import PathwayAgent  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

profiles = [
    WorkerProfile(skills="nursing, 3 years hospital", sector_interest="caregiving", years_experience=3, japanese_level="none"),
    WorkerProfile(skills="construction site supervisor, 6 years", sector_interest="construction", years_experience=6, japanese_level="N4"),
    WorkerProfile(skills="fresh graduate, no work experience", sector_interest="agriculture", years_experience=0, japanese_level="N5"),
]

for p in profiles:
    d = PathwayAgent().run(p, {}).data or {}
    print(f"\n== {p.sector_interest} | {p.japanese_level} | {p.years_experience}y ==")
    print("verdict :", d.get("eligibility_verdict"), "| readiness:", d.get("readiness_percent"))
    print("summary :", d.get("summary"))
    print("need    :", d.get("what_you_need"))
