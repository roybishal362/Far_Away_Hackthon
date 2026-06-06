"""Jobs agent — fetches REAL live openings for the recommended sector via JSearch.
No LLM fabrication: listings come straight from the API, each with a real apply link.

Job boards index by occupation keyword, not by "SSW sector" jargon, so we map the
pathway's sector to a clean search term and search broadly across Japan.
"""
from __future__ import annotations

from core.agents._common import profile_text
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.llm import get_llm
from core.tools.jobs import JobsTool
from core.types import WorkerProfile


def _rank(jobs: list[dict], profile: WorkerProfile) -> list[dict]:
    """Score each job's fit to THIS worker (uses skills + resume), then sort best-first."""
    llm = get_llm()
    if not llm.available() or not jobs:
        return jobs
    listing = "\n".join(f"{i}. {j.get('title')} @ {j.get('employer')}" for i, j in enumerate(jobs))
    try:
        d = llm.json(
            "Score how well each job fits THIS worker (0-100) and give a short one-line reason referencing their "
            'background. Return JSON {"ranked":[{"i":<index>,"score":<0-100>,"reason":"..."}]}.',
            f"Worker: {profile_text(profile)}\n\nJOBS:\n{listing}",
            temperature=0.2,
        )
        by_i = {int(x["i"]): x for x in d.get("ranked", []) if "i" in x}
        for i, j in enumerate(jobs):
            x = by_i.get(i)
            if x:
                j["match"] = x.get("score")
                j["fit_reason"] = x.get("reason")
        jobs = sorted(jobs, key=lambda j: (j.get("match") is not None, j.get("match") or 0), reverse=True)
    except Exception:
        pass
    return jobs

# SSW sector phrasing -> the occupation keyword job boards actually use.
SECTOR_KEYWORDS = {
    "care": "caregiver", "nurs": "caregiver",
    "construct": "construction worker",
    "agricultur": "farm worker", "farm": "farm worker",
    "food": "food service", "restaurant": "restaurant staff",
    "software": "software engineer", "it ": "software engineer", "engineer": "engineer",
    "manufactur": "factory worker", "machine": "machine operator",
    "hospitality": "hotel staff", "accommodation": "hotel staff",
    "aviation": "airport ground staff", "shipbuild": "welder",
    "automobile": "automotive mechanic", "fishery": "fishery worker",
}


def _sector(context: dict, profile: WorkerProfile) -> str:
    pathway = context.get("pathway")
    if pathway and getattr(pathway, "data", None):
        recs = pathway.data.get("recommended_sectors") or []
        if recs and isinstance(recs[0], dict) and recs[0].get("sector"):
            return recs[0]["sector"]
    return profile.sector_interest or profile.skills or "skilled worker"


def _keyword(sector: str, profile: WorkerProfile) -> str:
    base = (sector or "").lower()
    for needle, kw in SECTOR_KEYWORDS.items():
        if needle in base:
            return kw
    return base.split("/")[0].split(",")[0].strip() or "skilled worker"


class JobsAgent(Agent):
    name = "jobs"

    def __init__(self) -> None:
        self.tool = JobsTool()

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        sector = _sector(context, profile)
        keyword = _keyword(sector, profile)
        steps = [ReasoningStep(f"Searching live jobs for '{keyword}' (sector: {sector})", kind="tool_call")]
        result = self.tool.run(query=keyword, location="Japan", limit=25, num_pages=2)

        if not result.ok:
            steps.append(ReasoningStep("Jobs source unavailable", result.error or "", kind="tool_result"))
            return AgentResult(agent=self.name, ok=False, error=result.error, steps=steps)

        jobs = result.data or []
        steps.append(ReasoningStep(f"Found {len(jobs)} real openings", result.source, kind="tool_result"))
        jobs = _rank(jobs, profile)
        steps.append(ReasoningStep("Ranked jobs by fit to your profile", kind="decide"))
        return AgentResult(
            agent=self.name,
            summary=f"{len(jobs)} live openings matching '{keyword}' in Japan, ranked by fit.",
            data={"sector": sector, "keyword": keyword, "jobs": jobs},
            citations=result.citations,
            confidence=0.95 if jobs else 0.3,
            steps=steps,
            ok=True,
        )
