"""Database tests."""

from __future__ import annotations

from pathlib import Path

from src.database.database_manager import DB_PATH, get_connection
from src.database.migrations import init_schema
from src.database.models import create_tables


def test_tables_exist(tmp_path):
    db = tmp_path / "test.db"
    with get_connection(db) as conn:
        create_tables(conn)
    with get_connection(db) as conn:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
    assert {"users", "patients", "visits", "patient_files"}.issubset(tables)


def test_crud(tmp_path):
    db = tmp_path / "crud.db"
    with get_connection(db) as conn:
        create_tables(conn)
        conn.execute("INSERT INTO patients (name) VALUES ('John')")
    with get_connection(db) as conn:
        row = conn.execute("SELECT name FROM patients WHERE name='John'").fetchone()
    assert row[0] == "John"
