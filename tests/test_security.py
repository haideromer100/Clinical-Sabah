"""Security utils tests."""

from src.database import database_manager
from src.database.models import create_tables, create_user, user_exists
from src.utils.security import hash_password, verify_password


def test_hash_verify_roundtrip():
    pwd = "secret"
    pwd_hash, salt = hash_password(pwd)
    assert verify_password(pwd, pwd_hash, salt)
    assert not verify_password("wrong", pwd_hash, salt)


def test_create_user_and_verify(tmp_path, monkeypatch):
    db = tmp_path / "users.db"
    monkeypatch.setattr(database_manager, "DB_PATH", db)
    with database_manager.get_connection(db) as conn:
        create_tables(conn)
    assert create_user("alice", "pass123")
    assert user_exists("alice")
    with database_manager.get_connection(db) as conn:
        row = conn.execute(
            "SELECT password FROM users WHERE username='alice'"
        ).fetchone()
    stored_hash, salt = row[0].split(":")
    assert verify_password("pass123", stored_hash, salt)
