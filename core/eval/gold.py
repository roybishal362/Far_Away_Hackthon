"""Gold-standard SSW facts — curated from official sources (ssw.go.jp / MOFA / Japan Foundation).

These are checkable ground-truth claims. We measure whether an answer covers them
correctly (accuracy) and whether it states anything that contradicts them
(hallucination). Each maps to a knowledge-base entry in core/rag/knowledge.py,
which carries the official source URL.

HONESTY NOTE: verify each fact against the live official page before final
submission — rules can change; the gold set must track the source, not memory.
"""
from __future__ import annotations

GOLD: list[str] = [
    # Eligibility & tests
    "SSW-1 applicants must be at least 18 years old.",
    "SSW-1 requires a Japanese-language test such as JLPT N4 or JFT-Basic.",
    "SSW-1 requires passing a sector-specific skills evaluation test.",
    "The caregiving sector requires an additional nursing-care Japanese language evaluation test on top of the general language requirement.",
    "The JFT-Basic is a computer-based Japanese test held overseas in designated countries, including India.",
    "JLPT N4 certifies the ability to understand basic Japanese.",
    "SSW skills tests are conducted both in Japan and overseas in designated countries.",
    "Workers who successfully completed Technical Intern Training (ii) are exempt from the skills and Japanese tests when moving to SSW-1 in the corresponding field.",
    # Duration & family
    "Under SSW-1 the maximum total stay in Japan is five years.",
    "SSW-1 status is granted in renewable increments of 1 year, 6 months, or 4 months.",
    "SSW-1 holders cannot bring family members to Japan.",
    "SSW-2 has no upper limit on length of stay and allows bringing family.",
    # Program structure
    "The SSW status of residence was established in April 2019.",
    "SSW has two types: SSW-1 and SSW-2.",
    "Caregiving / nursing care is an eligible SSW sector.",
    # Worker rights & protections (the anti-scam core)
    "An SSW worker must be paid equal to or more than a Japanese national doing comparable work.",
    "SSW rules prohibit security deposits and penalty-clause contracts; workers must not pay deposits to intermediaries.",
    "Organizations accepting SSW-1 workers must provide a support plan (orientation, housing help, Japanese learning, consultations) or entrust it to a Registered Support Organization.",
    "SSW workers may change employers within the same industry field.",
    # Process
    "After passing the tests and signing a contract, the accepting organization applies for a Certificate of Eligibility (COE) before the worker applies for the visa at a Japanese embassy or consulate.",
    # India corridor
    "Japan and India signed a Memorandum of Cooperation on SSW that targets the elimination of malicious intermediary organizations.",
    "Under the August 2025 India-Japan Human Resource Exchange Action Plan, the two countries target 50,000 skilled Indian workers moving to Japan over five years.",
]
