"""'Real or nothing': no key + no fixture => honest failure; fixture => clearly
labeled cached sample; never silent fabrication."""
import json
from types import SimpleNamespace

import core.tools.jobs as jobs_mod
from core.tools.jobs import JobsTool


def _no_key(monkeypatch, tmp_path):
    monkeypatch.setattr(jobs_mod, "SETTINGS", SimpleNamespace(jsearch_api_key=None))
    monkeypatch.setenv("KAKEHASHI_FIXTURES_DIR", str(tmp_path))
    jobs_mod._CACHE.clear()


def test_unconfigured_without_fixture_fails_honestly(monkeypatch, tmp_path):
    _no_key(monkeypatch, tmp_path)
    res = JobsTool().run(query="caregiver")
    assert res.ok is False
    assert "not configured" in (res.error or "")


def test_fallback_disabled_never_serves_fixtures(monkeypatch, tmp_path):
    _no_key(monkeypatch, tmp_path)
    monkeypatch.setenv("KAKEHASHI_CACHED_FALLBACK", "0")
    (tmp_path / "jobs_caregiver.json").write_text(json.dumps(
        {"keyword": "caregiver", "jobs": [{"title": "Care Worker", "employer": "X", "apply_link": "https://x"}]}))
    assert JobsTool().run(query="caregiver").ok is False


def test_fixture_fallback_is_clearly_labeled(monkeypatch, tmp_path):
    _no_key(monkeypatch, tmp_path)
    monkeypatch.setenv("KAKEHASHI_CACHED_FALLBACK", "1")
    (tmp_path / "jobs_caregiver.json").write_text(json.dumps(
        {"keyword": "caregiver", "jobs": [{"title": "Care Worker", "employer": "X", "apply_link": "https://x"}]}))
    res = JobsTool().run(query="caregiver")
    assert res.ok is True
    assert "cached sample" in res.source
    assert res.citations and res.citations[0].source_url == "https://x"


def test_generic_fallback_used_for_unknown_keyword(monkeypatch, tmp_path):
    _no_key(monkeypatch, tmp_path)
    (tmp_path / "jobs_skilled_worker.json").write_text(json.dumps(
        {"keyword": "skilled worker", "jobs": [{"title": "Operator", "employer": "Y", "apply_link": "https://y"}]}))
    res = JobsTool().run(query="zookeeper")
    assert res.ok is True and "cached sample" in res.source
