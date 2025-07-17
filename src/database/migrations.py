"""Database migrations utilities."""

from __future__ import annotations

from pathlib import Path

from ..utils.security import hash_password
from .database_manager import DB_PATH, get_connection
from .models import create_tables


def init_schema(db_path: Path = DB_PATH) -> None:
    """Initialize database schema if database does not exist."""
    if not db_path.exists():
        db_path.parent.mkdir(parents=True, exist_ok=True)
        with get_connection(db_path) as conn:
            create_tables(conn)
            # Create default admin user with password 'admin'
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("admin", hash_password("admin")),
            )
