# What changed in this pass (review with `git diff` / `git status`)

## 1. The ablation is now defensible (biggest fix)
- **`core/eval/gold.py`** — gold set **7 → 22 facts**, now covering eligibility, tests, stay limits,
  **worker rights & anti-scam protections** (no deposits, equal pay, support plans, job-change rights),
  the COE process, and the India corridor. Your headline stat no longer rests on N=7.
- **`core/rag/knowledge.py`** — KB **14 → 26 facts** so retrieval can actually ground the new gold facts.
  ⚠️ Verify each new fact against the live official page before submission (note is in the file).
- **`core/eval/harness.py`** — the judge now returns **per-fact verdicts**, committed with results, so
  anyone can audit exactly which facts were covered/contradicted.
- **`scripts/run_eval.py`** (new) — pins the proof: 3 SSW personas × 3 runs → `eval/results.json` +
  `eval/ablation_chart.png` (deck-ready, palette-matched) + auto-rewrites the PROOF.md table.
- **`PROOF.md`** — restructured with auto-regen markers; old N=7 numbers moved to a clearly-labeled
  legacy section. **Old numbers are STALE against the new gold set — you must re-run.**

## 2. The demo can no longer die during judging
- **`core/tools/cache.py`** (new) — TTL cache; repeated persona clicks don't burn JSearch quota.
- **`core/tools/fixtures.py`** + **`scripts/record_fixtures.py`** (new) — record REAL JSearch responses
  once; if the live API fails, the app serves them **labeled "cached sample (recorded from a real live
  run)"**. No fixture → honest failure. "Real or nothing" preserved.
- **`core/tools/jobs.py`** — wired to both (cache → live → labeled fallback).

## 3. API hardening
- **`api/middleware.py`** (new) — per-IP sliding-window rate limit (`RATE_LIMIT_PER_MIN`, default 40).
- **`api/main.py`** — CORS now env-configurable (`ALLOWED_ORIGINS`); **bug fix:** the SSE `start` event
  was missing `synthesis` (hardcoded stale list — now derived from the engine).

## 4. Engineering-quality proof
- **`tests/`** (new, 22 tests, all passing, fully offline) — gold/KB consistency, retriever grounding,
  sector→keyword router, **adaptive skip logic as a test** (your "agentic not a workflow" claim is now
  literally tested), tool honesty (labeled fallback, never silent fabrication), cache, rate limiter,
  share-link path-traversal guard.
- **`.github/workflows/tests.yml`** (new) — CI runs pytest on every push (green badge on the repo).
- **`requirements-dev.txt`** (new) — pytest + matplotlib.

## 5. Repo fixes
- **`.gitignore`** — `data/` blanket-ignore narrowed to `data/plans/` + `data/raw/` (fixtures must be
  committable); removed a stray `README.md` ignore line that would have silently excluded new docs.
- **`README.md` / `DEPLOY.md`** — stale 86% numbers removed (regenerate, never hand-type), new
  hardening section, pre-deploy proof checklist.

## ⚠️ YOUR three actions (in order, ~20 minutes)
1. `python -m pytest -q` → confirm 22 passing on your machine.
2. `python scripts/record_fixtures.py` → commit `data/fixtures/`.
3. `python scripts/run_eval.py` → commit `eval/` + PROOF.md, and copy THOSE numbers into the deck.

## 🔑 Security note
`.env` (with real keys) is in this folder and was inside the zip you shared. It is **not** in git
history (verified) — GitHub is clean. But the keys have now traveled inside a zip at least once:
**rotate `GROQ_API_KEY` and `JSEARCH_API_KEY` before deploying** if that zip went anywhere else.
