"""BM25 retriever over the official SSW knowledge base.

Lightweight keyword retrieval — no embedding model weights, so it runs reliably
on any host. Returns passages WITH their citations so agents can ground answers.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from core.rag.knowledge import FACTS
from core.types import Citation


@dataclass
class Passage:
    text: str
    citation: Citation
    score: float = 0.0


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


class Retriever:
    def __init__(self, facts: list[dict] | None = None) -> None:
        self.facts = facts or FACTS
        self._corpus = [_tokenize(f["text"] + " " + " ".join(f.get("tags", []))) for f in self.facts]
        from rank_bm25 import BM25Okapi
        self._bm25 = BM25Okapi(self._corpus)

    def retrieve(self, query: str, k: int = 4) -> list[Passage]:
        scores = self._bm25.get_scores(_tokenize(query))
        ranked = sorted(range(len(self.facts)), key=lambda i: scores[i], reverse=True)[:k]
        out: list[Passage] = []
        for i in ranked:
            if scores[i] <= 0:
                continue
            f = self.facts[i]
            out.append(Passage(
                text=f["text"],
                citation=Citation(source_url=f["source_url"], title=f["title"], snippet=f["text"][:160]),
                score=float(scores[i]),
            ))
        return out


_RETRIEVER: Retriever | None = None


def get_retriever() -> Retriever:
    global _RETRIEVER
    if _RETRIEVER is None:
        _RETRIEVER = Retriever()
    return _RETRIEVER
