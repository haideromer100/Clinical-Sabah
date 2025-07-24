import os
from pathlib import Path

UNUSED_ENTRIES = [
    ("src/database/database_manager.py", ["exc_type", "tb"]),
    ("src/pages/patient_list.py", ["current_patient_id"]),
    ("src/pages/visits.py", ["QDialogVBoxLayout", "QPlainTextEdit"]),
    ("src/ui/dashboard_view.py", ["DashboardView"]),
    ("src/ui/patients_view.py", ["PatientsView", "edit_action", "view_action", "delete_action"]),
    ("src/ui/reports_view.py", ["ReportsView"]),
    ("src/ui/settings_view.py", ["SettingsView"]),
    ("src/ui/visits_view.py", ["VisitsView"]),
    ("src/utils/arabic_support.py", ["enable_rtl"]),
    ("src/utils/file_manager.py", ["store_file"]),
    ("src/utils/report_generator.py", ["generate_report", "width"]),
    ("src/utils/state.py", ["current_patient_id"]),
    ("src/widgets/custom_widgets.py", ["LabeledLineEdit", "HeaderLabel", "IconButton"]),
    ("src/widgets/image_viewer.py", ["ImageViewer"]),
    ("src/windows/patient_entry_window.py", ["ToothSurfaceDialog", "get_data"]),
]

def is_file_empty_or_useless(lines: list[str]) -> bool:
    """Check if file is empty or only has comments/empty lines."""
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            return False
    return True

for file_path, targets in UNUSED_ENTRIES:
    abs_path = Path(file_path).resolve()
    if not abs_path.exists():
        print(f"[❌ SKIPPED] {file_path} (not found)")
        continue

    with abs_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if any(target in line for target in targets):
            continue  # Remove unused line
        new_lines.append(line)

    if is_file_empty_or_useless(new_lines):
        abs_path.unlink()
        print(f"[🗑️ DELETED] {file_path} (file was empty or fully unused)")
    else:
        with abs_path.open("w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"[✅ CLEANED] {file_path}")
