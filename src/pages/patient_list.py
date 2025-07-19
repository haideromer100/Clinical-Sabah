from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLabel, QTableView, QVBoxLayout, QWidget

from ..database.database_manager import get_connection
from ..windows.patient_entry_window import PatientEntryWindow


class PatientListPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.counter = QLabel()
        layout.addWidget(self.counter)
        self.table = QTableView()
        self.table.doubleClicked.connect(self.edit_selected)
        layout.addWidget(self.table)
        self.load()

    def load(self) -> None:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, serial_no, name, phone FROM patients ORDER BY serial_no"
            ).fetchall()
        model = QtGui.QStandardItemModel(len(rows), 5)
        model.setHorizontalHeaderLabels(
            [
                "ID",
                "Serial",
                "Name",
                "Phone",
                "Actions",
            ]
        )
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QtGui.QStandardItem(str(value))
                item.setEditable(False)
                model.setItem(row_idx, col_idx, item)
            action_item = QtGui.QStandardItem("✏ 👁 📁 🖨 ❌")
            action_item.setEditable(False)
            model.setItem(row_idx, 4, action_item)
        self.table.setModel(model)
        self.counter.setText(f"Patients: {len(rows)}")

    def edit_selected(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return
        model = self.table.model()
        patient_id = int(model.item(index.row(), 0).text())
        dlg = PatientEntryWindow(self, patient_id)
        dlg.exec_()
        self.load()
