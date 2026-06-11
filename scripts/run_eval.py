"""Pin the proof: run the grounded-vs-ungrounded ablation and COMMIT the evidence.

Runs the ablation over 3 SSW personas x N runs, then writes:
  eval/results.json         — every run, every per-fact verdict (auditable)
  eval/ablation_chart.png   — the deck/README chart (needs matplotlib)
  PROOF.md                  — the results section is rewritten in place
                              (between the EVAL:BEGIN / EVAL:END markers)

Usage (with GROQ_API_KEY in .env):
    python scripts/run_eval.py            # 3 personas x 3 runs (default)
    python scripts/run_eval.py --runs 5

Commit eval/results.json and eval/ablation_chart.png. The numbers you publish
in the deck/README must be THESE numbers — never hand-typed ones.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from config import SETTINGS  # noqa: E402
from core.eval.gold import GOLD  # noqa: E402
from core.eval.harness import run_ablation  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

OUT_DIR = ROOT / "eval"
MARK_BEGIN, MARK_END = "<!-- EVAL:BEGIN -->", "<!-- EVAL:END -->"

# SSW-route personas (the ablation measures SSW-fact grounding, so all three
# stay on the SSW route — an Engineer-route profile would be judged on facts
# the system correctly never raises for them).
PERSONAS = [
    ("nurse_no_japanese", WorkerProfile(skills="nursing, elderly care", sector_interest="Caregiving / Nursing care",
                                        years_experience=3, japanese_level="none", education="GNM Nursing", lang="en")),
    ("farm_worker_n5", WorkerProfile(skills="farming, crop work", sector_interest="Agriculture",
                                     years_experience=5, japanese_level="JLPT N5", education="High school", lang="en")),
    ("construction_n4", WorkerProfile(skills="construction, scaffolding", sector_interest="Construction",
                                      years_experience=4, japanese_level="JLPT N4", education="ITI Diploma", lang="en")),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3, help="runs per persona (default 3)")
    args = ap.parse_args()

    if not SETTINGS.groq_api_key:
        print("GROQ_API_KEY is not configured — cannot run the ablation. Add it to .env first.")
        return 1

    rows: list[dict] = []
    for pname, profile in PERSONAS:
        for i in range(args.runs):
            print(f"[{pname}] run {i + 1}/{args.runs} …", flush=True)
            rep = run_ablation(profile)
            rows.append({"persona": pname, "run": i + 1, **rep.to_dict()})
            print(f"    grounded {rep.grounded_accuracy:.0%} / {rep.grounded_hallucinations} hall.   "
                  f"ungrounded {rep.ungrounded_accuracy:.0%} / {rep.ungrounded_hallucinations} hall.")

    g_acc = [r["grounded_accuracy"] for r in rows]
    u_acc = [r["ungrounded_accuracy"] for r in rows]
    g_hall = [r["grounded_hallucinations"] for r in rows]
    u_hall = [r["ungrounded_hallucinations"] for r in rows]
    agg = {
        "gold_n": len(GOLD),
        "runs": len(rows),
        "model": SETTINGS.llm_model,
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "grounded_accuracy_mean": round(statistics.mean(g_acc), 3),
        "grounded_accuracy_min": min(g_acc), "grounded_accuracy_max": max(g_acc),
        "ungrounded_accuracy_mean": round(statistics.mean(u_acc), 3),
        "ungrounded_accuracy_min": min(u_acc), "ungrounded_accuracy_max": max(u_acc),
        "grounded_hallucinations_total": sum(g_hall),
        "ungrounded_hallucinations_total": sum(u_hall),
    }

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "results.json").write_text(
        json.dumps({"aggregate": agg, "runs": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT_DIR / 'results.json'}")

    _chart(agg)
    _rewrite_proof(agg, rows)
    print("\nAggregate:", json.dumps(agg, indent=2))
    print("\nNow commit: eval/results.json, eval/ablation_chart.png, PROOF.md")
    return 0


def _chart(agg: dict) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed — skipping chart (pip install -r requirements-dev.txt)")
        return

    navy, vermillion, grey = "#1B2A4A", "#D9381E", "#8A8F98"
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.6), facecolor="#FAFAF7")
    labels = ["Ungrounded\n(plain LLM)", "Grounded\n(Kakehashi)"]

    ax = axes[0]
    vals = [agg["ungrounded_accuracy_mean"] * 100, agg["grounded_accuracy_mean"] * 100]
    bars = ax.bar(labels, vals, color=[grey, vermillion], width=0.55)
    ax.set_title(f"Accuracy vs {agg['gold_n']} official gold facts (mean of {agg['runs']} runs)", fontsize=11)
    ax.set_ylim(0, 100); ax.set_ylabel("%")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 2, f"{v:.0f}%", ha="center", fontweight="bold", fontsize=13)

    ax = axes[1]
    vals = [agg["ungrounded_hallucinations_total"], agg["grounded_hallucinations_total"]]
    bars = ax.bar(labels, vals, color=[grey, navy], width=0.55)
    ax.set_title(f"Contradictions of official facts (total across {agg['runs']} runs)", fontsize=11)
    ax.set_ylim(0, max(vals + [1]) * 1.3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.05, str(v), ha="center", fontweight="bold", fontsize=13)

    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_facecolor("#FAFAF7")
    fig.suptitle("Grounded vs ungrounded — same questions, same judge (temp 0)", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "ablation_chart.png", dpi=200)
    print(f"Wrote {OUT_DIR / 'ablation_chart.png'}")


def _rewrite_proof(agg: dict, rows: list[dict]) -> None:
    proof = ROOT / "PROOF.md"
    if not proof.exists():
        return
    text = proof.read_text(encoding="utf-8")
    if MARK_BEGIN not in text or MARK_END not in text:
        print("PROOF.md has no EVAL markers — leaving it untouched.")
        return

    lines = [
        f"*Generated by `scripts/run_eval.py` on {agg['timestamp_utc']} · model `{agg['model']}` · "
        f"gold set N={agg['gold_n']} · raw per-fact verdicts in [`eval/results.json`](eval/results.json).*",
        "",
        "| Persona | Run | Grounded acc. | Ungrounded acc. | Grounded hall. | Ungrounded hall. |",
        "|---|---:|:---:|:---:|:---:|:---:|",
    ]
    for r in rows:
        lines.append(f"| {r['persona']} | {r['run']} | **{r['grounded_accuracy']:.0%}** | "
                     f"{r['ungrounded_accuracy']:.0%} | **{r['grounded_hallucinations']}** | "
                     f"{r['ungrounded_hallucinations']} |")
    lines += [
        f"| **mean / total** | | **{agg['grounded_accuracy_mean']:.0%}** | {agg['ungrounded_accuracy_mean']:.0%} "
        f"| **{agg['grounded_hallucinations_total']}** | {agg['ungrounded_hallucinations_total']} |",
        "",
        f"![Ablation chart](eval/ablation_chart.png)",
    ]
    block = MARK_BEGIN + "\n" + "\n".join(lines) + "\n" + MARK_END
    head, _, rest = text.partition(MARK_BEGIN)
    _, _, tail = rest.partition(MARK_END)
    proof.write_text(head + block + tail, encoding="utf-8")
    print("Rewrote the results section of PROOF.md")


if __name__ == "__main__":
    raise SystemExit(main())
