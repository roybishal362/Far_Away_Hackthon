"""Save/share plans. Encrypted at rest with Fernet when FERNET_KEY is set,
else plain JSON. IDs are random, unguessable tokens (shareable links)."""
from __future__ import annotations

import json
import secrets
from pathlib import Path

from config import SETTINGS

_DIR = Path(__file__).resolve().parent.parent / "data" / "plans"


def save(plan: dict) -> str:
    _DIR.mkdir(parents=True, exist_ok=True)
    pid = secrets.token_urlsafe(8)
    if SETTINGS.fernet_key:
        from core.security.crypto import encrypt_dict
        (_DIR / f"{pid}.enc").write_bytes(encrypt_dict(plan, SETTINGS.fernet_key))
    else:
        (_DIR / f"{pid}.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return pid


def load(pid: str) -> dict | None:
    enc, plain = _DIR / f"{pid}.enc", _DIR / f"{pid}.json"
    if enc.exists() and SETTINGS.fernet_key:
        from core.security.crypto import decrypt_dict
        return decrypt_dict(enc.read_bytes(), SETTINGS.fernet_key)
    if plain.exists():
        return json.loads(plain.read_text(encoding="utf-8"))
    return None
