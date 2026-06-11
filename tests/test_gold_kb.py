"""The gold set and knowledge base must stay consistent and citable."""
from core.eval.gold import GOLD
from core.rag.knowledge import FACTS


def test_gold_set_is_substantial():
    assert len(GOLD) >= 20, "gold set shrank — the ablation claim depends on its size"


def test_gold_has_no_duplicates():
    assert len(GOLD) == len(set(GOLD))


def test_every_kb_fact_is_citable():
    for f in FACTS:
        assert f["source_url"].startswith("http"), f"uncited KB fact: {f['text'][:60]}"
        assert f.get("title"), "every KB fact needs a source title for the citation chip"
        assert f.get("text", "").strip()


def test_kb_covers_anti_scam_protections():
    """The anti-middleman angle is the project's core — the KB must ground it."""
    blob = " ".join(f["text"].lower() for f in FACTS)
    for needle in ("deposit", "intermediar", "support plan", "equal"):
        assert needle in blob, f"KB lost its '{needle}' worker-protection fact"
