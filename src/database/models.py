"""Database schema models."""

from __future__ import annotations

import sqlite3


def create_tables(conn: sqlite3.Connection) -> None:
    """Create tables in the SQLite database."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_no TEXT UNIQUE,
            name TEXT NOT NULL,
            age INTEGER,
            sex TEXT,
            phone TEXT,
            marital_status TEXT,
            chief_complaint TEXT,
            medical_history TEXT,
            drug_taken TEXT,
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            last_modified TEXT DEFAULT CURRENT_TIMESTAMP,
            created_by TEXT
        );

        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            visit_date TEXT NOT NULL,
            visit_details TEXT,
            treatment_performed TEXT,
            next_appointment TEXT,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS patient_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            file_type TEXT,
            file_name TEXT,
            file_path TEXT NOT NULL,
            upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
        );
        """
    )


def user_exists(username: str) -> bool:
    """Return True if a user with ``username`` exists."""
    from .database_manager import DB_PATH, get_connection

    with get_connection(DB_PATH) as conn:
        row = conn.execute(
            "SELECT 1 FROM users WHERE username=?",
            (username,),
        ).fetchone()
    return row is not None


def create_user(username: str, password_plain: str) -> bool:
    """Create a user if it doesn't exist. Return ``True`` on success."""
    from ..utils.security import hash_password
    from .database_manager import DB_PATH, get_connection

    if user_exists(username):
        return False
    pwd_hash, salt = hash_password(password_plain)
    try:
        with get_connection(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, f"{pwd_hash}:{salt}"),
            )
        return True
    except sqlite3.IntegrityError:
        return False
