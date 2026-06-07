# 🌉 Kakehashi — Architecture

> The shipped system. (An earlier draft of this file described a Streamlit/Anthropic prototype;
> this reflects what actually runs.)

## Design tenets
1. **Real or nothing** — every fact comes from a real API or a cited official document. Tools that lack a key
   return `ok=False` with a reason; they cannot fabricate.
2. **Proven** — capability is *measured* (grounded-vs-ungrounded ablation), not asserted.
3. **UI-agnostic core** — all intelligence is pure-Python in `core/`; the UI is a thin, swappable layer.
4. **Adaptive autonomy** — the orchestrator changes the plan per person (e.g. routes IT/office roles off SSW).
5. **Private by design** — minimal PII, encrypted at rest, secrets never in code.

## Layers
```
frontend/  Next.js 14 (App Router) · TypeScript · Tailwind · Framer Motion · Recharts
  app/         / (landing)  ·  /how (the agentic story)  ·  /app (the tool)
  components/  Nav, Hero, IntakeForm, AgentTimeline, Results (tabs), ProofDashboard, ...
  lib/         api client (SSE via fetch + manual parse), types
      │  HTTP + Server-Sent Events
      ▼
api/  FastAPI
  main.py   /run, /run/stream (SSE live timeline), /eval, /chat, /resume, /dossier, /save, /plan/{id}, /health
      │  calls only
      ▼
core/  (UI-agnostic Python brain)
  engine.py        orchestrates agents in order; ADAPTS (skips SSW-only agents on an off-SSW redirect);
                   computes the run-level Source-Grounding Score
  agents/          pathway · jobs · procedure · prep · journey · synthesis
                   (base.py defines the Agent contract: reason → call tool → cite → confidence + steps)
  tools/           real-data clients behind one interface: jobs (JSearch), estat (gov stats), flights (Amadeus)
  rag/             curated official SSW facts; BM25 retrieval; every passage carries a Citation
  eval/            gold checklist + grounded-vs-ungrounded ablation (the proof)
  chat.py          grounded follow-up Q&A over RAG + the knowledge pack
  knowledge_pack.py  sectors, procedure steps (real links), study resources, fees, salaries, visa routing
  security/        Fernet (AES) encryption-at-rest
config.py    loads keys from .env / env; honest no-key degradation
```

## Request flow (a run)
1. The `/app` page POSTs the `WorkerProfile` to `/run/stream`.
2. A worker thread runs `Engine().run(profile, on_step=…)`; each agent's reasoning `ReasoningStep`s are pushed
   onto a queue and streamed to the browser as **SSE** events → the live "Agents at work" timeline.
3. **Pathway** classifies the visa route (SSW / Engineer / Specialist). If off-SSW, the engine **skips** the
   SSW-only agents (procedure/prep/journey) and emits `skip` steps.
4. Remaining agents run, each returning data + **citations** + a confidence. **Synthesis** composes the overview.
5. A final `result` event delivers the structured `RunResult`; the UI renders the tabbed results.

## The agents
| Agent | Reasons about | Real tool | Output |
|---|---|---|---|
| 🧭 Pathway | eligibility for THIS person; correct visa | SSW-RAG | verdict, readiness %, gaps, sectors (cited) |
| 💼 Jobs | which real openings fit | JSearch | live listings ranked by fit % |
| 📄 Procedure | the official journey | SSW-RAG + knowledge pack | 6 steps, each with real gov links |
| 📚 Prep | language/skills gaps | official test info | study plan + free resources |
| 🗓️ Journey | relocation & cost | Amadeus | flights (roadmap) |
| ✨ Synthesis | the whole picture | gov salary data | overview + salary + cost |

## Grounding & proof
- Agents answer **only** from retrieved official passages and attach the source URL to each claim.
- `core/eval/harness.py` runs the same question **grounded** (our agents) vs **ungrounded** (plain LLM) and
  scores both against a gold set of official facts → accuracy + hallucination counts (the Proof tab).

## Security
- Secrets via env/`.env` (gitignored). `/plan/{id}` validates the id (`^[A-Za-z0-9_-]{6,24}$`) to block path
  traversal. Saved plans encrypted with Fernet when `FERNET_KEY` is set. No PII in logs.

## Tech
Next.js 14 · FastAPI · **Groq `gpt-oss-120b`** (multilingual) · BM25 (rank-bm25) · cryptography (Fernet) · Recharts.

## Real vs roadmap
**Live:** Pathway, Jobs (real), Procedure, Prep, Synthesis, Chat, Proof, save/share, PDF, EN/HI/JA, adaptive routing.
**Roadmap:** Amadeus flights (paid tier), e-Stat "Demand" charts, recruiter-scam detection.
