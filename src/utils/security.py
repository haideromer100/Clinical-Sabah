"""Security utilities for password hashing."""

from __future__ import annotations

import hashlib
import os


def hash_password(pwd: str) -> str:
    """Hash password with SHA-256 and a 16-byte salt."""
    salt = os.urandom(16)
    hashed = hashlib.sha256(salt + pwd.encode()).hexdigest()
    return salt.hex() + hashed


def verify_password(pwd: str, hashed: str) -> bool:
    """Verify a password against the hashed value."""
    salt = bytes.fromhex(hashed[:32])
    stored_hash = hashed[32:]
    new_hash = hashlib.sha256(salt + pwd.encode()).hexdigest()
    return new_hash == stored_hash
