from __future__ import annotations

from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QLabel,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ..database.database_manager import get_connection


class PatientsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("PatientsView")
        layout = QVBoxLayout(self)

        self.toolbar = QToolBar()
        self.toolbar.setIconSize(QSize(16, 16))
        self.edit_action = self.toolbar.addAction("Edit")
        self.view_action = self.toolbar.addAction("View")
        self.delete_action = self.toolbar.addAction("Delete")
        layout.addWidget(self.toolbar)

        self.table = QTableView()
        layout.addWidget(self.table, 1)

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
