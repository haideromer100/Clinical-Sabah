from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QWidget,
    QComboBox,
    QDialog,
    QGroupBox,
)

from ..database.database_manager import get_connection
from ..windows.visit_dialog import VisitDialog


class VisitsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        # اختيار المريض
        top_layout = QHBoxLayout()
        self.patient_combo = QComboBox()
        self.patient_combo.currentIndexChanged.connect(self.load)
        self.add_btn = QPushButton("Add Visit")
        self.add_btn.clicked.connect(self.add_visit)
        top_layout.addWidget(QLabel("Patient:"))
        top_layout.addWidget(self.patient_combo)
        top_layout.addWidget(self.add_btn)
        self.layout.addLayout(top_layout)

        # بطاقة معلومات المريض
        self.patient_info_box = QGroupBox("🧾 Patient Info")
        self.patient_info_layout = QFormLayout()
        self.patient_info_box.setLayout(self.patient_info_layout)
        self.layout.addWidget(self.patient_info_box)

        # جدول الجلسات
        self.table = QTableView()
        self.table.doubleClicked.connect(self.handle_double_click)
        self.layout.addWidget(self.table)

        self._load_patients()
        self.load()

    def _load_patients(self) -> None:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, name FROM patients ORDER BY name"
            ).fetchall()
        self.patient_combo.clear()
        for r in rows:
            self.patient_combo.addItem(r[1], r[0])

    def load(self) -> None:
        patient_id = self.patient_combo.currentData()
        if patient_id is None:
            self.clear_table()
            self.clear_patient_info()
            return

        self.load_patient_info(patient_id)
        self.load_visits(patient_id)

    def load_patient_info(self, patient_id: int) -> None:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT name, age, sex, phone, marital_status,
                       chief_complaint, medical_history, drugs_taken
                FROM patients
                WHERE id = ?
            """,
                (patient_id,),
            ).fetchone()

        if not row:
            self.clear_patient_info()
            return

        fields = [
            ("Name", row[0]),
            ("Age", row[1]),
            ("Sex", row[2]),
            ("Phone", row[3]),
            ("Marital Status", row[4]),
            ("Chief Complaint", row[5]),
            ("Medical History", row[6]),
            ("Drugs Taken", row[7]),
        ]

        # تنظيف العرض السابق
        for i in reversed(range(self.patient_info_layout.count())):
            self.patient_info_layout.itemAt(i).widget().deleteLater()

        # عرض المعلومات
        for label, value in fields:
            field_label = QLabel(f"{label}:")
            field_value = QLabel(str(value))
            field_value.setWordWrap(True)
            self.patient_info_layout.addRow(field_label, field_value)

    def clear_patient_info(self):
        for i in reversed(range(self.patient_info_layout.count())):
            self.patient_info_layout.itemAt(i).widget().deleteLater()

    def load_visits(self, patient_id: int) -> None:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, visit_date, visit_details, tooth_location FROM visits WHERE patient_id=? ORDER BY visit_date",
                (patient_id,),
            ).fetchall()

        model = QtGui.QStandardItemModel(len(rows), 3)
        model.setHorizontalHeaderLabels(["Date", "Details", "Tooth Info"])
        self.visit_ids = []

        for row_idx, row in enumerate(rows):
            visit_id, date, details, tooth_info = row
            self.visit_ids.append(visit_id)
            for col_idx, value in enumerate([date, details, tooth_info]):
                if col_idx == 2 and value:
                    value = str(value).replace("; ", "\n")
                item = QtGui.QStandardItem(str(value))
                item.setEditable(False)
                item.setTextAlignment(Qt.AlignTop | Qt.AlignLeft)
                model.setItem(row_idx, col_idx, item)

        self.table.setModel(model)
        self.table.setWordWrap(True)
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)

    def clear_table(self):
        self.table.setModel(QtGui.QStandardItemModel(0, 0))

    def add_visit(self) -> None:
        patient_id = self.patient_combo.currentData()
        if patient_id is None:
            return
        dlg = VisitDialog(patient_id, self)
        if dlg.exec_():
            self.load()

    def handle_double_click(self, index) -> None:
        if not index.isValid() or not hasattr(self, "visit_ids"):
            return
        visit_id = self.visit_ids[index.row()]
        patient_id = self.patient_combo.currentData()
        dlg = VisitDialog(patient_id, self, visit_id=visit_id)
        dlg.exec_()
        self.load()
