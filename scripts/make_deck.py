"""Generate the Kakehashi submission deck as a real .pptx.
Run: python scripts/make_deck.py  ->  Kakehashi_FAR_AWAY_2026.pptx
"""
import os
import sys

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Kakehashi_FAR_AWAY_2026.pptx")

INDIGO = RGBColor(0x1F, 0x21, 0x50)
SAKURA = RGBColor(0xE1, 0x1D, 0x54)
MARIGOLD = RGBColor(0xFF, 0x95, 0x00)
INK = RGBColor(0x15, 0x16, 0x3A)
GREY = RGBColor(0x6B, 0x6B, 0x80)
EMER = RGBColor(0x10, 0xB9, 0x81)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xF6, 0xF2, 0xF5)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height


def _box(slide, l, t, w, h, color, line=None):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    if line:
        s.line.color.rgb = line; s.line.width = Pt(1)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def _text(slide, l, t, w, h, runs, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, space=6):
    tb = slide.shapes.add_textbox(l, t, w, h); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    items = runs if isinstance(runs, list) else [runs]
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(space)
        if isinstance(item, tuple):
            txt, opt = item
        else:
            txt, opt = item, {}
        r = p.add_run(); r.text = txt
        r.font.size = Pt(opt.get("size", size)); r.font.bold = opt.get("bold", bold)
        r.font.color.rgb = opt.get("color", color); r.font.name = "Calibri"
    return tb


def footer(slide, n):
    _text(slide, Inches(0.5), Inches(7.0), Inches(8), Inches(0.4),
          "Kakehashi 架け橋  ·  FAR AWAY 2026  ·  Agentic & Autonomous Systems", size=10, color=GREY)
    _text(slide, Inches(12.3), Inches(7.0), Inches(0.7), Inches(0.4), str(n), size=10, color=GREY, align=PP_ALIGN.RIGHT)


def content(title, bullets, n, accent=SAKURA, subtitle=None):
    s = prs.slides.add_slide(BLANK)
    _box(s, 0, 0, W, Inches(0.18), accent)
    _text(s, Inches(0.6), Inches(0.45), Inches(12), Inches(1.0), title, size=32, bold=True, color=INDIGO)
    top = 1.55
    if subtitle:
        _text(s, Inches(0.6), Inches(1.4), Inches(12), Inches(0.6), subtitle, size=16, color=SAKURA, bold=True)
        top = 2.1
    runs = [(("•  " + b) if not isinstance(b, tuple) else b) for b in bullets]
    _text(s, Inches(0.7), Inches(top), Inches(12), Inches(5), runs, size=19, color=INK, space=12)
    footer(s, n)
    return s


# 1 — Title
s = prs.slides.add_slide(BLANK)
_box(s, 0, 0, W, H, INDIGO)
_box(s, 0, Inches(6.7), W, Inches(0.8), SAKURA)
_text(s, Inches(0.8), Inches(2.1), Inches(11.7), Inches(1.6),
      [("Kakehashi ", {"size": 60, "bold": True, "color": WHITE}), ("架け橋", {"size": 44, "color": RGBColor(0xFF, 0x9B, 0xB3)})])
_text(s, Inches(0.85), Inches(3.5), Inches(11.5), Inches(0.8),
      "An autonomous AI bridge for Indian workers to Japan", size=26, color=WHITE)
_text(s, Inches(0.85), Inches(4.4), Inches(11.5), Inches(0.8),
      "Real data, not mockups · Cited, not hallucinated · Proven, not claimed · EN / हिन्दी / 日本語", size=15, color=RGBColor(0xCF, 0xD0, 0xE0))
_text(s, Inches(0.85), Inches(6.75), Inches(11.5), Inches(0.6),
      "FAR AWAY 2026  ·  Theme: Agentic & Autonomous Systems", size=14, color=WHITE, bold=True)

# 2 — Problem
content("The problem", [
    "India & Japan signed a 2025 pact to move 50,000 skilled Indian workers to Japan.",
    "Japan faces a severe labour shortage — 300,000+ caregivers short by 2035.",
    "But for a worker, the journey is a months-long maze: which visa? am I eligible? the JLPT N4 bar, skills tests, paperwork, finding a real employer, cost, relocation.",
    "Information is scattered across Japanese government sites — and middlemen & misinformation fill the gap.",
], 2, accent=SAKURA, subtitle="A real, current, dual-government opportunity — with a painful gap")

# 3 — Solution
content("Kakehashi — the autonomous guide", [
    "Tell it about you (or upload your resume).",
    "Autonomous agents determine YOUR visa pathway, pull REAL live jobs, lay out the official step-by-step with real gov links, build a study plan, and estimate salary & cost.",
    "Ask follow-ups in a grounded chat — in your language.",
    "Save, share, or download the whole plan as a PDF 'Migration Dossier'.",
], 3, accent=INDIGO, subtitle="Assess → real jobs → procedure → study plan → cost → chat")

# 4 — Why different
content("Why it's different — 3 pillars", [
    ("Real or nothing — every tool returns real data or honestly says 'not configured'. It physically cannot fabricate.", {"size": 19, "bold": True, "color": INK}),
    ("Proven, not claimed — a built-in ablation measures grounded vs. ungrounded accuracy & hallucinations.", {"size": 19, "bold": True, "color": INK}),
    ("Genuinely autonomous — 6 agents reason → call a real tool → cite → score confidence; the orchestrator adapts the plan to you. Not a prompt wrapper.", {"size": 19, "bold": True, "color": INK}),
    ("FAR AWAY explicitly penalizes 'minimal-effort AI wrappers' and 'fake demos'. Kakehashi is the opposite.", {"size": 16, "color": SAKURA, "bold": True}),
], 4, accent=MARIGOLD)

# 5 — Architecture / agents
content("The multi-agent system", [
    "Pathway — classifies the right visa (SSW / Engineer / Specialist) + a personalized verdict, readiness score & gaps  [grounded, cited]",
    "Jobs — fetches real live openings, ranks each by fit to you  [JSearch API]",
    "Procedure — the official ordered journey, each step with the real gov link  [grounded]",
    "Prep — a study + exam plan keyed to your Japanese level + free resources",
    "Synthesis — your personal overview + salary + cost  ·  Chat — grounded follow-up Q&A",
], 5, accent=INDIGO, subtitle="Each agent: reason → call a real tool → cite → confidence  ·  streamed live over SSE")

# 6 — Autonomy in action
content("Autonomy in action (the 'wow')", [
    "Nurse (Delhi, no Japanese) → SSW caregiving pathway, full plan, ranked jobs, study plan.",
    "Software engineer → the system REFUSES to force SSW and reroutes to the Engineer visa — and auto-skips the SSW-only steps.",
    "HR / office role → routed to the Specialist (技人国) visa instead.",
    "The plan literally changes shape based on who you are. That is autonomous decision-making, not a fixed pipeline.",
], 6, accent=SAKURA, subtitle="Different person → different plan → the agent decides")

# 7 — Proof
s = content("Proof, not claims", [], 7, accent=EMER, subtitle="Same question, grounded vs. ungrounded — scored against a gold set of official facts")
_box(s, Inches(1.3), Inches(2.6), Inches(4.6), Inches(2.6), LIGHT)
_text(s, Inches(1.3), Inches(2.85), Inches(4.6), Inches(0.6), "Our grounded agents", size=18, bold=True, color=INDIGO, align=PP_ALIGN.CENTER)
_text(s, Inches(1.3), Inches(3.4), Inches(4.6), Inches(1.0), "≈ 71%", size=44, bold=True, color=EMER, align=PP_ALIGN.CENTER)
_text(s, Inches(1.3), Inches(4.5), Inches(4.6), Inches(0.5), "accuracy  ·  0 hallucinations", size=16, color=INK, align=PP_ALIGN.CENTER)
_box(s, Inches(7.4), Inches(2.6), Inches(4.6), Inches(2.6), LIGHT)
_text(s, Inches(7.4), Inches(2.85), Inches(4.6), Inches(0.6), "Plain LLM (ungrounded)", size=18, bold=True, color=INDIGO, align=PP_ALIGN.CENTER)
_text(s, Inches(7.4), Inches(3.4), Inches(4.6), Inches(1.0), "≈ 14%", size=44, bold=True, color=SAKURA, align=PP_ALIGN.CENTER)
_text(s, Inches(7.4), Inches(4.5), Inches(4.6), Inches(0.5), "accuracy  ·  6 hallucinations", size=16, color=INK, align=PP_ALIGN.CENTER)
_text(s, Inches(0.7), Inches(5.5), Inches(12), Inches(0.6), "Grounding takes accuracy 14% → 71% and cuts hallucinations to zero. The proof is a number.", size=16, color=INK, bold=True)

# 8 — Real data
content("Built on real data", [
    "SSW rules & procedures — official ssw.go.jp (ISA) + MOFA, grounded & cited (RAG).",
    "Live job openings — JSearch real-time API.",
    "Government labour statistics — Japan e-Stat official API.",
    "Exam fees & salaries — Prometric, JLPT, JFT + sourced research.",
    "No key → the tool says so. It never invents data.",
], 8, accent=INDIGO, subtitle="Every claim traces to a real source")

# 9 — Product
content("A real product, not a demo", [
    "Multi-page site: Home (the story) · How it works (the depth) · Build my plan (the tool).",
    "Tabs: Overview · Pathway · Jobs · Procedure · Study plan · Journey · Proof · Ask AI.",
    "Resume auto-fill · persona quick-starts · save/share link · PDF dossier · progress checklist.",
    "Multilingual — content AND chat in English / हिन्दी / 日本語 (the finale is in Japan).",
    "Private by design: encryption at rest, no PII in logs, honest disclaimer.",
], 9, accent=MARIGOLD)

# 10 — Impact
content("Real-world impact — a true bridge", [
    "Worker: a cited, honest path — and a way around recruitment-fee scams (official free job-matching).",
    "Japan: fills its designated-sector labour shortage.",
    "India: formal overseas employment + remittances.",
    "Directly serves the signed India–Japan partnership and the named goal of trustworthy AI for talent mobility.",
], 10, accent=SAKURA, subtitle="It helps the worker, Japan, and India at once")

# 11 — Tech & scalability
content("Engineering & scalability", [
    "Frontend: Next.js 14 + TypeScript + Tailwind + Framer Motion.  Backend: FastAPI + SSE.",
    "LLM: Groq gpt-oss-120b (strong multilingual).  RAG: BM25.  Security: Fernet (AES).",
    "UI-agnostic core with swappable agents & tools — add a sector, agent, or visa route without a rewrite.",
    "Honest roadmap: Amadeus flights (paid tier) and e-Stat demand charts are wired and clearly marked as next.",
], 11, accent=INDIGO, subtitle="Modular, built to extend — not a throwaway demo")

# 12 — Closing
s = prs.slides.add_slide(BLANK)
_box(s, 0, 0, W, H, INDIGO)
_box(s, 0, Inches(6.7), W, Inches(0.8), MARIGOLD)
_text(s, Inches(0.85), Inches(2.2), Inches(11.6), Inches(1.2),
      "A bridge between India and Japan.", size=40, bold=True, color=WHITE)
_text(s, Inches(0.9), Inches(3.5), Inches(11.5), Inches(2),
      [("Real data. Cited sources. Measured proof. Genuinely autonomous.", {"size": 22, "color": RGBColor(0xFF, 0x9B, 0xB3)}),
       ("Working demo  ·  GitHub: github.com/roybishal362/Far_Away_Hackthon", {"size": 18, "color": WHITE}),
       ("Kakehashi 架け橋  —  FAR AWAY 2026", {"size": 16, "color": RGBColor(0xCF, 0xD0, 0xE0)})], space=14)

prs.save(OUT)
print("Saved deck:", OUT, "| slides:", len(prs.slides._sldIdLst))
