"""Confirm agent output + chat localize to Hindi / Japanese."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import chat  # noqa: E402
from core.agents.pathway import PathwayAgent  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

for lang in ["hi", "ja"]:
    p = WorkerProfile(skills="nursing, 3 years", sector_interest="Nursing Care", years_experience=3, japanese_level="none", lang=lang)
    summary = PathwayAgent().run(p, {}).summary
    print(f"\n[{lang}] pathway summary: {summary[:160]}")

print("\n[ja] chat:", chat.answer("Can I bring my family on SSW?", lang="ja")["answer"][:160])
print("[hi] chat:", chat.answer("How much is the JFT-Basic test?", lang="hi")["answer"][:160])
