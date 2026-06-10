# Independent verification brief — paste BOTH sections into Fable 5 (Claude.ai)

Paste the PROMPT first, then the BRIEFING below it, in one message.

---

## ▼ PART 1 — THE PROMPT (paste this)

You are a tough, experienced hackathon judge AND a senior technical mentor (12+ years building
AI products). I'm a solo builder in an international student hackathon and I want a BRUTALLY HONEST,
no-flattery verification of my project before I submit. Do NOT try to make me feel good. If something
is weak, mediocre, generic, over-claimed, or unlikely to qualify — say so plainly and explain why.
Question my assumptions. Point out exactly where a real judge would push back. Praise only what
genuinely deserves it.

Using the BRIEFING below, give me a structured, critical evaluation:

1. **Theme fit** — Does the project genuinely fit the chosen theme ("Agentic & Autonomous Systems"),
   or am I stretching it? Is it *actually* agentic/autonomous, or a dressed-up workflow?
2. **Problem-statement critique** — Is the self-defined problem real, specific, original, and impactful,
   or generic/over-scoped/contrived? Would judges find it compelling? Any factual or framing risks?
3. **Per-criterion scoring** — Score each judging criterion out of 5 with honest reasoning AND the single
   most important thing that would raise each score:
   Innovation & Technical Depth · Engineering Quality · Real-World Impact · Scalability ·
   Design & UX · Execution & Completeness.
4. **Realistic qualification odds** — Honestly, what's my chance of making the Top 100 (of an unknown
   field)? Low / fair / good / strong — and why. Don't hedge into uselessness.
5. **Top risks & weaknesses** — The 3–5 things most likely to cost me points or get questioned by judges.
6. **What I'm missing** — Anything important (technical, product, impact, or submission) I haven't
   considered that I should add or reconsider.
7. **Prioritized fix list** — The few highest-leverage actions, in order, for the time I have left.
8. **Final honest take** — 3–4 sentences: is this a strong submission or not, and what would make it great.

Be specific, cite my own details back to me, and flag anything that sounds like a claim I can't back up.

---

## ▼ PART 2 — THE BRIEFING (paste this too)

### The hackathon: "FAR AWAY 2026"
- Organized by Zuup (youth-led nonprofit). International, ages 15–25, solo or teams ≤5.
- **3 rounds:** Round 1 = online MVP (build week, **Top ~100 + 50 waitlist qualify**); Round 2 = in-person
  24-hour hackathon in Delhi (Top 5 advance; travel not funded); Round 3 = grand finale **in Japan**.
- **Round 1 task:** pick ONE of 5 themes and build a **working MVP** demonstrating *innovation, technical
  depth, and real-world impact*. Submit: **working demo + GitHub repo + optional PPT/video**.
- **The 5 themes:** Railways · Examinations · **Agentic & Autonomous Systems** · Space & Aerospace · Logistics & Transit.
- **Judging criteria:** Innovation & Technical Depth · Engineering Quality · Real-World Impact ·
  Scalability · Design & User Experience · Execution Quality & Completeness.
- **They REWARD:** real working products, technical depth, real-world impact, creative AI use, builders who
  ship. **They PENALIZE:** idea-only/PowerPoint startups, copy-paste, fake demos, **minimal-effort AI wrappers**, lack of depth.

### My choice
- **Theme:** Agentic & Autonomous Systems. **Builder:** solo (Python/ML background), limited time.
- The hackathon gives only a theme — *I* defined the problem statement.

### My project: "Kakehashi" (架け橋 = "bridge")
**Problem statement:** An autonomous, source-grounded multi-agent system that guides **Indian skilled
workers** through **Japan's Specified Skilled Worker (SSW)** visa journey. Grounded in the real **August
2025 India–Japan Human Resource Exchange Partnership** (a signed pact to move 50,000 Indian workers to
Japan, which faces an MHLW-projected ~570,000 care-worker shortfall by 2040). Both governments named AI for "trustworthy
talent mobility." The worker's journey today is a months-long maze across Japanese-government sites,
exploited by scam middlemen.

**What it does:** the user enters a profile or uploads a resume; autonomous agents then (1) classify the
correct visa pathway and adapt the plan per person, (2) pull real live job openings ranked by fit,
(3) lay out the official step-by-step procedure with a real government link per step, (4) build a study
plan with free resources, (5) estimate salary & cost, (6) answer follow-ups in a grounded chat — in
English, Hindi, or Japanese — and export a PDF "Migration Dossier."

**Why I claim it's more than a wrapper (please pressure-test these):**
- **6 specialized agents**, each: reason → call a REAL external tool → cite the source → score confidence.
- **Adaptive autonomy:** an LLM router classifies the visa route; e.g. a software engineer is **rerouted to
  the Engineer visa and the SSW-only steps are auto-skipped**; HR → Specialist visa; nurse → full SSW plan.
  The plan literally changes shape per person.
- **Real data, "real or nothing":** SSW rules grounded & cited from official ssw.go.jp (ISA) + MOFA via RAG;
  live jobs from the JSearch API; government stats from Japan e-Stat. If a key/source is missing, the tool
  says "not configured" — it never fabricates.
- **Measured proof:** a built-in grounded-vs-ungrounded ablation, scored against a gold set of official
  facts, shows grounded = 86% accuracy + 0 hallucinations consistently across runs, vs an erratic 29–71% ungrounded baseline (see PROOF.md).
- **Stack:** Next.js + FastAPI (SSE live agent timeline) + Groq `gpt-oss-120b` (multilingual) + BM25 RAG +
  Fernet (AES) encryption. Multi-page site (Home / How it works / App), persona quick-starts, save/share link.

### Honest current status (do not assume more than this)
- **Built and tested end-to-end; on GitHub.** Runs locally (backend + frontend).
- **NOT yet deployed** — there is no public live URL yet.
- Submission package (README, pitch deck, demo-video script) is drafted.
- My own rough self-score is ~4/5 average — strongest on real-world impact and technical depth; weakest on
  scalability and completeness (both largely fixed by deploying).
- **Roadmap (clearly marked, not live):** Amadeus flight integration (paid tier), e-Stat "demand" charts,
  recruiter-scam detection.
- **Remaining before submission:** deploy (public URL) → record demo video → polish (loading/empty states,
  mobile, accessibility) → backend hardening (caching, rate-limit).

### What I want verified
Honestly: is the **theme choice** right, is the **problem statement** strong and real, does the **MVP fulfill
the judging criteria**, and what's my **realistic chance to qualify** — plus exactly what to fix.
