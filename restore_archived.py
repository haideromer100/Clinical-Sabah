import shutil
from pathlib import Path

# مجلد الأرشيف
archive_dir = Path("archived_unused")

# قائمة الملفات الأصلية ومساراتها قبل الأرشفة
original_paths = {
    "patient_list.py": "src/pages/",
    "dashboard_view.py": "src/ui/",
    "patients_view.py": "src/ui/",
    "reports_view.py": "src/ui/",
    "settings_view.py": "src/ui/",
    "visits_view.py": "src/ui/",
    "report_generator.py": "src/utils/",
    "state.py": "src/utils/",
    "custom_widgets.py": "src/widgets/",
    "patient_entry_window.py": "src/windows/",
}

# تنفيذ الاسترجاع
for file_name, original_folder in original_paths.items():
    src = archive_dir / file_name
    dest = Path(original_folder) / file_name
    if src.exists():
        shutil.move(str(src), str(dest))
        print(f"✔ Restored: {src} → {dest}")
    else:
        print(f"⚠ File not found in archive: {src}")

print("\n✅ تمت استعادة جميع الملفات المؤرشفة.")
