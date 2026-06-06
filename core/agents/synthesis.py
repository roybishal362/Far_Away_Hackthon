"""Synthesis agent — runs last, composes a warm personalized overview of the
worker's journey plus concrete salary & cost numbers. Speaks for the whole system.
"""
from __future__ import annotations

from core import knowledge_pack as KP
from core.agents._common import lang_directive, profile_text
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.llm import get_llm
from core.types import Citation, WorkerProfile


class SynthesisAgent(Agent):
    name = "synthesis"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        steps = [ReasoningStep("Composing your personalized journey overview", kind="think")]
        pathway = context.get("pathway")
        jobs = context.get("jobs")

        sector = profile.sector_interest or ""
        verdict = readiness = None
        if pathway and getattr(pathway, "data", None):
            verdict = pathway.data.get("eligibility_verdict")
            readiness = pathway.data.get("readiness_percent")
            recs = pathway.data.get("recommended_sectors") or []
            if recs and isinstance(recs[0], dict) and recs[0].get("sector"):
                sector = recs[0]["sector"]

        salary = KP.salary_for(sector)
        n_jobs = len(jobs.data.get("jobs", [])) if jobs and getattr(jobs, "data", None) else 0

        note = ""
        llm = get_llm()
        if llm.available():
            try:
                d = llm.json(
                    "You are Kakehashi. Write a warm, motivating 3-4 sentence personal overview of this worker's "
                    "path to Japan. Be specific and encouraging; do not invent facts.",
                    f"Worker: {profile_text(profile)}\nVerdict: {verdict} | readiness {readiness}% | sector {sector} | "
                    f"{n_jobs} live jobs | salary ¥{salary['min']:,}-{salary['max']:,}/mo\nReturn JSON {{\"summary\":\"...\"}}" + lang_directive(profile),
                    temperature=0.5,
                )
                note = d.get("summary", "")
            except Exception:
                note = ""

        data = {
            "sector": sector,
            "salary": salary,
            "salary_note": KP.SALARY_NOTE,
            "fees": KP.FEES,
            "verdict": verdict,
            "readiness": readiness,
            "live_jobs": n_jobs,
            "summary": note,
            "disclaimer": KP.DISCLAIMER,
        }
        steps.append(ReasoningStep("Overview, salary & cost compiled", kind="decide"))
        return AgentResult(
            agent=self.name,
            summary=note or f"Your {sector or 'SSW'} journey overview, salary range, and costs.",
            data=data,
            citations=[Citation(source_url=s["url"], title=s["name"]) for s in KP.SALARY_SOURCES],
            confidence=0.9,
            steps=steps,
            ok=True,
        )
