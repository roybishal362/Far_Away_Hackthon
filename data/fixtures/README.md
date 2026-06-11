# Recorded-real fixtures (honest demo fallback)

Files here are **recorded from real live API responses** by
`python scripts/record_fixtures.py` — never hand-written.

If a live tool call fails during judging (quota, downtime), the matching fixture
is served and the UI labels it **"cached sample (recorded from a real live run)"**.
If no fixture exists, the tool reports the real failure — nothing is ever fabricated.

Disable the fallback with `KAKEHASHI_CACHED_FALLBACK=0`.
