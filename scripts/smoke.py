"""End-to-end smoke test of the agent engine. Run: python scripts/smoke.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.engine import Engine  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

profile = WorkerProfile(
    skills="nursing, 3 years hospital experience",
    sector_interest="caregiving",
    years_experience=3,
    japanese_level="none",
    origin_city="Delhi",
    target_city="Tokyo",
)

print("=== TIMELINE ===")
res = Engine().run(profile, on_step=lambda a, s: print(f"  [{a}] {s.kind}: {s.label}"))

print("\n=== RESULTS ===")
for name, ar in res.results.items():
    print(f"\n## {name}: ok={ar.ok} conf={ar.confidence} grounded={ar.grounded()}")
    if ar.ok:
        print("   summary:", ar.summary)
        print("   citations:", [c.short() for c in ar.citations])
    else:
        print("   error:", ar.error)

print("\n=== METRICS ===")
print(res.metrics)
