<div align="center">

# 🌉 Kakehashi (架け橋)

### An autonomous AI bridge for Indian workers to Japan

**FAR AWAY 2026 · Theme: Agentic & Autonomous Systems**

*A source-grounded multi-agent system that guides Indian skilled workers through Japan's
Specified Skilled Worker (SSW) journey — every answer cited from official sources, every claim measured.*

`Real data, not mockups` · `Cited, not hallucinated` · `Proven, not claimed` · `EN / हिन्दी / 日本語`

</div>

---

## 🎯 The problem (why we built this)

In **August 2025**, India and Japan signed a Human Resource Exchange Partnership to move **50,000 skilled
Indian workers** to Japan — which faces a severe labour shortage (300,000+ caregivers short by 2035). Both
governments named **AI talent mobility** and **trustworthy AI** as the way to make it happen.

But for an actual worker, the journey is a months-long maze: *Which visa? Am I even eligible? The JLPT N4
language bar, sector skills tests, immigration paperwork, finding a real employer, the cost, the relocation…*
The information is scattered across Japanese government sites, and the gap is filled by middlemen and
misinformation.

**Kakehashi is the autonomous guide through that maze — serving both governments at once:** India sends
workers, Japan fills its shortage, and the worker gets a cited, personalized, honest plan.

## 🌉 What it does

You tell Kakehashi about yourself (or upload your resume). A team of **autonomous agents** then:
- determines the **right visa pathway** for *you* (and correctly reroutes IT/office roles off SSW),
- pulls **real live jobs** in Japan and ranks them by fit,
- lays out the **official step-by-step procedure** with the real government link for every step,
- builds a **personalized study plan** with free resources,
- estimates **salary and cost**, and
- answers your **follow-up questions** in a grounded chat — in your language.

…then you can **save, share, or download** the whole thing as a PDF "Migration Dossier."

## ✨ Why it's different — three pillars

1. **Real or nothing.** Every tool returns real data or *honestly says it's not configured* — it physically
   cannot fabricate. Jobs are real live listings; SSW rules are grounded in official `ssw.go.jp` / MOFA pages
   with a citation on every claim.
2. **Proven, not claimed.** A built-in ablation measures our grounded agents vs. a plain LLM:
   **accuracy ≈14% → ≈71%, hallucinations ≈6 → 0** against a gold set of official facts. The proof is a number.
3. **Genuinely autonomous.** 6 specialized agents reason → call a real tool → cite → score confidence, and the
   orchestrator **adapts the plan to you** (e.g. an IT worker is routed to the Engineer visa and the SSW-only
   steps are skipped automatically). Most "agentic" demos are a single prompt wrapper — this isn't.

## 🧠 Architecture

```
frontend/ (Next.js 14 · TS · Tailwind · Framer Motion)    ← multi-page product (Home / How / App)
   └── talks to ─▶ FastAPI (api/) ── SSE live agent timeline
core/  (UI-agnostic Python brain)
  engine.py     orchestrates agents, adapts the plan, computes the grounding score
  agents/       pathway · jobs · procedure · prep · journey · synthesis
  tools/        real-data clients: jobs (JSearch), e-Stat (gov stats), flights (Amadeus)
  rag/          official SSW facts, BM25-retrieved, every passage cited
  eval/         gold checklist + grounded-vs-ungrounded ablation (the proof)
  chat.py       grounded follow-up Q&A   ·   security/  AES-Fernet encryption
config.py       loads keys from env/secrets; honest no-key degradation
```

| Agent | What it does | Real tool |
|---|---|---|
| 🧭 **Pathway** | Classifies the correct visa (SSW / Engineer / Specialist) + a personalized verdict, readiness score & gaps | SSW-RAG (cited) |
| 💼 **Jobs** | Fetches real live openings, ranks each by fit to you | JSearch API |
| 📄 **Procedure** | The official ordered journey, each step with the real gov link | SSW-RAG |
| 📚 **Prep** | A study + exam plan keyed to your Japanese level + free resources | official test info |
| 🗓️ **Journey** | Flights, cost & timeline | Amadeus (roadmap) |
| ✨ **Synthesis** | Your warm personal overview + salary + cost | gov salary data |

## 📊 The proof (Proof tab)

`POST /eval` runs the same question two ways and scores both against a gold set of official SSW facts:

| | Accuracy | Hallucinations |
|---|---|---|
| **Our grounded agents** | ≈ 71% | **0** |
| Plain LLM (ungrounded) | ≈ 14% | 6 |

*Grounding takes accuracy 14% → 71% and cuts hallucinations to zero. That gap is the evidence.*

## 🔌 Real data sources

| Need | Source | Type |
|---|---|---|
| SSW rules & procedures | Official **ssw.go.jp** (ISA) + **MOFA** | grounded & cited (RAG) |
| Live job openings | **JSearch** (real-time) | REST API |
| Government labour statistics | **Japan e-Stat** | official gov API |
| Exam fees / salaries | Prometric, JLPT, JFT + sourced research | cited |
| Flights | **Amadeus** | API (roadmap) |

## 🖥️ The product

A real multi-page site: **Home** (the story + impact), **How it works** (the agentic depth, for judges),
and **Build my plan** (the tool) with tabs for **Overview · Pathway · Jobs · Procedure · Study plan ·
Journey · Proof · Ask AI**, plus persona quick-starts, resume auto-fill, save/share links, PDF export,
a progress checklist, and a privacy panel.

## 🌐 Multilingual · 🔐 Private by design
- Content **and** chat in **English / हिन्दी / 日本語** (the finale is in Japan 🇯🇵).
- Real or nothing · AES-Fernet encryption at rest · no PII in logs · disclaimer (not legal advice).

## 🗺️ Real vs. roadmap (we're honest about both)
| Live now | Roadmap |
|---|---|
| Pathway, Jobs (real), Procedure, Prep, Synthesis, Chat, Proof, save/share, PDF, EN/HI/JA | Amadeus flights (paid tier), e-Stat "Demand" charts, recruiter-scam detection |

## 🛠️ Tech stack
**Frontend:** Next.js 14, TypeScript, Tailwind, Framer Motion, Recharts ·
**Backend:** FastAPI, SSE · **LLM:** Groq `gpt-oss-120b` (multilingual) ·
**RAG:** BM25 · **Security:** cryptography (Fernet)

## ▶️ Run locally
> Windows: use `py` (the launcher), not `python`.

**Backend** (Python 3.12+):
```bash
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# create .env (see .env keys below), then:
.\.venv\Scripts\python.exe -m uvicorn api.main:app --reload --port 8000
```
**Frontend** (Node 18+):
```bash
cd frontend && npm install
copy .env.local.example .env.local   # NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev      # http://localhost:3000
```
**`.env` keys** (free): `GROQ_API_KEY` (console.groq.com) · `JSEARCH_API_KEY` (OpenWeb Ninja) ·
`ESTAT_APP_ID` (e-stat.go.jp). The app degrades honestly without any key.

## 📜 More
[ARCHITECTURE.md](ARCHITECTURE.md) · [DEPLOY.md](DEPLOY.md) · smoke tests in `scripts/`.

<div align="center">

**Kakehashi 架け橋 — a bridge between India and Japan.**
Built for FAR AWAY 2026 · Agentic & Autonomous Systems

</div>
