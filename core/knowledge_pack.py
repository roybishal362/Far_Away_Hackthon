"""Curated, real SSW content (researched + verified URLs). Agents/UI use this
directly so links are REAL, never hallucinated by the LLM.

Source: official ISA (ssw.go.jp / moj.go.jp), MOFA, Japan Foundation, Prometric,
JAC, NCA, Pearson VUE. See ARCHITECTURE.md / research pack.
"""
from __future__ import annotations

# --- The current SSW(i) industry fields (2025-2026, post-2024 expansion) ---
SECTORS: list[dict] = [
    {"name": "Nursing Care", "ja": "介護", "desc": "Physical care & support at care facilities (excludes home-visit care)."},
    {"name": "Building Cleaning Management", "ja": "ビルクリーニング", "desc": "Interior cleaning of hotels, offices, hospitals."},
    {"name": "Industrial Product Manufacturing", "ja": "工業製品製造業", "desc": "Machining, welding, plating, molding, assembly (merged field)."},
    {"name": "Construction", "ja": "建設", "desc": "Formwork, rebar, plumbing, plastering, earthwork, finishing."},
    {"name": "Shipbuilding & Ship Machinery", "ja": "造船・舶用工業", "desc": "Welding, machining, painting, fitting for ships."},
    {"name": "Automobile Repair & Maintenance", "ja": "自動車整備", "desc": "Inspection and disassembly maintenance of vehicles."},
    {"name": "Aviation", "ja": "航空", "desc": "Airport ground handling and aircraft maintenance."},
    {"name": "Accommodation (Hotel/Ryokan)", "ja": "宿泊", "desc": "Front desk, guest service, restaurant service."},
    {"name": "Road Transport (Driver)", "ja": "自動車運送業", "desc": "Truck/bus/taxi (bus & taxi need a Japanese Class-2 licence). Added Dec 2024."},
    {"name": "Railway", "ja": "鉄道", "desc": "Track/signal maintenance, rolling-stock, station service, driving. Added 2024."},
    {"name": "Agriculture", "ja": "農業", "desc": "Crop cultivation and livestock husbandry."},
    {"name": "Fishery & Aquaculture", "ja": "漁業", "desc": "Fishing operations and fish/shellfish farming."},
    {"name": "Food & Beverage Manufacturing", "ja": "飲食料品製造業", "desc": "Food/drink production, processing, hygiene (excludes liquor)."},
    {"name": "Food Service / Restaurant", "ja": "外食業", "desc": "Food prep, customer service, store management."},
    {"name": "Forestry", "ja": "林業", "desc": "Planting, thinning, logging. Added 2024."},
    {"name": "Wood Industry", "ja": "木材産業", "desc": "Sawn lumber, plywood, wood processing. Added 2024."},
    {"name": "Resource Circulation / Recycling", "ja": "資源循環", "desc": "Waste collection, sorting, recycling. New field."},
    {"name": "Linen Supply", "ja": "リネンサプライ", "desc": "Industrial laundry/linen rental services. New field."},
    {"name": "Logistics & Warehousing", "ja": "倉庫・物流", "desc": "Receiving, picking, packing, dispatch. New field."},
]

# Non-SSW route surfaced explicitly so IT/engineering candidates aren't misled.
NON_SSW_IT = {
    "name": "Software / IT / Engineering",
    "verdict": "Not an SSW field — use the Engineer visa",
    "detail": (
        "Software/IT/engineering roles are NOT covered by SSW. The correct status is "
        "'Engineer/Specialist in Humanities/International Services' (技術・人文知識・国際業務 / 'Gijinkoku'), "
        "the standard work visa for software/system engineers, programmers, data scientists, etc. "
        "Requires a relevant bachelor's degree (or ~10 yrs experience, or a Japan-recognised IT qualification), "
        "an employer contract, and equal pay. High earners can target the points-based 'Highly Skilled Professional' "
        "status for faster permanent residence."
    ),
    "resources": [
        {"name": "ISA — Engineer/Specialist in Humanities/International Services", "url": "https://www.moj.go.jp/isa/applications/status/gijinkoku.html", "purpose": "Official status-of-residence page for the IT/engineering work visa."},
        {"name": "ISA — Highly Skilled Professional", "url": "https://www.moj.go.jp/isa/applications/status/hsp_index.html", "purpose": "Points-based status for high-end talent (faster PR)."},
    ],
}

IT_KEYWORDS = ["it", "software", "developer", "programmer", "engineer", "data scien", "web", "tech", "coding", "computer"]

# --- The ordered overseas (India -> Japan) SSW journey with REAL links ---
PROCEDURE_STEPS: list[dict] = [
    {
        "step": "Orientation — understand SSW and pick a sector",
        "detail": "Confirm eligibility and choose one designated field. SSW(i) = up to 5 years, equal pay to Japanese workers, no family accompaniment. Two prerequisites: (a) a Japanese-language test AND (b) the sector skills test. For Indian candidates, using a sending organization is OPTIONAL — you may apply directly.",
        "resources": [
            {"name": "ISA — Steps to Working in Japan", "url": "https://www.ssw.go.jp/en/about/step/", "purpose": "Official ordered flow for overseas SSW candidates."},
            {"name": "ISA — What is the SSW status", "url": "https://www.ssw.go.jp/en/about/visa/", "purpose": "SSW(i) vs (ii), fields, 5-year limit, equal-pay & no-family rules."},
        ],
    },
    {
        "step": "Pass a Japanese-language test (JFT-Basic or JLPT N4+)",
        "detail": "Prove ~A2/N4 Japanese. Option A: JFT-Basic (CBT, pass 200/250), offered in India via Prometric. Option B: JLPT N4 or higher (held in India in July/December). Nursing care additionally needs the Nursing Care Japanese Language Evaluation Test.",
        "resources": [
            {"name": "JFT-Basic official (Japan Foundation)", "url": "https://www.jpf.go.jp/jft-basic/e/index.html", "purpose": "What JFT-Basic is, level, sections, pass mark."},
            {"name": "Prometric — JFT-Basic for India", "url": "https://ac.prometric-jp.com/testlist/jfe/jftbasic_india.html", "purpose": "India test centres & booking for JFT-Basic."},
            {"name": "JLPT — Taking the Test Overseas", "url": "https://www.jlpt.jp/e/application/overseas_index.html", "purpose": "Apply for JLPT N4+ in India (Jul/Dec)."},
        ],
    },
    {
        "step": "Pass the sector skills evaluation test",
        "detail": "Pass the Specified Skill Evaluation Test for your field, proving you can work immediately. Most fields go through Prometric (same ID/flow as JFT-Basic); some via a sector body (Agriculture→NCA/ASAT, Construction→JAC, Building Cleaning→Pearson VUE). You need BOTH a passing language AND skills result before the employer step.",
        "resources": [
            {"name": "Prometric — SSW Test List (all fields)", "url": "https://www.prometric-jp.com/en/ssw/test_list/", "purpose": "Every Prometric-administered skills test by field."},
            {"name": "Prometric — create your testing ID", "url": "https://www.prometric-jp.com/en/ssw/exam/id/", "purpose": "Make the Prometric ID (passport needed) for any booking."},
        ],
    },
    {
        "step": "Find an accepting employer",
        "detail": "With both tests passed, find a Japanese 'Accepting Organization'. Indian candidates may search directly. Channels: the ISA support hub, JAC's FREE construction job-matching, Hello Work (government placement with foreigner centres), and job fairs. Then pass an interview (often online).",
        "resources": [
            {"name": "ISA Support Website (SSW hub)", "url": "https://www.ssw.go.jp/en/", "purpose": "Program info + job-search resources."},
            {"name": "JAC — Free Job Matching (construction)", "url": "https://ssw.jac-skill.or.jp/en/job-matching/", "purpose": "Free construction job-matching (no fees)."},
            {"name": "Hello Work (public placement)", "url": "https://www.hellowork.mhlw.go.jp/", "purpose": "Japan's free government job placement."},
        ],
    },
    {
        "step": "Sign the contract + pre-departure orientation & health check",
        "detail": "Sign an SSW-compliant contract (equal pay, proper conditions). The employer prepares a 'Support Plan' (in-house or via a Registered Support Organization), gives pre-departure orientation on work/life/immigration rules, and you complete a medical checkup.",
        "resources": [
            {"name": "ISA — How to obtain the SSW status", "url": "https://www.ssw.go.jp/en/about/sswv/", "purpose": "Contract, support plan, and pre-employment obligations."},
            {"name": "ISA — Required Documents", "url": "https://www.ssw.go.jp/en/about/apply/", "purpose": "Documents the employer/applicant must prepare."},
        ],
    },
    {
        "step": "Get the Certificate of Eligibility (CoE), then the visa",
        "detail": "Your employer applies to the ISA for a Certificate of Eligibility (1-3 months). Once issued, apply for the SSW visa at the Embassy of Japan in India with the CoE, passport, and forms. On arrival you receive a Residence Card and on-the-job support begins.",
        "resources": [
            {"name": "ISA — Immigration Services Agency (home)", "url": "https://www.moj.go.jp/isa/index.html", "purpose": "Receives the CoE application and grants the status."},
            {"name": "Embassy of Japan in India — Visa", "url": "https://www.in.emb-japan.go.jp/itpr_en/visa.html", "purpose": "Where Indian candidates submit the SSW visa with the CoE."},
        ],
    },
]

# --- Free / open-source study resources (real URLs) ---
STUDY_RESOURCES: list[dict] = [
    {"name": "Irodori: Japanese for Life in Japan (free coursebooks + audio)", "url": "https://www.irodori.jpf.go.jp/", "purpose": "Japan Foundation's flagship FREE coursebook, recommended for JFT-Basic. Full PDFs + 1,100+ audio.", "level": "A1-A2 (N5-N4)"},
    {"name": "JFT-Basic 'Hint for Learning' (free e-learning hub)", "url": "https://www.jpf.go.jp/jft-basic/e/support/index.html", "purpose": "Official hub of FREE JFT-Basic study materials.", "level": "JFT"},
    {"name": "JFT-Basic sample questions", "url": "https://www.jpf.go.jp/jft-basic/sample/q01.html", "purpose": "Free official samples mirroring the real CBT format.", "level": "JFT"},
    {"name": "JLPT official sample questions", "url": "https://www.jlpt.jp/e/samples/forlearners.html", "purpose": "Free official N4 question formats (and N1-N3).", "level": "N5-N4"},
    {"name": "Marugoto (free downloadable materials)", "url": "https://marugoto.jpf.go.jp/en/download/", "purpose": "Vocab indexes, can-do checks, kanji lists — grammar/vocab reinforcement.", "level": "A1-B1"},
    {"name": "NHK News Web Easy", "url": "https://www3.nhk.or.jp/news/easy/", "purpose": "Free simplified news with furigana + audio — daily reading/listening.", "level": "N4-N3"},
    {"name": "Tae Kim's Guide to Japanese Grammar", "url": "https://guidetojapanese.org/learn/grammar", "purpose": "Free, well-regarded grammar guide (CC-licensed).", "level": "N5-N4"},
    {"name": "Anki (open-source SRS flashcards)", "url": "https://apps.ankiweb.net/", "purpose": "Free spaced-repetition for vocab/kanji; free N4/JFT community decks.", "level": "all"},
]

# --- Sector skills tests: who administers + where to register (real URLs) ---
SKILLS_TESTS: list[dict] = [
    {"sector": "Nursing Care", "test_name": "Nursing Care Skills Evaluation Test (+ Nursing Care Japanese test)", "administrator": "Prometric (for MHLW)", "register_url": "https://www.prometric-jp.com/en/ssw/test_list/archives/2"},
    {"sector": "Food Service", "test_name": "Food Service Industry SSW(i) Test", "administrator": "OTAFF via Prometric", "register_url": "https://www.prometric-jp.com/en/ssw/test_list/archives/4"},
    {"sector": "Agriculture", "test_name": "Agriculture Skill Assessment Test (ASAT)", "administrator": "National Chamber of Agriculture (NCA)", "register_url": "https://asat-nca.jp/en/flow/index/"},
    {"sector": "Construction", "test_name": "Construction Field Specified Skills Evaluation Exam", "administrator": "JAC (delivered at Prometric centres)", "register_url": "https://ssw.jac-skill.or.jp/en/"},
    {"sector": "Building Cleaning", "test_name": "Building Cleaning Management SSW(i) Test", "administrator": "J-BMA via Pearson VUE", "register_url": "https://www.pearsonvue.com/us/en/jbma.html"},
    {"sector": "Accommodation", "test_name": "Accommodation Industry Evaluation Test", "administrator": "Center for Accommodation Industry Proficiency Test via Prometric", "register_url": "https://www.prometric-jp.com/en/ssw/test_list/archives/12"},
]


def is_it_sector(text: str) -> bool:
    t = (text or "").lower()
    return any(k in t for k in IT_KEYWORDS)


def skills_test_for(sector: str) -> dict | None:
    s = (sector or "").lower()
    for t in SKILLS_TESTS:
        if t["sector"].lower().split()[0] in s or s.split("/")[0].strip() in t["sector"].lower():
            return t
    return None
