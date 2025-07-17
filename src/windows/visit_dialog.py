"""Dialog to add a visit."""

from __future__ import annotations

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QDateEdit,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
)

from ..database.database_manager import get_connection


class VisitDialog(QDialog):
    """Add visit dialog."""

    def __init__(self, patient_id: int, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.treatment_edit = QLineEdit()
        self.next_date_edit = QDateEdit()
        self.next_date_edit.setCalendarPopup(True)
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)

        layout = QFormLayout(self)
        layout.addRow("Date", self.date_edit)
        layout.addRow("Treatment", self.treatment_edit)
        layout.addRow("Next", self.next_date_edit)
        layout.addRow(save_btn)

    def save(self) -> None:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO visits (patient_id, visit_date, treatment, next_visit) VALUES (?, ?, ?, ?)",
                (
                    self.patient_id,
                    self.date_edit.date().toString("yyyy-MM-dd"),
                    self.treatment_edit.text(),
                    self.next_date_edit.date().toString("yyyy-MM-dd"),
                ),
            )
        self.accept()
