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
            pwd_hash, salt = hash_password("admin")
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                ("admin", f"{pwd_hash}:{salt}"),
            )

    # تأكد من وجود الأعمدة الجديدة
    add_serial_no_column()
    add_tooth_location_column()
    add_patient_extra_fields()
    add_created_at_column_to_files()  # ✅ مهم


def add_serial_no_column():
    """Add serial_no column to patients table if it doesn't exist."""
    with get_connection() as conn:
        existing = conn.execute("PRAGMA table_info(patients)").fetchall()
        columns = [col[1] for col in existing]
        if "serial_no" not in columns:
            conn.execute("ALTER TABLE patients ADD COLUMN serial_no TEXT")
            print("✅ تم إضافة العمود serial_no إلى جدول patients.")
        else:
            print("ℹ️ العمود serial_no موجود مسبقًا.")


def add_tooth_location_column():
    """Add tooth_location column to visits table if it doesn't exist."""
    with get_connection() as conn:
        existing = conn.execute("PRAGMA table_info(visits)").fetchall()
        columns = [col[1] for col in existing]
        if "tooth_location" not in columns:
            conn.execute("ALTER TABLE visits ADD COLUMN tooth_location TEXT")
            print("✅ تم إضافة العمود tooth_location إلى جدول visits.")
        else:
            print("ℹ️ العمود tooth_location موجود مسبقًا.")


def add_patient_extra_fields():
    """Add chief_complaint, medical_history, drugs_taken to patients if missing."""
    with get_connection() as conn:
        existing = conn.execute("PRAGMA table_info(patients)").fetchall()
        columns = [col[1] for col in existing]

        if "chief_complaint" not in columns:
            conn.execute("ALTER TABLE patients ADD COLUMN chief_complaint TEXT")
            print("✅ تم إضافة العمود chief_complaint إلى جدول patients.")
        else:
            print("ℹ️ العمود chief_complaint موجود مسبقًا.")

        if "medical_history" not in columns:
            conn.execute("ALTER TABLE patients ADD COLUMN medical_history TEXT")
            print("✅ تم إضافة العمود medical_history إلى جدول patients.")
        else:
            print("ℹ️ العمود medical_history موجود مسبقًا.")

        if "drugs_taken" not in columns:
            conn.execute("ALTER TABLE patients ADD COLUMN drugs_taken TEXT")
            print("✅ تم إضافة العمود drugs_taken إلى جدول patients.")
        else:
            print("ℹ️ العمود drugs_taken موجود مسبقًا.")


def add_created_at_column_to_files():
    """Add created_at column to patient_files if missing."""
    with get_connection() as conn:
        existing = conn.execute("PRAGMA table_info(patient_files)").fetchall()
        columns = [col[1] for col in existing]

        if "created_at" not in columns:
            conn.execute("ALTER TABLE patient_files ADD COLUMN created_at TEXT")
            print("✅ تم إضافة العمود created_at إلى جدول patient_files.")

            # تحديث السجلات الحالية بوقت الآن
            conn.execute("UPDATE patient_files SET created_at = datetime('now')")
            print("✅ تم تحديث created_at لجميع السجلات القديمة.")
        else:
            print("ℹ️ العمود created_at موجود مسبقًا.")


if __name__ == "__main__":
    add_serial_no_column()
    add_tooth_location_column()
    add_patient_extra_fields()
    add_created_at_column_to_files()
