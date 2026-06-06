"""Pathway agent — determines the worker's eligible SSW sector(s) + requirements,
grounded strictly in official sources (every claim cites a real passage)."""
from __future__ import annotations

from core.agents._common import gather, profile_text, used_citations
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.llm import LLMNotConfigured, get_llm
from core.types import WorkerProfile

SYSTEM = (
    "You are a principal immigration-pathway advisor for Japan's Specified Skilled Worker (SSW) program. "
    "Use ONLY the numbered OFFICIAL CONTEXT provided. Never invent facts, numbers, or sectors. "
    "If the context does not support a claim, omit it. Reference the context indices you relied on."
)

SCHEMA = (
    'Return JSON: {"eligibility": "<assessment>", '
    '"recommended_sectors": [{"sector": "...", "why": "..."}], '
    '"requirements": ["..."], "caveats": ["..."], '
    '"summary": "<2-3 sentence headline>", "sources_used": [<context indices>]}'
)


class PathwayAgent(Agent):
    name = "pathway"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        steps = [ReasoningStep("Analyzing profile against SSW eligibility", kind="think")]
        query = f"{profile.skills} {profile.sector_interest} SSW eligibility requirements Japanese language test sectors age"
        passages, ctx = gather(query, k=5)
        steps.append(ReasoningStep("Retrieved official SSW rules", f"{len(passages)} cited passages", kind="tool_result"))
        if not passages:
            return AgentResult(agent=self.name, ok=False, error="No official context retrieved", steps=steps)

        user = f"WORKER PROFILE:\n{profile_text(profile)}\n\nOFFICIAL CONTEXT:\n{ctx}\n\n{SCHEMA}"
        try:
            data = get_llm().json(SYSTEM, user)
        except LLMNotConfigured as exc:
            return AgentResult(agent=self.name, ok=False, error=str(exc), steps=steps)

        steps.append(ReasoningStep("Decided eligible pathway", kind="decide"))
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
