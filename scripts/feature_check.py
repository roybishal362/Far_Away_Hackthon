"""Verify synthesis, adaptive orchestration, and grounded chat."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import chat  # noqa: E402
from core.engine import Engine  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

# 1) Caregiving — full run with synthesis
r = Engine().run(WorkerProfile(skills="nursing, 3 years", sector_interest="Nursing Care", years_experience=3, japanese_level="none"))
print("CAREGIVING agents:", list(r.results.keys()))
syn = r.results.get("synthesis")
if syn:
    print("  salary:", syn.data["salary"]["min"], "-", syn.data["salary"]["max"], "| live_jobs:", syn.data["live_jobs"], "| fees:", len(syn.data["fees"]))
    print("  summary:", (syn.summary or "")[:140])

# 2) IT — adaptive: procedure/prep/journey should be SKIPPED
rit = Engine().run(WorkerProfile(skills="software developer python, 4 yrs", sector_interest="Software / IT", years_experience=4, japanese_level="N4"))
print("\nIT agents (should omit procedure/prep/journey):", list(rit.results.keys()))

# 3) Grounded chat
a = chat.answer("How much is the JFT-Basic test in India, and can I bring my family on SSW?")
print("\nCHAT answer:", a["answer"][:300])
print("chat citations:", len(a["citations"]))
