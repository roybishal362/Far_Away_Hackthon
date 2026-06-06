"""Procedure agent — serves the REAL ordered SSW journey with official links per
step (curated, never LLM-invented) + the sector's skills test, plus a short
personalized overview for THIS worker.
"""
from __future__ import annotations

from core.agents._common import lang_directive, profile_text
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.knowledge_pack import PROCEDURE_STEPS, skills_test_for
from core.llm import get_llm
from core.types import Citation, WorkerProfile


def _sector(profile: WorkerProfile, context: dict) -> str:
    pathway = context.get("pathway")
    if pathway and getattr(pathway, "data", None):
        recs = pathway.data.get("recommended_sectors") or []
        if recs and isinstance(recs[0], dict) and recs[0].get("sector"):
            return recs[0]["sector"]
    return profile.sector_interest or ""


class ProcedureAgent(Agent):
    name = "procedure"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        sector = _sector(profile, context)
        skills = skills_test_for(sector)
        steps_log = [
            ReasoningStep("Assembling the official SSW procedure", kind="think"),
            ReasoningStep(
                f"Loaded {len(PROCEDURE_STEPS)} official steps with real links",
                f"sector skills test: {skills['test_name'] if skills else 'general (see Prometric list)'}",
                kind="tool_result",
            ),
        ]

        # Personalized overview ONLY (links come from curated data, never the LLM).
        summary = ""
        llm = get_llm()
        if llm.available():
            try:
                d = llm.json(
                    "You are an SSW procedures advisor. Write a concise, personalized 2-3 sentence overview of the "
                    "migration journey for THIS worker. Do NOT invent any URLs or step names.",
                    f"Worker: {profile_text(profile)}\nTarget sector: {sector or 'open'}\nReturn JSON {{\"summary\": \"...\"}}" + lang_directive(profile),
                    temperature=0.4,
                )
                summary = d.get("summary", "")
            except Exception:
                summary = ""

        steps_log.append(ReasoningStep("Built step-by-step plan with official links", kind="decide"))
        data = {"steps": PROCEDURE_STEPS, "skills_test": skills, "sector": sector, "summary": summary}
        cits = [Citation(source_url="https://www.ssw.go.jp/en/about/step/", title="ISA - Steps to Working in Japan")]
        if skills:
            cits.append(Citation(source_url=skills["register_url"], title=f"{skills['sector']} skills test - register"))

        return AgentResult(
            agent=self.name,
            summary=summary or f"A {len(PROCEDURE_STEPS)}-step official SSW journey for {sector or 'your sector'}, each step with real links.",
            data=data,
            citations=cits,
            confidence=0.95,
            steps=steps_log,
            ok=True,
        )
