"""Migration Dossier — render a run result + profile into a downloadable PDF.

ASCII-safe text only (Helvetica) so it renders on any host; uses 'JPY' not the
yen glyph and '->' not arrows to avoid missing-glyph boxes.
"""
from __future__ import annotations

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (HRFlowable, ListFlowable, ListItem, Paragraph,
                                SimpleDocTemplate, Spacer)


def build(plan: dict, profile: dict) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, title="Kakehashi Migration Dossier",
        topMargin=1.6 * cm, bottomMargin=1.6 * cm, leftMargin=1.8 * cm, rightMargin=1.8 * cm,
    )
    ss = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=ss["Title"], fontSize=20, textColor=colors.HexColor("#1f2150"))
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], textColor=colors.HexColor("#e11d54"))
    body = ss["BodyText"]
    small = ParagraphStyle("small", parent=body, fontSize=8, textColor=colors.grey)

    def P(t, s=body):
        return Paragraph(str(t), s)

    results = plan.get("results", {}) or {}
    story = [
        P("Kakehashi - Migration Dossier", h1),
        P("Your personalized path to Japan via the Specified Skilled Worker program", small),
        Spacer(1, 0.4 * cm),
    ]

    if profile:
        story += [P("Your profile", h2), P(
            f"Skills: {profile.get('skills','')}<br/>Sector: {profile.get('sector_interest','')}<br/>"
            f"Experience: {profile.get('years_experience','')} yrs<br/>Japanese: {profile.get('japanese_level','')}<br/>"
            f"Route: {profile.get('origin_city','')} -> {profile.get('target_city','')}"
        ), Spacer(1, 0.3 * cm)]

    syn = (results.get("synthesis", {}) or {}).get("data") or {}
    if syn:
        story.append(P("Overview", h2))
        if syn.get("summary"):
            story.append(P(syn["summary"]))
        sal = syn.get("salary") or {}
        if sal.get("min"):
            story.append(P(f"Expected salary: JPY {sal['min']:,}-{sal['max']:,}/month. {syn.get('salary_note','')}"))
        if syn.get("fees"):
            story.append(P("Estimated costs: " + "; ".join(f"{f['item']} {f['amount']}" for f in syn["fees"])))
        story.append(Spacer(1, 0.3 * cm))

    pw = (results.get("pathway", {}) or {}).get("data") or {}
    if pw:
        story.append(P("Your pathway", h2))
        if pw.get("eligibility_verdict"):
            story.append(P(f"Verdict: {pw['eligibility_verdict']} (readiness {pw.get('readiness_percent','-')}%)"))
        for label, key in [("What you have", "what_you_have"), ("What you need", "what_you_need"), ("Requirements", "requirements")]:
            items = pw.get(key) or []
            if items:
                story.append(P(f"<b>{label}:</b>"))
                story.append(ListFlowable([ListItem(P(x, small)) for x in items], bulletType="bullet"))
        story.append(Spacer(1, 0.3 * cm))

    steps = ((results.get("procedure", {}) or {}).get("data") or {}).get("steps") or []
    if steps:
        story.append(P("Step-by-step procedure", h2))
        for i, s in enumerate(steps):
            story.append(P(f"<b>{i + 1}. {s.get('step','')}</b>"))
            if s.get("detail"):
                story.append(P(s["detail"], small))
            for res in (s.get("resources") or []):
                story.append(P(f'- {res.get("name","")}: <link href="{res.get("url","")}">{res.get("url","")}</link>', small))
        story.append(Spacer(1, 0.3 * cm))

    res_list = ((results.get("prep", {}) or {}).get("data") or {}).get("resources") or []
    if res_list:
        story.append(P("Free study resources", h2))
        for r in res_list:
            story.append(P(f'- {r.get("name","")}: <link href="{r.get("url","")}">{r.get("url","")}</link>', small))
        story.append(Spacer(1, 0.3 * cm))

    jobs = ((results.get("jobs", {}) or {}).get("data") or {}).get("jobs") or []
    if jobs:
        story.append(P("Live job openings (sample)", h2))
        for j in jobs[:8]:
            story.append(P(f'- {j.get("title","")} - {j.get("employer","")}: <link href="{j.get("apply_link","")}">apply</link>', small))
        story.append(Spacer(1, 0.3 * cm))

    story.append(HRFlowable(width="100%", color=colors.lightgrey))
    story.append(P(syn.get("disclaimer", "") or "Guidance only - verify with official authorities.", small))

    doc.build(story)
    return buf.getvalue()
