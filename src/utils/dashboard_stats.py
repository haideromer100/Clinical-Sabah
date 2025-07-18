from __future__ import annotations

from datetime import date

from ..database.database_manager import get_connection


def count_patients() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) FROM patients").fetchone()
    return int(row[0]) if row else 0


def count_today_visits() -> int:
    today = date.today().isoformat()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM visits WHERE visit_date=?",
            (today,),
        ).fetchone()
    return int(row[0]) if row else 0


def count_pending_reports() -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) FROM patient_files").fetchone()
    return int(row[0]) if row else 0


def get_patient_count() -> int:
    return count_patients()


def get_today_visits() -> int:
    return count_today_visits()


def get_pending_reports() -> int:
    return count_pending_reports()
