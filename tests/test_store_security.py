"""Share-link IDs must not be a path-traversal vector, and round-trips must work."""
import secrets

import core.store as store
from api.main import _PID_RE


def test_pid_regex_blocks_traversal():
    for bad in ("../etc/passwd", "..", "a/b", "x" * 30, "ab"):
        assert not _PID_RE.match(bad)
    assert _PID_RE.match(secrets.token_urlsafe(8))


def test_save_load_roundtrip(monkeypatch, tmp_path):
    monkeypatch.setattr(store, "_DIR", tmp_path)
    pid = store.save({"hello": "世界"})
    assert store.load(pid) == {"hello": "世界"}
    assert store.load("nonexistent0") is None
