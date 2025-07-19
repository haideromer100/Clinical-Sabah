from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtWidgets import (
    QComboBox,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ..database.database_manager import get_connection
from ..windows.visit_dialog import VisitDialog


class VisitsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        top = QVBoxLayout()
        self.patient_combo = QComboBox()
        self.patient_combo.currentIndexChanged.connect(self.load)
        self.add_btn = QPushButton("Add Visit")
        self.add_btn.clicked.connect(self.add_visit)
        top.addWidget(QLabel("Patient:"))
        top.addWidget(self.patient_combo)
        top.addWidget(self.add_btn)
        layout.addLayout(top)
        self.table = QTableView()
        layout.addWidget(self.table)
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
            model = QtGui.QStandardItemModel(0, 0)
            self.table.setModel(model)
            return
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT visit_date, visit_details FROM visits WHERE patient_id=? ORDER BY visit_date",
                (patient_id,),
            ).fetchall()
        model = QtGui.QStandardItemModel(len(rows), 2)
        model.setHorizontalHeaderLabels(["Date", "Details"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QtGui.QStandardItem(str(value))
                item.setEditable(False)
                model.setItem(row_idx, col_idx, item)
        self.table.setModel(model)

    def add_visit(self) -> None:
        patient_id = self.patient_combo.currentData()
        if patient_id is None:
            return
        dlg = VisitDialog(patient_id, self)
        dlg.exec_()
        self.load()
