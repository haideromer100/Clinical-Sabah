"""Database connection manager."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DB_PATH = Path("data/clinic.db")


class DatabaseManager:
    """Context manager for SQLite connection with foreign keys enabled."""

    def __init__(self, db_path: Path = DB_PATH) -> None:
        self.db_path = db_path
        self.conn: sqlite3.Connection | None = None

    def __enter__(self) -> sqlite3.Connection:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.conn:
            if exc is None:
                self.conn.commit()
            self.conn.close()
            self.conn = None


@contextmanager
def get_connection(db_path: Path = DB_PATH) -> Iterator[sqlite3.Connection]:
    """Provide a context-managed connection."""
    with DatabaseManager(db_path) as conn:
        yield conn
