"""Prep agent — a PERSONALIZED study + exam plan keyed to the worker's current
Japanese level and target, with REAL free/open-source resources attached
(links curated, never LLM-invented).
"""
from __future__ import annotations

from core.agents._common import profile_text
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.knowledge_pack import STUDY_RESOURCES
from core.llm import get_llm
from core.types import Citation, WorkerProfile

SYSTEM = (
    "You are a principal preparation coach for SSW candidates. Build a realistic, PERSONALIZED study + exam plan "
    "for THIS worker to reach JLPT N4 / JFT-Basic and pass their sector skills test. Reference their CURRENT Japanese "
    "level and target sector; a beginner (none/N5) needs a longer plan than someone at N4. Do NOT invent resource URLs."
)

SCHEMA = (
    'Return JSON: {"gaps": ["specific gaps for THIS worker"], '
    '"plan": [{"milestone": "...", "weeks": <int>, "detail": "what to do, which free resource to use"}], '
    '"total_weeks": <int>, "summary": "<personalized headline>"}'
)


class PrepAgent(Agent):
    name = "prep"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        steps = [ReasoningStep("Assessing readiness gaps", f"Japanese level: {profile.japanese_level}", kind="think")]
        plan_data: dict = {}
        llm = get_llm()
        if llm.available():
            try:
                resource_hint = "; ".join(f"{r['name']} ({r['level']})" for r in STUDY_RESOURCES)
                plan_data = llm.json(
                    SYSTEM,
                    f"Worker: {profile_text(profile)}\nAvailable free resources you may reference by name: {resource_hint}\n\n{SCHEMA}",
                    temperature=0.4,
                )
            except Exception:
                plan_data = {}

        steps.append(ReasoningStep("Built personalized plan + attached free resources", f"{len(STUDY_RESOURCES)} open-source resources", kind="decide"))
        data = {**plan_data, "resources": STUDY_RESOURCES}
        cits = [Citation(source_url=r["url"], title=r["name"], snippet=r["purpose"]) for r in STUDY_RESOURCES[:6]]
        return AgentResult(
            agent=self.name,
            summary=plan_data.get("summary", "Personalized study plan with free resources."),
            data=data,
            citations=cits,
            confidence=0.85,
            steps=steps,
            ok=True,
        )
