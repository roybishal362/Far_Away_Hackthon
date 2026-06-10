# Kakehashi — FINAL Gamma prompt (Round 1 deck · 15 cards)

HOW TO USE: In Gamma → "Create with AI → Paste text" → paste EVERYTHING below the line.
First set the theme to the palette/fonts in [THEME]. Generate EXACTLY 15 cards (slides are separated
by `---`; do not merge or split). For any slot marked [IMPORT: file.png], do NOT let Gamma AI-generate
an image — leave a placeholder and I'll drop in the real asset after export. Export 16:9 PDF + PPTX.

────────────────────────────────────────────────────────

[THEME — apply before generating]
Palette: primary deep indigo-navy #1B2A4A (≈60% weight); backgrounds off-white #FAFAF7; ONE accent only —
torii vermillion #D9381E (key numbers, the router node, CTAs); captions warm grey #8A8F98. Dark navy
backgrounds on slides 1, 9, 15 only; light on the rest.
Typography: bold geometric sans headlines (Inter/Archivo) 36pt+; body 14–16pt left-aligned; giant stat
numbers 60–72pt with small labels. Center titles only.
Motif: ONE subtle recurring bridge-arc line as the section/image frame on every slide.
FORBIDDEN (these are AI-deck tells): no accent underlines on titles, no edge color stripes, no header/footer
bars, no text-only slides, no centered paragraphs, no cream/beige backgrounds.
Footer (small, muted, text only): Kakehashi 架け橋 · FAR AWAY 2026 · Agentic & Autonomous Systems
Style: assertion headlines (full-sentence takeaways, not labels). One idea + one visual per slide. ≤25 words body.

────────────────────────────────────────────────────────

Headline: Kakehashi 架け橋
Body: An autonomous, source-grounded multi-agent guide for India→Japan skilled-worker migration. Solo builder · Theme: Agentic & Autonomous Systems · FAR AWAY 2026.
Layout: dark navy title slide; wordmark centered with a vermillion bridge-arc; three small labelled QR codes bottom-right.
Image: [IMPORT: qr_strip.png — Live demo / GitHub / Video] (do NOT AI-generate)

---

Headline: For an Indian worker, the path to a Japanese visa is a months-long maze — and scammers live in the gaps.
Body: Official guidance is scattered across Japanese-language government sites · the wrong pathway costs months · fraudulent middlemen exploit the confusion — both governments name "malicious intermediaries" as a target problem in their SSW cooperation framework.
Layout: persona card on the left ("Priya, 24 — nurse from Kochi, wants Japan's caregiver pathway"); schematic tangled-path graphic on the right with dead-ends and a red "agent fee ₹___" trap node.
Image: [IMPORT: maze_persona.png] (do NOT AI-generate)

---

Headline: Two governments just signed the corridor — but the infrastructure for the workers doesn't exist yet.
Body: 500,000 two-way exchanges in 5 years · 50,000 skilled Indian workers to Japan (Aug-2025 India–Japan Action Plan) · 570,000 care-worker shortfall in Japan by 2040 (MHLW, 9th LTC Insurance Plan).
Layout: three giant vermillion stat numbers with small labels; a minimal India→Japan corridor map using the arc motif. Small muted source line: mofa.go.jp · pmindia.gov.in · MHLW 2024.
Image: [Gamma layout — large stat numbers + simple corridor arc]

---

Headline: Kakehashi turns the maze into a personal, cited, step-by-step plan — in English, Hindi, and Japanese.
Body: Six outcome chips: Visa pathway classified · Live jobs ranked · Official steps, gov-linked · Study plan built · Salary & cost estimated · Grounded Q&A chat — exports a PDF "Migration Dossier."
Layout: outcome chips on the left; real hero screenshot half-bleed on the right. No tech words on this slide.
Image: [IMPORT: screenshot_home.png] (do NOT AI-generate)

---

Headline: Deployed and working — try it yourself in 90 seconds.
Body: Pick a persona → watch the agents reason live → open any citation. Live demo: [PASTE LIVE URL AFTER DEPLOY].
Layout: 2–3 real screenshots in rounded frames (the live SSE agent-timeline mid-run is the must-have), one thin vermillion annotation each; a large QR to the live URL.
Image: [IMPORT: screenshot_timeline.png + qr_live.png] (do NOT AI-generate)

---

Headline: Specialized agents that each reason, call a real external tool, cite the source, and score their confidence.
Body: Footer strip (text only): Next.js · FastAPI (SSE) · Groq gpt-oss-120b · BM25 RAG · Fernet-encrypted PII.
Layout: full-slide imported architecture diagram, left→right: User profile/resume → Orchestrator + LLM Router (vermillion) → Pathway (SSW/MOFA RAG) · Jobs (JSearch API) · Procedure (ssw.go.jp / ISA) · Study plan (curated free resources) · Synthesis: salary & cost (sourced benchmarks) · Q&A (grounded RAG) → shared Verification & Citation layer ("source + confidence, or 'not configured' — never fabricates") → Migration Dossier (PDF) / SSE timeline. Inside one node show the micro-loop reason→tool→cite→confidence.
Image: [IMPORT: diagram_architecture.png] (do NOT AI-generate)

---

Headline: The plan changes shape per person — the system decides the route, not a template.
Body: Same input form, structurally different plans. Routing, step-skipping, and mid-run re-planning are model decisions at runtime — e.g. the Jobs agent broadens its query and retries when results are thin, live in the timeline.
Layout: imported side-by-side divergence diagram. One Router at left. Top branch "Priya · Nurse" → SSW Caregiver pathway → full chain (skills test → JFT-Basic → jobs → CoE → visa). Bottom branch "Arjun · Software Engineer" → rerouted to Engineer/Specialist visa, with the SSW-only steps greyed/struck-through labelled "auto-skipped by router." Annotation: "HR profile → Specialist visa."
Image: [IMPORT: diagram_reroute.png] (do NOT AI-generate)

---

Headline: Every claim is cited to an official source — and when a source is missing, Kakehashi says so instead of guessing.
Body: Citations resolve to ssw.go.jp / MOFA · per-agent confidence shown in the Proof tab · no key, no source → "not configured," never invented.
Layout: composite real screenshot — a cited answer with its source chip, a vermillion arrow to the actual ssw.go.jp page it opens.
Image: [IMPORT: screenshot_citation.png] (do NOT AI-generate)

---

Headline: Grounding isn't a claim — we measured it: 86% accuracy with 0 hallucinations on every run, vs a plain LLM swinging 29–71%.
Body: Scored against a gold set of 7 official facts. Reproducible: eval script + gold set + results committed in the repo (PROOF.md). Grounding makes it accurate AND consistent.
Layout: dark navy slide; full-slide imported matplotlib ablation chart (vermillion = grounded, navy = ungrounded; big % labels; "0 hallucinations, every run" callout).
Image: [IMPORT: chart_ablation.png] (do NOT AI-generate)

---

Headline: Built for the worker, not the middleman — trilingual, mobile, and free at the point of use.
Body: Serves SSW / Engineer / Specialist aspirants across the SSW program's designated sectors · EN / HI / JA today, regional languages on the roadmap · output is a portable, cited PDF dossier the worker owns.
Layout: real dossier screenshot or a 3-persona quick-start strip. (If any real users by submission: replace body with one user quote + "X dossiers generated in week 1.")
Image: [IMPORT: screenshot_dossier.png] (do NOT AI-generate)

---

Headline: Production habits on a hackathon timeline.
Body: Live agent telemetry — SSE step-by-step timeline · PII encrypted at rest (Fernet / AES-128) · graceful degradation on every external dependency · validated inputs + non-guessable plan IDs.
Layout: real screenshot of the SSE timeline with two thin annotations; icon rows for the four points. (Only true items listed.)
Image: [IMPORT: screenshot_timeline2.png] (do NOT AI-generate)

---

Headline: Today it serves a demo; the path to 50,000 workers is boring, known engineering.
Body: Two columns — Now: BM25 in-process · single region · free-tier inference. Next: hybrid retrieval (vector DB) · response caching + job queue · WhatsApp delivery channel (where this user actually lives) · multi-region.
Layout: clean two-column "Now → Next" with the arc motif bridging them.
Image: [Gamma layout — two-column comparison]

---

Headline: Round 1 ships the engine; Rounds 2–3 ship the shield and the pilot.
Body: Three columns clearly labelled "Roadmap — not live today." R1 (shipped): everything in this deck. R2: "Sentinel" recruiter-scam detector (checks offers vs registered sending-org lists) + WhatsApp bot. R3: institutional pilot with a training/coaching partner + e-Stat demand dashboards.
Layout: 3-column horizon timeline; a prominent "Roadmap — not live" tag.
Image: [Gamma layout — 3-column horizon]

---

Headline: How Kakehashi addresses the six judging criteria.
Body: Innovation/Depth → measured ablation + adaptive routing (s7, s9) · Engineering → SSE, encryption, graceful failure (s11) · Impact → signed 50k-worker corridor + trilingual (s3, s10) · Scalability → honest ladder + WhatsApp (s12) · Design/UX → personas, dossier, mobile (s5, s10) · Completeness → deployed URL + repo + video (s5).
Layout: clean 6-row table, criterion → one-line evidence pointer. Humble phrasing ("How we address…").
Image: [Gamma layout — 6-row table]

---

Headline: A bridge needs to exist before people can cross it. Kakehashi is live.
Body: One-line recap. Built solo during build week — everything shown in this deck is running today. Live demo · GitHub · 3-min video.
Layout: dark navy close; wordmark + the bridge-arc completing across the slide; three large labelled QR codes.
Image: [IMPORT: qr_strip_large.png — Live demo / GitHub / Video] (do NOT AI-generate)

────────────────────────────────────────────────────────

ASSETS TO IMPORT (generate these real, before finalizing):
- diagram_architecture.png, diagram_reroute.png (navy nodes / vermillion router + verification layer)
- chart_ablation.png (matplotlib, from PROOF.md numbers: grounded 86% & 0 halluc vs ungrounded 29–71%)
- screenshots (real deployed app): home, SSE timeline mid-run, citation→ssw.go.jp composite, PDF dossier, mobile, HI/JA toggle
- qr codes: live URL, GitHub (github.com/roybishal362/Far_Away_Hackthon), demo video — test from a phone
