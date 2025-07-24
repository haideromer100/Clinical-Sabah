import os
import shutil
from pathlib import Path

# المسارات التي تحتوي على ملفات غير مستخدمة
paths_to_archive = [
    "src/pages/patient_list.py",
    "src/ui/dashboard_view.py",
    "src/ui/patients_view.py",
    "src/ui/reports_view.py",
    "src/ui/settings_view.py",
    "src/ui/visits_view.py",
    "src/utils/report_generator.py",
    "src/utils/state.py",
    "src/widgets/custom_widgets.py",
    "src/windows/patient_entry_window.py",
]

# مجلد الأرشيف
archive_dir = Path("archived_unused")
archive_dir.mkdir(exist_ok=True)

# أرشفة الملفات
for path in paths_to_archive:
    src = Path(path)
    if src.exists():
        dest = archive_dir / src.name
        shutil.move(str(src), str(dest))
        print(f"✔ Archived: {src} → {dest}")
    else:
        print(f"⚠ File not found, skipped: {src}")

print("\n✅ عملية الأرشفة اكتملت. تأكد من عمل التطبيق الآن.")
