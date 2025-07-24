from __future__ import annotations
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QComboBox, QHBoxLayout
)
from ..database.database_manager import get_connection


class ReportsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # ===== عنوان الصفحة =====
        self.layout.addWidget(QLabel("📁 قائمة تقارير الأشعة والتحاليل:"))

        # ===== الفلاتر =====
        filter_layout = QHBoxLayout()
        self.patient_filter = QComboBox()
        self.type_filter = QComboBox()

        self.patient_filter.addItem("👤 جميع المرضى", None)
        self.type_filter.addItem("📄 كل الأنواع", None)
        self.type_filter.addItem("🦷 الأشعة (X-Rays)", "xrays")
        self.type_filter.addItem("🧪 التحاليل (Lab Results)", "lab_results")

        self.patient_filter.currentIndexChanged.connect(self.reload_reports)
        self.type_filter.currentIndexChanged.connect(self.reload_reports)

        filter_layout.addWidget(QLabel("فلترة حسب المريض:"))
        filter_layout.addWidget(self.patient_filter)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(QLabel("فلترة حسب النوع:"))
        filter_layout.addWidget(self.type_filter)

        self.layout.addLayout(filter_layout)

        # ===== منطقة عرض التقارير =====
        self.scroll = QScrollArea()
        self.container = QFrame()
        self.content = QVBoxLayout(self.container)
        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)

        self.layout.addWidget(self.scroll)
        self.layout.addStretch()

        self.load_patients()
        self.reload_reports()

    def load_patients(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT id, name FROM patients ORDER BY name").fetchall()
        for patient_id, name in rows:
            self.patient_filter.addItem(name, patient_id)

    def reload_reports(self):
        # تنظيف القائمة السابقة
        while self.content.count():
            item = self.content.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        selected_patient = self.patient_filter.currentData()
        selected_type = self.type_filter.currentData()

        query = """
            SELECT pf.id, patients.name, pf.file_type, pf.file_name, pf.file_path
            FROM patient_files pf
            JOIN patients ON patients.id = pf.patient_id
        """
        conditions = []
        params = []

        if selected_patient:
            conditions.append("pf.patient_id = ?")
            params.append(selected_patient)
        if selected_type:
            conditions.append("pf.file_type = ?")
            params.append(selected_type)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        query += " ORDER BY pf.id DESC"

        with get_connection() as conn:
            rows = conn.execute(query, params).fetchall()

        if not rows:
            self.content.addWidget(QLabel("⚠️ لا توجد تقارير مطابقة للفلاتر."))
        else:
            for _, patient_name, file_type, file_name, file_path in rows:
                label_text = f"{patient_name} | {file_type.upper()} | {file_name}"
                btn = QPushButton(label_text)
                btn.clicked.connect(lambda _, path=file_path: self.open_file(path))
                self.content.addWidget(btn)
    def filter_by_patient(self, patient_id: int):
        index = self.patient_filter.findData(patient_id)
        if index >= 0:
            self.patient_filter.setCurrentIndex(index)


    def open_file(self, path: str):
        abs_path = os.path.abspath(path)
        try:
            os.startfile(abs_path)
        except Exception as e:
            print(f"❌ فشل في فتح الملف: {e}")

