"""Shared helpers for grounded agent reasoning (retrieve -> reason -> cite)."""
from __future__ import annotations

from core.rag.index import Passage, get_retriever
from core.types import Citation, WorkerProfile


LANG_NAMES = {"en": "English", "hi": "Hindi", "ja": "Japanese"}


def lang_directive(p: WorkerProfile) -> str:
    """Tell the LLM to localize human-readable text values (schema keys stay English)."""
    name = LANG_NAMES.get(getattr(p, "lang", "en"), "English")
    if name == "English":
        return ""
    return f"\nIMPORTANT: Write ALL human-readable text VALUES in {name}. Keep JSON keys in English."


def profile_text(p: WorkerProfile) -> str:
    base = (
        f"Skills/experience: {p.skills or 'unspecified'}; years: {p.years_experience}; "
        f"sector interest: {p.sector_interest or 'open'}; Japanese level: {p.japanese_level}; "
        f"education: {p.education or 'unspecified'}; route: {p.origin_city} -> {p.target_city}."
    )
    resume = getattr(p, "resume_text", "") or ""
    if resume.strip():
        base += f"\n\nRESUME (use these real details to personalize):\n{resume[:1500]}"
    return base


def gather(query: str, k: int = 5) -> tuple[list[Passage], str]:
    """Retrieve official passages and render a numbered, source-tagged context block."""
    passages = get_retriever().retrieve(query, k)
    ctx = "\n".join(
        f"[{i + 1}] {p.text} (source: {p.citation.title})" for i, p in enumerate(passages)
    )
    return passages, ctx


def used_citations(passages: list[Passage], indices) -> list[Citation]:
    """Map the LLM's cited context indices back to real Citations.

    Falls back to citing every retrieved passage if the model didn't specify —
    so a grounded answer is never shown as uncited.
    """
    cits: list[Citation] = []
    for idx in indices or []:
        try:
            i = int(idx)
        except (TypeError, ValueError):
            continue
        if 1 <= i <= len(passages):
            cits.append(passages[i - 1].citation)
    return cits or [p.citation for p in passages]
