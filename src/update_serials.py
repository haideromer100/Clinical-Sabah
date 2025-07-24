# scripts/update_serials.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "clinic.db"

def update_serial_numbers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # التأكد من وجود العمود
    cursor.execute("PRAGMA table_info(patients)")
    columns = [col[1] for col in cursor.fetchall()]
    if "serial_no" not in columns:
        cursor.execute("ALTER TABLE patients ADD COLUMN serial_no TEXT")
        print("✅ تم إنشاء العمود serial_no.")

    # توليد الرقم التسلسلي
    cursor.execute("SELECT id FROM patients WHERE serial_no IS NULL OR serial_no = ''")
    patients = cursor.fetchall()
    for patient_id, in patients:
        cursor.execute("UPDATE patients SET serial_no = ? WHERE id = ?", (str(patient_id), patient_id))

    conn.commit()
    print(f"✅ تم تحديث {len(patients)} مريض بالرقم التسلسلي.")
    conn.close()

if __name__ == "__main__":
    update_serial_numbers()
