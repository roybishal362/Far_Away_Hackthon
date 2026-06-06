"""Real encryption-at-rest for any persisted worker profile (AES via Fernet).

Default posture is session-only / no persistence. If the app DOES persist a
profile, it is encrypted with a key from config (FERNET_KEY) — never plaintext.
"""
from __future__ import annotations

import json


def generate_key() -> str:
    """Make a fresh Fernet key (base64 str). Store it as the FERNET_KEY secret."""
    from cryptography.fernet import Fernet
    return Fernet.generate_key().decode()


def encrypt_dict(payload: dict, key: str) -> bytes:
    """Encrypt a profile dict -> opaque token. Real AES (Fernet)."""
    from cryptography.fernet import Fernet
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return Fernet(key.encode()).encrypt(raw)


def decrypt_dict(token: bytes, key: str) -> dict:
    from cryptography.fernet import Fernet
    raw = Fernet(key.encode()).decrypt(token)
    return json.loads(raw.decode("utf-8"))
