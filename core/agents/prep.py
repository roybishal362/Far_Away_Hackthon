"""Prep agent — given the worker's gaps (e.g. needs JLPT N4), builds a personalized
study + exam plan with a timeline, grounded in official test requirements."""
from __future__ import annotations

from core.agents._common import gather, profile_text, used_citations
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.llm import LLMNotConfigured, get_llm
from core.types import WorkerProfile

SYSTEM = (
    "You are a principal preparation coach for SSW candidates. Using ONLY the numbered OFFICIAL CONTEXT "
    "for the hard requirements (tests, language level), build a realistic study + exam plan. "
    "You MAY suggest sensible study cadence, but never misstate official test requirements."
)

SCHEMA = (
    'Return JSON: {"gaps": ["..."], '
    '"plan": [{"milestone": "...", "weeks": <int>, "detail": "..."}], '
    '"summary": "<headline>", "sources_used": [<indices>]}'
)


class PrepAgent(Agent):
    name = "prep"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        steps = [ReasoningStep("Assessing readiness gaps", f"Japanese level: {profile.japanese_level}", kind="think")]
        query = "SSW skills evaluation test Japanese language JLPT N4 JFT-Basic requirement"
        passages, ctx = gather(query, k=4)
        steps.append(ReasoningStep("Retrieved official test requirements", f"{len(passages)} cited passages", kind="tool_result"))
        if not passages:
            return AgentResult(agent=self.name, ok=False, error="No official context retrieved", steps=steps)

        user = (
            f"WORKER PROFILE:\n{profile_text(profile)}\n\nOFFICIAL CONTEXT:\n{ctx}\n\n"
            f"Identify what the worker still needs (language level, skills test) and plan it. {SCHEMA}"
        )
        try:
            data = get_llm().json(SYSTEM, user)
        except LLMNotConfigured as exc:
            return AgentResult(agent=self.name, ok=False, error=str(exc), steps=steps)

        steps.append(ReasoningStep("Built study + exam plan", kind="decide"))
        cits = used_citations(passages, data.get("sources_used"))
        return AgentResult(
            agent=self.name,
            summary=data.get("summary", ""),
            data=data,
            citations=cits,
            confidence=0.85 if cits else 0.4,
            steps=steps,
            ok=True,
        )
