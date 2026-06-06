"""Run the grounded-vs-ungrounded ablation. Run: python scripts/eval_smoke.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.eval.harness import run_ablation  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

profile = WorkerProfile(
    skills="nursing, 3 years hospital experience",
    sector_interest="caregiving",
    years_experience=3,
    japanese_level="none",
)

report = run_ablation(profile)
print("=== ABLATION: grounded (our agent) vs ungrounded (LLM free-recall) ===")
print(f"Gold facts: {report.gold_n}")
print(f"GROUNDED   accuracy: {report.grounded_accuracy:.0%}   hallucinations: {report.grounded_hallucinations}")
print(f"UNGROUNDED accuracy: {report.ungrounded_accuracy:.0%}   hallucinations: {report.ungrounded_hallucinations}")
