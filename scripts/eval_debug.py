"""Debug the ablation: is the judge mis-parsing, or is grounding genuinely not covering?"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agents.pathway import PathwayAgent  # noqa: E402
from core.agents.prep import PrepAgent  # noqa: E402
from core.agents.procedure import ProcedureAgent  # noqa: E402
from core.eval.gold import GOLD  # noqa: E402
from core.eval.harness import JUDGE_SYSTEM  # noqa: E402
from core.llm import get_llm  # noqa: E402
from core.types import WorkerProfile  # noqa: E402

p = WorkerProfile(skills="nursing, 3 years", sector_interest="Nursing Care", years_experience=3, japanese_level="none")
ctx, parts = {}, []
for a in (PathwayAgent(), ProcedureAgent(), PrepAgent()):
    r = a.run(p, ctx)
    ctx[a.name] = r
    if r.ok:
        parts.append(json.dumps(r.data))
grounded = "\n".join(parts)
print("=== GROUNDED TEXT (first 900 chars) ===")
print(grounded[:900])

numbered = "\n".join(f"{i + 1}. {g}" for i, g in enumerate(GOLD))
user = (f"GOLD FACTS:\n{numbered}\n\nANSWER:\n{grounded}\n\n"
        'Return JSON: {"covered": [<indices correctly supported>], "contradicted": [<indices wrong>]}')
raw = get_llm().json(JUDGE_SYSTEM, user, temperature=0.0)
print("\n=== JUDGE RAW OUTPUT ===")
print(raw)
print("covered types:", [type(x).__name__ for x in (raw.get('covered') or [])])
