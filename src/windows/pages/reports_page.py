
from __future__ import annotations
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from ...database.database_manager import get_connection


class ReportsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        scroll = QScrollArea()
        container = QFrame()
        content = QVBoxLayout(container)
        container.setLayout(content)

        layout.addWidget(QLabel("📁 قائمة تقارير الأشعة والتحاليل:"))

        with get_connection() as conn:
            # محاولة استخدام created_at، وإن فشل نحذفه من الاستعلام
            try:
                rows = conn.execute("SELECT pf.id, patients.name, pf.file_type, pf.file_name, pf.file_path FROM patient_files pf JOIN patients ON patients.id = pf.patient_id ORDER BY pf.created_at DESC").fetchall()
            except Exception:
                rows = conn.execute("SELECT pf.id, patients.name, pf.file_type, pf.file_name, pf.file_path FROM patient_files pf JOIN patients ON patients.id = pf.patient_id").fetchall()

        if not rows:
            content.addWidget(QLabel("⚠️ لا توجد تقارير حالياً."))
        else:
            for _, patient_name, file_type, file_name, file_path in rows:
                label_text = f"{patient_name} | {file_type.upper()} | {file_name}"
                btn = QPushButton(label_text)
                btn.clicked.connect(lambda _, path=file_path: self.open_file(path))
                content.addWidget(btn)

        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        layout.addStretch()

    def open_file(self, path: str):
        abs_path = os.path.abspath(path)
        try:
            os.startfile(abs_path)  # يعمل على Windows فقط
        except Exception as e:
            print(f"❌ فشل في فتح الملف: {e}")
