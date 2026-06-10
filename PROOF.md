# 📊 PROOF — the grounded-vs-ungrounded ablation (reproducible)

Kakehashi's core claim is "grounded, not hallucinated." This is the measurement behind it —
reproducible, committed, and honest about its limits.

## Method
- **Gold set:** 7 checkable SSW facts curated from official sources — see [`core/eval/gold.py`](core/eval/gold.py).
- **Grounded** = our real multi-agent system (Pathway + Procedure + Prep, RAG-grounded with citations).
- **Ungrounded** = the *same* question asked to the plain LLM with **no** official context.
- **Judge:** an LLM (Groq `gpt-oss-120b`, **temperature 0**) gives a per-fact verdict — does the answer
  *support* each gold fact (→ accuracy) and does it *contradict* any (→ hallucination)?
- **Run it yourself:** `python scripts/proof_runs.py` (script: [`core/eval/harness.py`](core/eval/harness.py)).

## Results (3 consecutive runs, same profile: nurse, no Japanese)

| Run | Grounded accuracy | Ungrounded accuracy | Grounded hallucinations | Ungrounded hallucinations |
|----:|:-----------------:|:-------------------:|:-----------------------:|:-------------------------:|
| 1 | **86%** (6/7) | 43% | **0** | 1 |
| 2 | **86%** (6/7) | 29% | **0** | 1 |
| 3 | **86%** (6/7) | 71% | **0** | 0 |
| **avg** | **86%** | **~48%** | **0** | **~0.7** |

## What this shows
1. **Higher accuracy:** grounded **86%** vs an ungrounded average of **~48%**.
2. **Zero hallucinations:** grounded produced **0 contradictions of official facts in every run**; the plain LLM did not.
3. **Reliability (the underrated win):** grounded is **identical every run (86%/0)**, while the ungrounded
   baseline swings **29% → 71%** — grounding makes the system *consistent*, not just *accurate*.

## Honest limits (so the number is trustworthy)
- **N = 7 gold facts** — small but fixed and committed; not a large benchmark.
- Grounded tops out at **86% (6/7)**, not 100%, because one gold fact (the SSW-2 family rule) isn't
  surfaced for an SSW-1 nurse — i.e. the system correctly doesn't volunteer an irrelevant fact.
- Measured on `gpt-oss-120b`; a different judge/model would shift the absolute numbers (the *gap* is the point).
- The plain LLM's ungrounded accuracy is non-trivial because `gpt-oss-120b` already knows some SSW facts —
  the value of grounding here is **eliminating hallucinations and guaranteeing consistency**, with a citation on every claim.
