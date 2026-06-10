"""Generate deck assets (real, on-brand): ablation chart + architecture + reroute diagrams.
Run: python scripts/make_assets.py  ->  deck_assets/*.png
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "deck_assets")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1B2A4A"
VERM = "#D9381E"
OFFW = "#FAFAF7"
GREY = "#8A8F98"
LGREY = "#D9DBE0"

plt.rcParams["font.family"] = "DejaVu Sans"


# ───────────────────────── 1 · ABLATION CHART (3 runs) ─────────────────────────
def chart():
    runs = ["Run 1", "Run 2", "Run 3"]
    grounded = [86, 86, 86]
    ungrounded = [43, 29, 71]
    x = np.arange(3)
    w = 0.36
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=200)
    fig.patch.set_facecolor(OFFW)
    ax.set_facecolor(OFFW)
    b1 = ax.bar(x - w / 2, grounded, w, color=VERM, label="Grounded (ours)", zorder=3)
    b2 = ax.bar(x + w / 2, ungrounded, w, color=NAVY, label="Ungrounded plain LLM", zorder=3)
    ax.axhline(86, ls="--", color=VERM, lw=1, alpha=0.45, zorder=1)
    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(runs, color=NAVY, fontsize=11)
    ax.set_ylabel("Accuracy vs official facts (%)", color=NAVY, fontsize=11)
    ax.tick_params(colors=NAVY)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(GREY)
    for b in b1:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{int(b.get_height())}%", ha="center", color=VERM, fontweight="bold", fontsize=11)
    for b in b2:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{int(b.get_height())}%", ha="center", color=NAVY, fontweight="bold", fontsize=11)
    ax.set_title("Grounded: 86% every run  ·  Plain LLM: swings 29–71%",
                 color=NAVY, fontsize=14, fontweight="bold", pad=16)
    ax.legend(frameon=False, loc="upper center", ncol=2, fontsize=10, bbox_to_anchor=(0.5, -0.13))
    fig.text(0.5, 0.005,
             "Hallucinations (contradicting official facts): grounded 0 every run · plain LLM up to 1   ·   gold set = 7 official facts · reproducible (PROOF.md)",
             ha="center", color=GREY, fontsize=8.5)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(os.path.join(OUT, "chart_ablation.png"), facecolor=OFFW)
    plt.close(fig)


# ───────────────────────── helpers for diagrams ─────────────────────────
def box(ax, x, y, w, h, title, fill, tcolor="white", sub=None, struck=False, fs=10):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.08",
                                fc=fill, ec="none", zorder=3))
    ty = y + h / 2 + (0.08 if sub else 0)
    ax.text(x + w / 2, ty, title, ha="center", va="center", color=tcolor, fontsize=fs, fontweight="bold", zorder=4)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.13, sub, ha="center", va="center", color=tcolor, fontsize=7.2, alpha=0.85, zorder=4)
    if struck:
        ax.plot([x + 0.06, x + w - 0.06], [y + h / 2, y + h / 2], color=tcolor, lw=1.1, zorder=5)


def arrow(ax, p1, p2, color=GREY):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=11, color=color, lw=1.3, shrinkA=1, shrinkB=1, zorder=2))


# ───────────────────────── 2 · ARCHITECTURE DIAGRAM ─────────────────────────
def architecture():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
    fig.patch.set_facecolor(OFFW)
    ax.set_facecolor(OFFW)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.text(0.3, 7.7, "Six specialized agents — each: reason → call a real tool → cite the source → score confidence",
            color=NAVY, fontsize=12.5, fontweight="bold")

    box(ax, 0.4, 6.2, 2.3, 0.95, "User profile /\nresume", NAVY)
    box(ax, 4.55, 6.2, 3.2, 0.95, "Orchestrator + LLM Router", VERM, fs=10)
    arrow(ax, (2.7, 6.67), (4.55, 6.67))

    agents = [
        ("Pathway", "SSW · MOFA RAG"), ("Jobs", "JSearch API"), ("Procedure", "ssw.go.jp (ISA)"),
        ("Study plan", "free resources"), ("Synthesis", "salary · cost (sourced)"), ("Q&A", "grounded RAG"),
    ]
    ax_w, gap = 1.72, 0.2
    x0 = 0.4
    for i, (t, s) in enumerate(agents):
        x = x0 + i * (ax_w + gap)
        box(ax, x, 4.1, ax_w, 1.0, t, NAVY, sub=s, fs=9.5)
        arrow(ax, (6.15, 6.2), (x + ax_w / 2, 5.1))   # router -> agent
        arrow(ax, (x + ax_w / 2, 4.1), (x + ax_w / 2, 3.35))  # agent -> verification

    box(ax, 0.4, 2.3, 11.2, 1.0,
        "Verification & Citation layer  —  source + confidence on every claim, or 'not configured' (never fabricates)",
        VERM, fs=9)
    box(ax, 2.9, 0.55, 6.2, 1.0, "Migration Dossier (PDF)  ·  SSE live agent timeline", NAVY, fs=10)
    arrow(ax, (6.0, 2.3), (6.0, 1.55))

    ax.text(0.4, 0.2, "Next.js · FastAPI (SSE) · Groq gpt-oss-120b · BM25 RAG · Fernet-encrypted PII",
            color=GREY, fontsize=9)
    fig.savefig(os.path.join(OUT, "diagram_architecture.png"), facecolor=OFFW, bbox_inches="tight")
    plt.close(fig)


# ───────────────────────── 3 · REROUTE DIAGRAM ─────────────────────────
def reroute():
    fig, ax = plt.subplots(figsize=(12, 6.4), dpi=200)
    fig.patch.set_facecolor(OFFW)
    ax.set_facecolor(OFFW)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.text(0.3, 6.6, "The plan changes shape per person — the router decides the route, not a template",
            color=NAVY, fontsize=12.5, fontweight="bold")

    box(ax, 0.4, 3.0, 2.2, 1.1, "LLM Router\nclassifies visa route", VERM, fs=10)

    # Top branch — nurse → full SSW chain
    box(ax, 3.1, 4.7, 1.9, 0.9, "Priya · Nurse", NAVY, fs=10)
    arrow(ax, (2.6, 3.9), (3.1, 5.15))
    chain = ["Skills test", "JFT-Basic", "Find job", "CoE", "SSW visa"]
    cx = 5.3
    prev = (5.0, 5.15)
    for i, c in enumerate(chain):
        x = cx + i * 1.32
        box(ax, x, 4.75, 1.2, 0.8, c, NAVY, fs=8.5)
        arrow(ax, prev, (x, 5.15))
        prev = (x + 1.2, 5.15)

    # Bottom branch — software → SSW steps auto-skipped → Engineer visa
    box(ax, 3.0, 1.2, 2.5, 0.9, "Arjun · Software", NAVY, fs=9.5)
    arrow(ax, (2.6, 3.2), (3.0, 1.65))
    box(ax, 5.7, 1.25, 3.0, 0.8, "SSW steps (auto-skipped)", LGREY, tcolor=GREY, struck=True, fs=9)
    arrow(ax, (5.5, 1.65), (5.7, 1.65))
    box(ax, 8.9, 1.2, 2.8, 0.9, "Engineer / Specialist visa", VERM, fs=9)
    arrow(ax, (8.7, 1.65), (8.9, 1.65))

    ax.text(0.4, 0.45, "Same input form → structurally different plans (routing + auto-skip at runtime).  HR profile → Specialist visa.",
            color=GREY, fontsize=9.5)
    fig.savefig(os.path.join(OUT, "diagram_reroute.png"), facecolor=OFFW, bbox_inches="tight")
    plt.close(fig)


chart()
architecture()
reroute()
print("Saved 3 assets to:", OUT)
for f in ("chart_ablation.png", "diagram_architecture.png", "diagram_reroute.png"):
    p = os.path.join(OUT, f)
    print(" -", f, f"({os.path.getsize(p) // 1024} KB)" if os.path.exists(p) else "(MISSING)")
