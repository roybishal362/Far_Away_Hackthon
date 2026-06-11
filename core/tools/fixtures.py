"""Recorded-real fixtures: the honest demo-fallback layer.

THE RULE ("real or nothing") STILL HOLDS:
- Fixtures are RECORDED from real, live API responses by `scripts/record_fixtures.py`
  — never hand-written, never invented.
- When a fixture is served, the result's `source` clearly says it is a cached
  sample, not a live call. The UI shows that label.
- If no fixture exists for a query, there is no fallback: the tool reports the
  real failure. We never fabricate to look alive.

Why this exists: judges click at random times. A JSearch quota blip should show
"recorded live data (cached sample)" — not a dead app.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

_DEFAULT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "fixtures"


def fixtures_dir() -> Path:
    return Path(os.environ.get("KAKEHASHI_FIXTURES_DIR", str(_DEFAULT_DIR)))


def enabled() -> bool:
    """Fallback is ON by default for demo resilience; disable with =0."""
    return os.environ.get("KAKEHASHI_CACHED_FALLBACK", "1") not in {"0", "false", "no"}


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (text or "").lower()).strip("_") or "default"


def save_jobs_fixture(keyword: str, jobs: list[dict]) -> Path:
    d = fixtures_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"jobs_{_slug(keyword)}.json"
    path.write_text(json.dumps({"keyword": keyword, "jobs": jobs}, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_jobs_fixture(keyword: str) -> list[dict] | None:
    """Exact keyword fixture first, then the generic 'skilled worker' default."""
    d = fixtures_dir()
    for name in (f"jobs_{_slug(keyword)}.json", "jobs_skilled_worker.json", "jobs_default.json"):
        p = d / name
        if p.exists():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                jobs = data.get("jobs") or []
                if jobs:
                    return jobs
            except Exception:
                continue
    return None
