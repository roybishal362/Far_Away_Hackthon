"""Record REAL JSearch responses into data/fixtures/ for the honest demo fallback.

Run this ONCE locally with your JSEARCH_API_KEY in .env, then COMMIT the
data/fixtures/*.json files. From then on, if the live API fails or hits quota
during judging, the app serves these recorded-real listings — clearly labeled
"cached sample" — instead of dying.

    python scripts/record_fixtures.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.tools import fixtures  # noqa: E402
from core.tools.jobs import JobsTool  # noqa: E402

# Keep in sync with SECTOR_KEYWORDS in core/agents/jobs.py — these are the
# keywords the agent actually searches, including the broaden-and-retry default.
KEYWORDS = [
    "caregiver",
    "software engineer",
    "construction worker",
    "farm worker",
    "factory worker",
    "hotel staff",
    "skilled worker",   # the agent's last-resort broadened query — MUST exist
]


def main() -> int:
    tool = JobsTool()
    if not tool.available():
        print("JSEARCH_API_KEY not configured — cannot record real fixtures.")
        return 1
    ok = 0
    for kw in KEYWORDS:
        print(f"Recording live results for '{kw}' …", flush=True)
        res = tool.run(query=kw, location="Japan", limit=12, num_pages=1)
        live = res.ok and "cached sample" not in (res.source or "")
        if live and res.data:
            path = fixtures.save_jobs_fixture(kw, res.data)
            print(f"  saved {len(res.data)} real listings -> {path}")
            ok += 1
        else:
            print(f"  skipped ({res.error or 'no live results'})")
    print(f"\nRecorded {ok}/{len(KEYWORDS)} fixtures. Commit data/fixtures/ to the repo.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
