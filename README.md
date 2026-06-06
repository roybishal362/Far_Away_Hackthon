# 🚀 Far Away — Strike Kit

A deploy-ready Streamlit + Python/ML starter for the **Far Away** hackathon (Round 1 MVP).
Built small on purpose: **thin app, smart core, proof not claims** — and structured so it
can grow fast in Rounds 2 & 3 without a rewrite.

## What this is
A working end-to-end ML demo skeleton with three **swappable slots**:

| File | Slot | Swap this when the theme drops |
|------|------|--------------------------------|
| `src/data.py` | **Data** — load & prep inputs | point it at the real dataset/API/upload |
| `src/model.py` | **Model** — the smart core | drop in the real model / API / pretrained pipeline |
| `src/evaluate.py` | **Evaluation** — the proof | the metrics & charts that prove it's real |
| `app.py` | **UI** — Streamlit front | usually unchanged; it just calls the slots |

The contract: keep each slot's function *signatures* stable, change only the insides.
That's what lets us extend fast later instead of rewriting.

## Design principles (we hold ourselves to these)
1. **Thin app, smart + proven core** — one feature, working, backed by numbers.
2. **Modular, not pre-built** — clean swappable slots, not unused infrastructure.
3. **Always submittable** — runs end-to-end every day; build in vertical slices.
4. **Evidence over claims** — every claim traces to a metric, a baseline, or a chart.
5. **Demo is the product** — a flawless 60-second story.

## Run it
This project runs in the **cloud** (Streamlit Community Cloud / Codespaces / Colab),
not on a locked-down local machine.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Push this repo to GitHub.
2. Go to share.streamlit.io → New app → pick this repo → main file `app.py`.
3. Deploy → you get a public URL. That URL is the demo for judges.

---
*Placeholder demo currently uses the iris dataset so the pipeline runs today.
Swap the slots on theme-day.*
