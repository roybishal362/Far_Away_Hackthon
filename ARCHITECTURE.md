# 🌉 Kakehashi — Architecture & Build Blueprint

**One-liner:** An autonomous multi-agent system that guides Indian skilled workers through
Japan's *Specified Skilled Worker (SSW)* migration — grounded in **real** official data,
with **proof** that its guidance is correct and not hallucinated.

**Theme:** Agentic & Autonomous Systems · **Impact:** serves the signed Aug-2025 India–Japan
Human Resource Exchange Partnership (helps *both* governments) · **Edge:** everything real + provable.

---

## 1. Design tenets (non-negotiable)
1. **Real or nothing** — every fact comes from a real API or a cited official document. We never fake data. If something can't be real in 7 days, we cut it or mark it roadmap.
2. **Provable** — every capability has a metric + visualization. Trust is *measured*, not claimed.
3. **UI-agnostic core** — all intelligence lives in pure-Python modules; the UI is a thin, swappable layer.
4. **Always submittable** — vertical slices; the app runs end-to-end every day.
5. **Private by design** — minimal PII, encrypted at rest, secrets never in code.

## 2. System layers (clean separation)
```
ui/            ← Streamlit presentation ONLY (swappable). No business logic here.
core/
  engine.py    ← orchestrates a run end-to-end; the single entrypoint the UI calls
  agents/      ← specialized agents (pure Python, framework-free)
  tools/       ← real-data clients (e-Stat, JSearch, Amadeus, SSW-RAG) behind one interface
  rag/         ← official-doc ingestion, retrieval, citation
  eval/        ← gold checklist + metrics + the proof charts
  security/    ← encryption, secrets, privacy helpers
config.py      ← settings + key loading (env / Streamlit secrets), graceful no-key behavior
```
**Contract:** the UI imports only `core.engine`. Swapping Streamlit → Next.js later touches nothing in `core/`.

## 3. The agents (multi-agent orchestration — real depth, not a wrapper)
| Agent | Input | Real tool it uses | Output |
|---|---|---|---|
| 🧭 **Orchestrator** | worker profile + goal | — (plans & routes) | ordered plan, delegates to agents, merges results |
| ✅ **Pathway** | skills, experience, language level | **SSW-RAG** (ssw.go.jp/MOFA) | eligible SSW sector(s) + exact requirements, **cited** |
| 📈 **Demand** | candidate sectors | **e-Stat API** (gov stats) | real labor-demand evidence per sector (charts) |
| 💼 **Jobs** | matched sector + location | **JSearch API** | real live job listings + apply links |
| 📄 **Procedure** | chosen pathway | **SSW-RAG** | step-by-step immigration checklist + drafted documents, cited |
| 📚 **Prep** | gaps (e.g. needs JLPT N4) | official test info (RAG) | personalized study/exam plan + timeline |
| 🗓️ **Journey** | origin, target city, date | **Amadeus API** | real flight options + cost/timeline estimate |

Each agent: (1) reasons with an LLM (Claude), (2) calls its **real** tool, (3) returns a result
**with citations** and a **confidence**. The Orchestrator composes them and a **human-in-the-loop**
checkpoint gates any consequential step.

## 4. Grounding & citations (the trust engine)
- Official SSW/MOFA pages + key PDFs are ingested into a local vector index (RAG).
- Agents answer **only** from retrieved passages and attach the source URL to each claim.
- A claim with no supporting source is flagged, not shown as fact. → feeds the metric below.

## 5. Proof / evaluation (the "math", engineered not lazy)
- **Gold checklist**: a hand-curated set of true SSW facts/steps per sector (from official sources).
- **Source-Grounding Score** 🆕: % of agent claims backed by a valid official citation.
- **Procedure accuracy**: precision / recall vs the gold checklist.
- **Hallucination ablation**: error rate **with vs without** RAG grounding → bar chart proving the engineering matters.
- **Readiness Score** 🆕: composite of the worker's fit vs requirements (+ gap analysis).
- All rendered on an **Evaluation dashboard** tab with charts.

## 6. Security & privacy (real, MVP-scoped)
- Secrets via `st.secrets` / env — **never** committed. (`.gitignore` enforces.)
- Any persisted profile encrypted with **Fernet (AES)**; default is session-only / no persistence.
- No PII in logs; data-minimization; TLS in transit (Streamlit Cloud).
- A **Privacy panel** in the app explains the model. *(Enterprise KMS/audit = Round 2/3.)*

## 7. Product enhancements (make it a product, not a demo)
- Live **agent-reasoning timeline** · **citation-per-claim** · **Migration Dossier PDF export**
- **Multilingual** output (EN/HI/JA) · **cost + timeline estimator** · **human-in-the-loop approval**

## 8. External keys required (user registers — all free tiers)
| Key | Where | Cost |
|---|---|---|
| **Anthropic (Claude) API** | console.anthropic.com | pay-as-you-go (cheap) |
| **e-Stat API** | e-stat.go.jp/api (register) | free |
| **JSearch** | rapidapi.com → JSearch | free tier |
| **Amadeus** | developers.amadeus.com | free 2,000 calls/mo |

The app degrades **honestly** without a key (shows "configure key", never fakes data).

## 9. Build order (vertical slices)
**Core (Days 1–4):** config → SSW-RAG + Pathway → Jobs (JSearch) → Procedure checklist+doc → eval dashboard → polished UI shell.
**Stretch (Days 5–7):** Demand (e-Stat) viz → Journey (Amadeus) → Prep plan → encryption + privacy panel → PDF/multilingual → demo polish + pitch.
