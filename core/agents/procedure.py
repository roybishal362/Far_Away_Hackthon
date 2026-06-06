"""Procedure agent — builds the step-by-step immigration checklist + document list,
grounded in official SSW procedure facts (cited)."""
from __future__ import annotations

from core.agents._common import gather, profile_text, used_citations
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.llm import LLMNotConfigured, get_llm
from core.types import WorkerProfile

SYSTEM = (
    "You are a principal SSW procedures specialist. Using ONLY the numbered OFFICIAL CONTEXT, "
    "produce a correct, ordered checklist to move from applicant to working in Japan. "
    "Do not invent steps, fees, or office names not supported by the context."
)

SCHEMA = (
    'Return JSON: {"steps": [{"step": "...", "detail": "..."}], '
    '"documents": ["..."], "summary": "<headline>", "sources_used": [<indices>]}'
)


class ProcedureAgent(Agent):
    name = "procedure"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        steps = [ReasoningStep("Mapping the immigration procedure", kind="think")]
        sector = ""
        pathway = context.get("pathway")
        if pathway and getattr(pathway, "data", None):
            recs = pathway.data.get("recommended_sectors") or []
            sector = recs[0].get("sector", "") if recs and isinstance(recs[0], dict) else ""

        query = f"SSW application procedure steps documents skills test JLPT N4 visa {sector}"
        passages, ctx = gather(query, k=6)
        steps.append(ReasoningStep("Retrieved official procedure rules", f"{len(passages)} cited passages", kind="tool_result"))
        if not passages:
            return AgentResult(agent=self.name, ok=False, error="No official context retrieved", steps=steps)

        user = f"WORKER PROFILE:\n{profile_text(profile)}\nTARGET SECTOR: {sector or 'open'}\n\nOFFICIAL CONTEXT:\n{ctx}\n\n{SCHEMA}"
        try:
            data = get_llm().json(SYSTEM, user)
        except LLMNotConfigured as exc:
            return AgentResult(agent=self.name, ok=False, error=str(exc), steps=steps)

        steps.append(ReasoningStep("Built ordered checklist", kind="decide"))
        cits = used_citations(passages, data.get("sources_used"))
        return AgentResult(
            agent=self.name,
            summary=data.get("summary", ""),
            data=data,
            citations=cits,
            confidence=0.9 if cits else 0.4,
            steps=steps,
            ok=True,
        )
