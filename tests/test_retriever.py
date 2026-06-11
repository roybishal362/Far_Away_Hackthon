"""Retrieval must return cited passages, and the right ones for key queries."""
from core.rag.index import Retriever


def test_every_passage_carries_a_citation():
    r = Retriever()
    for q in ("language test JLPT", "family members stay", "deposit scam agent fee"):
        for p in r.retrieve(q, k=4):
            assert p.citation.source_url.startswith("http")
            assert p.citation.title


def test_deposit_query_surfaces_worker_protection():
    r = Retriever()
    texts = " ".join(p.text.lower() for p in r.retrieve("agent asked me to pay a deposit", k=4))
    assert "deposit" in texts


def test_language_query_surfaces_jlpt_or_jft():
    r = Retriever()
    texts = " ".join(p.text.lower() for p in r.retrieve("japanese language test requirement", k=4))
    assert "jlpt" in texts or "jft" in texts
