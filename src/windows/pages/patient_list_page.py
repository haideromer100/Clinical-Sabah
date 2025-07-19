from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtWidgets import QLineEdit, QTableView, QVBoxLayout, QWidget

from ..patient_entry_window import PatientEntryWindow
from ...database.database_manager import get_connection


class PatientListPage(QWidget):
    """Page listing patients in a table."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.search = QLineEdit()
        self.table = QTableView()
        self.table.doubleClicked.connect(self.edit_selected)
        layout.addWidget(self.search)
        layout.addWidget(self.table)
        self.load()

    def load(self) -> None:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, serial_no, name, phone FROM patients ORDER BY serial_no"
            ).fetchall()
        model = QtGui.QStandardItemModel(len(rows), 4)
        model.setHorizontalHeaderLabels(["ID", "Serial", "Name", "Phone"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QtGui.QStandardItem(str(value))
                model.setItem(row_idx, col_idx, item)
        self.table.setModel(model)

    def edit_selected(self) -> None:
        index = self.table.currentIndex()
        if not index.isValid():
            return
        model = self.table.model()
        patient_id = int(model.item(index.row(), 0).text())
        dlg = PatientEntryWindow(self, patient_id)
        dlg.exec_()
        self.load()
