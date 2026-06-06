"""Resume -> profile auto-fill. Extracts profile fields from resume text via the LLM."""
from __future__ import annotations

from core.llm import get_llm

SYSTEM = (
    "Extract a worker profile from this resume text for a Japan SSW assistant. "
    "Return JSON with keys: skills (short phrase), sector_interest (best-matching SSW sector name, "
    "or 'Software / IT / Engineering' if it's a tech role), years_experience (number), "
    "japanese_level (one of: none, JFT-Basic, N5, N4, N3 or higher), education (short). "
    "Infer sensibly; if unknown use defaults (years_experience 0, japanese_level 'none')."
)


def extract(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {}
    try:
        data = get_llm().json(SYSTEM, text[:6000], temperature=0.1)
    except Exception:
        return {}
    # keep only known keys
    keys = {"skills", "sector_interest", "years_experience", "japanese_level", "education"}
    return {k: v for k, v in data.items() if k in keys}
