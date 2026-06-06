"""The proof: a grounded-vs-ungrounded ablation.

Runs the SAME question two ways — (A) grounded in official sources (our agent),
(B) ungrounded (LLM free-recall, no context) — and uses an LLM judge to score
each against the gold facts. The gap is the evidence that grounding works.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from core.agents._common import profile_text
from core.agents.pathway import PathwayAgent
from core.eval.gold import GOLD
from core.llm import get_llm
from core.types import WorkerProfile

JUDGE_SYSTEM = (
    "You are a strict fact-checker. Given numbered GOLD FACTS and an ANSWER, decide which "
    "gold facts the answer correctly supports and which it contradicts (states wrongly). "
    "Judge only against the gold facts; ignore extra detail that is not about them."
)

UNGROUNDED_SYSTEM = (
    "You are an SSW immigration advisor. Answer ONLY from your own prior knowledge. "
    "No reference material is provided."
)


@dataclass
class EvalReport:
    gold_n: int
    grounded_accuracy: float
    ungrounded_accuracy: float
    grounded_hallucinations: int
    ungrounded_hallucinations: int

    def to_dict(self) -> dict:
        return asdict(self)


def _judge(answer_text: str) -> tuple[int, int]:
    """Return (covered_count, contradicted_count) of the answer vs GOLD."""
    numbered = "\n".join(f"{i + 1}. {g}" for i, g in enumerate(GOLD))
    user = (
        f"GOLD FACTS:\n{numbered}\n\nANSWER:\n{answer_text}\n\n"
        'Return JSON: {"covered": [<indices correctly supported>], '
        '"contradicted": [<indices the answer states incorrectly>]}'
    )
    data = get_llm().json(JUDGE_SYSTEM, user)
    covered = [i for i in (data.get("covered") or []) if isinstance(i, int)]
    contradicted = [i for i in (data.get("contradicted") or []) if isinstance(i, int)]
    return len(set(covered)), len(set(contradicted))


def run_ablation(profile: WorkerProfile) -> EvalReport:
    # (A) Grounded — our real multi-agent system (RAG + citations across agents)
    from core.agents.prep import PrepAgent
    from core.agents.procedure import ProcedureAgent

    ctx: dict = {}
    parts: list[str] = []
    for agent in (PathwayAgent(), ProcedureAgent(), PrepAgent()):
        r = agent.run(profile, ctx)
        ctx[agent.name] = r
        if r.ok:
            parts.append(json.dumps(r.data))
    grounded_text = "\n".join(parts)
    g_cov, g_hall = _judge(grounded_text)

    # (B) Ungrounded — same ask, no official context
    ungrounded = get_llm().json(
        UNGROUNDED_SYSTEM,
        f"Worker: {profile_text(profile)}\nList the SSW eligibility requirements and limits as "
        'JSON: {"requirements": ["..."], "limits": ["..."]}',
    )
    u_cov, u_hall = _judge(json.dumps(ungrounded))

    n = len(GOLD)
    return EvalReport(
        gold_n=n,
        grounded_accuracy=round(g_cov / n, 3),
        ungrounded_accuracy=round(u_cov / n, 3),
        grounded_hallucinations=g_hall,
        ungrounded_hallucinations=u_hall,
    )
