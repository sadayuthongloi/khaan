import base64
import hashlib
from dataclasses import dataclass
from typing import Optional

from cryptography.fernet import Fernet, InvalidToken


ENC_PREFIX = "ENC:"
_KEY_WORDING_SALT = "#Standard MongoDB Management System#"


def derive_legacy_md5_hex(key_wording: str) -> str:
    """
    Derive the same final MD5 hex printed by `key.py`:
      md5(md5(key_wording) + "#Standard MongoDB Management System#")
    """
    md5_first = hashlib.md5(key_wording.encode("utf-8")).hexdigest()
    md5_plus_salt = md5_first + _KEY_WORDING_SALT
    md5_final = hashlib.md5(md5_plus_salt.encode("utf-8")).hexdigest()
    return md5_final


def derive_fernet_key(key_wording: str) -> bytes:
    """
    Convert the legacy MD5 hex string into a Fernet key.
    Fernet expects: urlsafe_base64encode(32 bytes).
    """
    legacy_hex = derive_legacy_md5_hex(key_wording)
    digest32 = hashlib.sha256(legacy_hex.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest32)


def encrypt_string(plain: str, fernet_key: bytes) -> str:
    if plain is None:
        return plain
    if plain == "":
        return ""
    f = Fernet(fernet_key)
    token = f.encrypt(plain.encode("utf-8")).decode("utf-8")
    return f"{ENC_PREFIX}{token}"


def decrypt_string(value: str, fernet_key: bytes) -> str:
    if value is None:
        return value
    if value == "":
        return ""
    if not value.startswith(ENC_PREFIX):
        return value
    token = value[len(ENC_PREFIX) :]
    f = Fernet(fernet_key)
    plain = f.decrypt(token.encode("utf-8")).decode("utf-8")
    return plain


def maybe_decrypt_field(value: str, fernet_key: Optional[bytes]) -> str:
    """
    - Plaintext stays plaintext
    - `ENC:` values are decrypted when a key is available
    - If encrypted but key is missing/invalid, returns the original value unchanged
    """
    if value is None or value == "":
        return value
    if not isinstance(value, str):
        return value
    if not value.startswith(ENC_PREFIX):
        return value
    if not fernet_key:
        return value
    try:
        return decrypt_string(value, fernet_key)
    except InvalidToken:
        return value


def maybe_encrypt_field(value: str, fernet_key: Optional[bytes]) -> str:
    """
    Encrypts only non-empty strings, skips already-encrypted values.
    If key is missing, returns the original value unchanged.
    """
    if value is None or value == "":
        return value
    if not isinstance(value, str):
        return value
    if value.startswith(ENC_PREFIX):
        return value
    if not fernet_key:
        return value
    return encrypt_string(value, fernet_key)


@dataclass(frozen=True)
class KeySource:
    key_wording: str

