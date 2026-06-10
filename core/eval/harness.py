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
    """Return (covered_count, contradicted_count) of the answer vs GOLD.

    Uses a per-fact verdict object (not an index list) so the model can't mash
    indices into one number — a real bug that silently zeroed the score.
    """
    numbered = "\n".join(f"{i + 1}. {g}" for i, g in enumerate(GOLD))
    user = (
        f"GOLD FACTS:\n{numbered}\n\nANSWER:\n{answer_text}\n\n"
        "For EACH gold fact, decide whether the ANSWER supports it and whether the ANSWER contradicts it. "
        'Return JSON with ONE object per fact: '
        '{"verdicts": [{"id": <fact number>, "supported": true/false, "contradicted": true/false}, ...]}'
    )
    data = get_llm().json(JUDGE_SYSTEM, user, temperature=0.0)  # deterministic scoring
    verdicts = data.get("verdicts") or []
    covered = sum(1 for v in verdicts if isinstance(v, dict) and v.get("supported"))
    contradicted = sum(1 for v in verdicts if isinstance(v, dict) and v.get("contradicted"))
    return covered, contradicted


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
        temperature=0.0,
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
