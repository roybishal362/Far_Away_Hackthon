"""Curated, citation-bearing knowledge base of REAL SSW facts.

Every entry carries the official source URL it came from. Agents answer ONLY from
retrieved entries and attach the citation - that is what we measure with the
Source-Grounding Score. This same set seeds the evaluation gold-standard.

IMPORTANT (honesty): these are seeded from official sources (ssw.go.jp, MOFA, ISA).
Before the final submission, verify/expand each against the live official page -
they are pinned here for reliable retrieval, not as a substitute for the source.
"""
from __future__ import annotations

SSW_OFFICIAL = "https://www.ssw.go.jp/en/"
MOFA_SSW = "https://www.mofa.go.jp/mofaj/ca/fna/ssw/us/overview/"
ISA_SSW = "https://www.ssw.go.jp/en/about/visa/"
JAC_JOBS = "https://ssw.jac-skill.or.jp/en/job-matching/recruit-list.php"

# Each fact: (text, source_url, source_title, tags)
FACTS: list[dict] = [
    {
        "text": "The Specified Skilled Worker (SSW) status of residence was established in April 2019 to accept foreign workers with skills in designated industrial fields facing labor shortages.",
        "source_url": MOFA_SSW, "title": "MOFA - What is the SSW?", "tags": ["overview", "history"],
    },
    {
        "text": "SSW has two types: Specified Skilled Worker (i) [SSW-1] and Specified Skilled Worker (ii) [SSW-2].",
        "source_url": ISA_SSW, "title": "ISA - SSW status of residence", "tags": ["types"],
    },
    {
        "text": "An SSW-1 applicant must be at least 18 years old, in good health, and have the occupational skills and Japanese language ability to work immediately without special training.",
        "source_url": MOFA_SSW, "title": "MOFA - SSW-1 requirements", "tags": ["ssw1", "eligibility", "age"],
    },
    {
        "text": "SSW-1 requires passing a sector-specific skills evaluation test and a Japanese language test (JLPT N4 or JFT-Basic or higher).",
        "source_url": MOFA_SSW, "title": "MOFA - SSW-1 tests", "tags": ["ssw1", "tests", "language", "jlpt"],
    },
    {
        "text": "Under SSW-1 a worker may stay in Japan for a total of up to five years and cannot bring family members.",
        "source_url": MOFA_SSW, "title": "MOFA - SSW-1 duration", "tags": ["ssw1", "duration", "family"],
    },
    {
        "text": "SSW-2 has no upper limit on length of stay and allows the worker to bring family members; it requires a more advanced industry skills test.",
        "source_url": ISA_SSW, "title": "ISA - SSW-2 conditions", "tags": ["ssw2", "duration", "family"],
    },
    {
        "text": "As of 2026 the SSW-1 visa covers 19 industry fields, expanded by the government to address workforce shortages including transportation and primary industries.",
        "source_url": SSW_OFFICIAL, "title": "ISA - SSW sectors (2026)", "tags": ["sectors", "2026"],
    },
    {
        "text": "Eligible SSW sectors include caregiving/nursing care, food & beverage manufacturing, agriculture, construction, industrial machinery, automobile maintenance, shipbuilding, accommodation, and aviation, among others.",
        "source_url": SSW_OFFICIAL, "title": "ISA - SSW eligible sectors", "tags": ["sectors", "caregiving", "agriculture", "construction"],
    },
    {
        "text": "New overseas SSW-1 applications for the restaurant/food-service sector were suspended around April 13, 2026, as the sector's five-year cap (from April 2024) is being reached.",
        "source_url": SSW_OFFICIAL, "title": "ISA - restaurant sector suspension 2026", "tags": ["sectors", "restaurant", "2026", "suspension"],
    },
    {
        "text": "Hello Work is Japan's nationwide public employment service (Ministry of Health, Labour and Welfare) offering free job listings and support to work-eligible residents including SSW visa holders.",
        "source_url": "https://www.ssw.go.jp/en/", "title": "ISA - Hello Work / job matching", "tags": ["jobs", "hellowork"],
    },
    {
        "text": "Official SSW job-matching listings are published via JAC (Japan Association for Construction Human Resources) and the ISA support website, including overseas job-matching events.",
        "source_url": JAC_JOBS, "title": "JAC - SSW job matching list", "tags": ["jobs", "matching"],
    },
    {
        "text": "Japan and India signed a Memorandum of Cooperation on the SSW partnership; under the August 2025 Human Resource Exchange Partnership the two countries aim to move 50,000 skilled Indian workers to Japan over five years.",
        "source_url": "https://www.pmindia.gov.in/en/news_updates/action-plan-for-india-japan-human-resource-exchange-and-cooperation/",
        "title": "PM India - India-Japan HR Exchange Action Plan", "tags": ["india", "partnership", "2025"],
    },
    {
        "text": "Japan faces a severe caregiver shortage, officially estimated at more than 300,000 caregivers by 2035, a key driver of foreign-worker acceptance.",
        "source_url": "https://www.preventionweb.net/news/japans-aging-population-will-increase-disaster-vulnerability",
        "title": "Japan aging & labor shortage", "tags": ["caregiving", "demand", "aging"],
    },
]
