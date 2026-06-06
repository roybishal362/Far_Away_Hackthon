"""Gold-standard SSW facts — curated from official sources (ssw.go.jp / MOFA).

These are checkable ground-truth claims. We measure whether an agent's answer
covers them correctly (accuracy) and whether it states anything that contradicts
them (hallucination). Each maps to a knowledge-base citation.
"""
from __future__ import annotations

GOLD: list[str] = [
    "SSW-1 applicants must be at least 18 years old.",
    "SSW-1 requires a Japanese-language test such as JLPT N4 or JFT-Basic.",
    "SSW-1 requires passing a sector-specific skills evaluation test.",
    "Under SSW-1 the maximum total stay in Japan is five years.",
    "SSW-1 holders cannot bring family members to Japan.",
    "SSW-2 has no upper limit on length of stay and allows bringing family.",
    "Caregiving / nursing care is an eligible SSW sector.",
]
