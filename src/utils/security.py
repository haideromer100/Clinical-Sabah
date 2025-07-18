"""Security utilities for password hashing."""

from __future__ import annotations

import hashlib
import os


def hash_password(pwd: str) -> tuple[str, str]:
    """Return SHA-256 hash and hex salt for ``pwd``."""
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.sha256(bytes.fromhex(salt) + pwd.encode()).hexdigest()
    return pwd_hash, salt


def verify_password(pwd: str, pwd_hash: str, salt: str) -> bool:
    """Verify ``pwd`` against stored hash and salt."""
    new_hash = hashlib.sha256(bytes.fromhex(salt) + pwd.encode()).hexdigest()
    return new_hash == pwd_hash
