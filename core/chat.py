"""Grounded follow-up chat — 'Ask Kakehashi'.

Answers using ONLY official SSW facts (RAG) + the curated knowledge pack
(fees, salaries, study resources, IT routing). Honest when unsure; cites sources.
"""
from __future__ import annotations

from core import knowledge_pack as KP
from core.llm import get_llm
from core.rag.index import get_retriever

SYSTEM = (
    "You are Kakehashi, a careful assistant for Indian workers migrating to Japan via the Specified Skilled "
    "Worker (SSW) program. Answer ONLY from the provided OFFICIAL CONTEXT and KNOWLEDGE PACK. If the answer "
    "isn't supported there, say you're not certain and point the user to the official source. Be concise, "
    "practical, and friendly. Never invent fees, dates, or URLs."
)


def _pack_context() -> str:
    fees = "; ".join(f"{f['item']}: {f['amount']}" for f in KP.FEES)
    sal = "; ".join(f"{k}: ¥{v['min']:,}-{v['max']:,}/mo" for k, v in KP.SALARIES.items())
    res = "; ".join(f"{r['name']} ({r['url']})" for r in KP.STUDY_RESOURCES[:6])
    return (
        f"FEES — {fees}. {KP.SALARY_NOTE}\n"
        f"SSW SALARIES (gross/month) — {sal}; other SSW sectors ¥{KP.SALARY_DEFAULT['min']:,}-{KP.SALARY_DEFAULT['max']:,}.\n"
        f"IT/SOFTWARE/ENGINEERING — {KP.NON_SSW['engineer']['detail']}\n"
        f"OFFICE/HR/BUSINESS/HUMANITIES — {KP.NON_SSW['specialist']['detail']}\n"
        f"NON-SSW SALARY — professional/engineer roles vary widely by role & company, typically higher than SSW; check live job listings for figures.\n"
        f"FREE STUDY RESOURCES — {res}.\n"
        f"SECTORS — {', '.join(s['name'] for s in KP.SECTORS)}."
    )


_LANGS = {"en": "English", "hi": "Hindi", "ja": "Japanese"}


def answer(question: str, profile_text: str = "", history: list[dict] | None = None, lang: str = "en") -> dict:
    passages = get_retriever().retrieve(question, k=5)
    ctx = "\n".join(f"[{i + 1}] {p.text} (source: {p.citation.title})" for i, p in enumerate(passages))
    hist = "\n".join(f"{m.get('role')}: {m.get('content')}" for m in (history or [])[-4:])
    lang_note = "" if lang == "en" else f"\nReply in {_LANGS.get(lang, 'English')}."

    user = (
        (f"Worker profile: {profile_text}\n\n" if profile_text else "")
        + (f"CONVERSATION SO FAR:\n{hist}\n\n" if hist else "")
        + f"OFFICIAL CONTEXT:\n{ctx}\n\nKNOWLEDGE PACK:\n{_pack_context()}\n\n"
        + f"QUESTION: {question}\n\nAnswer concisely using only the above.{lang_note}"
    )
    text = get_llm().complete(SYSTEM, user, temperature=0.3, max_tokens=600)
    citations = [{"url": p.citation.source_url, "title": p.citation.title} for p in passages]
    return {"answer": text, "citations": citations}
