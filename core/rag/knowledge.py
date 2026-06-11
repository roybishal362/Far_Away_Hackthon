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
        "text": "Japan faces a severe care-worker shortage: the Ministry of Health, Labour and Welfare (MHLW) projects a shortfall of about 570,000 care workers by 2040 (9th Long-Term Care Insurance Business Plan), a key driver of foreign-worker acceptance.",
        "source_url": "https://isvd.or.jp/en/columns/2026-03-09-care-worker-shortage-structure",
        "title": "MHLW - care-worker shortage (570k by 2040)", "tags": ["caregiving", "demand", "aging"],
    },
    {
        "text": "The Japan-India Memorandum of Cooperation on Specified Skilled Workers (signed 18 Jan 2021) states its purpose includes 'the elimination of malicious intermediary organizations' - the scam-middleman problem is acknowledged by the governments themselves.",
        "source_url": "https://www.mofa.go.jp/press/release/press6e_000266.html",
        "title": "MOFA - Japan-India SSW MoC (eliminate malicious intermediaries)", "tags": ["india", "partnership", "scams", "intermediaries"],
    },
    {
        "text": "SSW-1 status is granted in renewable increments of 1 year, 6 months, or 4 months, up to the total maximum stay of five years.",
        "source_url": ISA_SSW, "title": "ISA - SSW-1 period of stay", "tags": ["ssw1", "duration", "renewal"],
    },
    {
        "text": "SSW-2 status is granted in renewable increments of 3 years, 1 year, or 6 months, with no cap on the total period of stay.",
        "source_url": ISA_SSW, "title": "ISA - SSW-2 period of stay", "tags": ["ssw2", "duration", "renewal"],
    },
    {
        "text": "Organizations accepting SSW-1 workers must provide a formal support plan - including pre-arrival orientation, help securing housing, daily-life orientation, opportunities to learn Japanese, and handling of consultations/complaints - or entrust this support to a government-registered Registered Support Organization.",
        "source_url": SSW_OFFICIAL, "title": "ISA - SSW-1 support plan & Registered Support Organizations", "tags": ["ssw1", "support", "accepting-organization", "rights"],
    },
    {
        "text": "An SSW worker's remuneration must be equal to or greater than that of a Japanese national performing comparable work.",
        "source_url": MOFA_SSW, "title": "MOFA - SSW equal-pay requirement", "tags": ["salary", "rights", "equal-pay"],
    },
    {
        "text": "SSW rules prohibit security deposits and penalty-clause contracts: a worker who has paid a deposit ('hoshokin') to a sending/intermediary organization, or whose contract imposes penalties for quitting, does not meet the acceptance conditions. Workers should never pay such deposits.",
        "source_url": SSW_OFFICIAL, "title": "ISA - no deposits / no penalty contracts", "tags": ["scams", "rights", "deposits", "intermediaries"],
    },
    {
        "text": "Foreign nationals who successfully completed Technical Intern Training (ii) (3 years of TITP) are exempt from both the skills test and the Japanese-language test when moving to SSW-1 in the corresponding field.",
        "source_url": MOFA_SSW, "title": "MOFA - TITP(ii) completers' test exemption", "tags": ["titp", "exemption", "tests"],
    },
    {
        "text": "The JFT-Basic (Japan Foundation Test for Basic Japanese) is a computer-based test measuring everyday-life Japanese (roughly CEFR A2), conducted by the Japan Foundation and held overseas in designated countries including India.",
        "source_url": "https://www.jpf.go.jp/jft-basic/e/", "title": "Japan Foundation - JFT-Basic", "tags": ["jft", "language", "tests", "india"],
    },
    {
        "text": "The JLPT (Japanese-Language Proficiency Test) has five levels N1 (hardest) to N5; N4 - the usual SSW language bar - certifies the ability to understand basic Japanese. It is held worldwide, typically twice a year.",
        "source_url": "https://www.jlpt.jp/e/", "title": "JLPT - levels & schedule", "tags": ["jlpt", "language", "tests"],
    },
    {
        "text": "For the caregiving/nursing-care sector, applicants must additionally pass the Nursing Care Japanese Language Evaluation Test on top of the general Japanese-language requirement.",
        "source_url": SSW_OFFICIAL, "title": "ISA - extra language test for nursing care", "tags": ["caregiving", "language", "tests"],
    },
    {
        "text": "SSW sector skills tests are conducted both in Japan and overseas in designated countries; test schedules and overseas venues are published by the sector bodies and the ISA.",
        "source_url": SSW_OFFICIAL, "title": "ISA - skills tests in Japan and overseas", "tags": ["tests", "skills", "overseas"],
    },
    {
        "text": "Typical from-abroad SSW flow: pass the skills and Japanese tests, sign an employment contract with a Japanese accepting organization, the organization applies to the Immigration Services Agency for a Certificate of Eligibility (COE), then the worker applies for the visa at a Japanese embassy/consulate with the COE and travels to Japan.",
        "source_url": ISA_SSW, "title": "ISA - application flow (tests -> contract -> COE -> visa)", "tags": ["procedure", "coe", "visa", "steps"],
    },
    {
        "text": "SSW workers may change employers within the same industry field (or across fields if they meet that field's test requirements), completing the required immigration procedures - the visa is not locked to one employer.",
        "source_url": ISA_SSW, "title": "ISA - job change within the same field", "tags": ["jobs", "rights", "job-change"],
    },
]
