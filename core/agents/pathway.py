"""Pathway agent — a PERSONALIZED SSW eligibility assessment for THIS worker,
grounded strictly in official sources (every factual claim cites a real passage).

Personalization is the whole point: two workers with different experience / Japanese
level / sector must get clearly different verdicts, gaps, readiness, and timelines.
"""
from __future__ import annotations

from core.agents._common import gather, lang_directive, profile_text, used_citations
from core.agents.base import Agent, AgentResult, ReasoningStep
from core.knowledge_pack import NON_SSW_IT, is_it_sector
from core.llm import LLMNotConfigured, get_llm
from core.types import Citation, WorkerProfile

SYSTEM = (
    "You are a principal immigration-pathway advisor for Japan's Specified Skilled Worker (SSW) program. "
    "Use ONLY the numbered OFFICIAL CONTEXT for hard facts (requirements, limits, tests) and never invent them. "
    "Your task is a PERSONALIZED assessment of THIS specific worker: reference their exact years of experience, "
    "their Japanese level, their education, and their target sector. Two different workers MUST receive clearly "
    "different verdicts, gaps, readiness scores, and timelines. Be concrete and specific to this person."
)

SCHEMA = (
    'Return JSON: {'
    '"eligibility_verdict": "eligible | eligible-with-gaps | not-yet", '
    '"readiness_percent": <integer 0-100 reflecting how ready THIS worker is now>, '
    '"recommended_sectors": [{"sector": "...", "why": "...", "fit": "high|medium|low"}], '
    '"what_you_have": ["concrete strengths drawn from THIS profile"], '
    '"what_you_need": ["specific gaps THIS worker must close, e.g. reach JLPT N4"], '
    '"timeline": "<personalized estimate, e.g. ~6-9 months given no Japanese yet>", '
    '"requirements": ["official requirements that apply"], '
    '"caveats": ["sector suspensions or limits if relevant"], '
    '"summary": "<2-3 sentence personalized headline that names THIS worker\'s situation>", '
    '"sources_used": [<context indices>]}'
)


def _heuristic_readiness(profile: WorkerProfile) -> int:
    """A deterministic floor so the score always reflects the actual inputs."""
    score = 20
    jp = (profile.japanese_level or "none").lower()
    if "n3" in jp:
        score += 45
    elif "n4" in jp:
        score += 35
    elif "n5" in jp or "jft" in jp:
        score += 20
    score += min(int(profile.years_experience * 8), 30)
    if profile.sector_interest:
        score += 5
    return max(5, min(score, 95))


class PathwayAgent(Agent):
    name = "pathway"

    def run(self, profile: WorkerProfile, context: dict) -> AgentResult:
        # Correctness guard: IT/software/engineering is NOT an SSW field — route to the Engineer visa.
        if is_it_sector(profile.sector_interest) or is_it_sector(profile.skills):
            data = {
                "eligibility_verdict": "redirect",
                "readiness_percent": None,
                "recommended_sectors": [],
                "what_you_have": [],
                "what_you_need": [NON_SSW_IT["detail"]],
                "timeline": "",
                "requirements": [],
                "caveats": [NON_SSW_IT["verdict"]],
                "summary": NON_SSW_IT["detail"],
                "non_ssw": NON_SSW_IT,
            }
            cits = [Citation(source_url=r["url"], title=r["name"], snippet=r["purpose"]) for r in NON_SSW_IT["resources"]]
            return AgentResult(
                agent=self.name,
                summary="Software/IT/engineering roles use the Engineer visa (技人国), not SSW.",
                data=data,
                citations=cits,
                confidence=0.95,
                steps=[ReasoningStep("Detected IT/engineering — routing to the correct visa", NON_SSW_IT["verdict"], kind="decide")],
                ok=True,
            )

        steps = [ReasoningStep(
            "Analyzing this profile against SSW eligibility",
            f"{profile.years_experience}y exp · Japanese: {profile.japanese_level} · sector: {profile.sector_interest or 'open'}",
            kind="think",
        )]
        query = f"{profile.skills} {profile.sector_interest} SSW eligibility requirements Japanese language test sectors age duration family"
        passages, ctx = gather(query, k=6)
        steps.append(ReasoningStep("Retrieved official SSW rules", f"{len(passages)} cited passages", kind="tool_result"))
        if not passages:
            return AgentResult(agent=self.name, ok=False, error="No official context retrieved", steps=steps)

        user = (
            f"WORKER PROFILE (assess THIS person specifically):\n{profile_text(profile)}\n\n"
            f"OFFICIAL CONTEXT:\n{ctx}\n\n{SCHEMA}" + lang_directive(profile)
        )
        try:
            data = get_llm().json(SYSTEM, user, temperature=0.3)
        except LLMNotConfigured as exc:
            return AgentResult(agent=self.name, ok=False, error=str(exc), steps=steps)

        # Blend the model's readiness with a deterministic floor from the actual inputs.
        floor = _heuristic_readiness(profile)
        try:
            model_score = int(data.get("readiness_percent", floor))
        except (TypeError, ValueError):
            model_score = floor
        data["readiness_percent"] = max(5, min(round((model_score + floor) / 2), 98))

        steps.append(ReasoningStep(
            f"Verdict: {data.get('eligibility_verdict', 'assessed')} · readiness {data['readiness_percent']}%",
            kind="decide",
        ))
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
