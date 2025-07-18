"""Window to list patients."""

from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QTableView, QVBoxLayout, QWidget

from ..database.database_manager import get_connection


class PatientListWindow(QWidget):
    """List patients with a table view."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Patients")
        layout = QVBoxLayout(self)
        self.search = QLineEdit()
        self.table = QTableView()
        layout.addWidget(self.search)
        layout.addWidget(self.table)
        self.load()

    def load(self) -> None:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, name, age, contact FROM patients"
            ).fetchall()
        model = QtGui.QStandardItemModel(len(rows), 4)
        model.setHorizontalHeaderLabels(["ID", "Name", "Age", "Contact"])
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                item = QtGui.QStandardItem(str(value))
                model.setItem(row_idx, col_idx, item)
        self.table.setModel(model)
