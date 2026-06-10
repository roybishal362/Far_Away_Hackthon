"""Run the ablation N times to publish reproducible numbers. Run: python scripts/proof_runs.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.eval.gold import GOLD  # noqa: E402
from core.eval.harness import run_ablation  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

p = WorkerProfile(skills="nursing, 3 years", sector_interest="Nursing Care", years_experience=3, japanese_level="none")
print(f"Gold facts: {len(GOLD)}")
print("run | grounded_acc | ungrounded_acc | grounded_hall | ungrounded_hall")
for i in range(3):
    r = run_ablation(p)
    print(f"{i+1} | {r.grounded_accuracy:.2f} | {r.ungrounded_accuracy:.2f} | {r.grounded_hallucinations} | {r.ungrounded_hallucinations}")
