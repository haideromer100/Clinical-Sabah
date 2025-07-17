"""Security utils tests."""

from src.utils.security import hash_password, verify_password


def test_hash_verify_roundtrip():
    pwd = "secret"
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
    assert not verify_password("wrong", hashed)
