"""Patient entry and edit window."""

from __future__ import annotations

from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
)

from ..database.database_manager import get_connection
from ..utils.validators import not_empty
from .visit_dialog import VisitDialog


class PatientEntryWindow(QDialog):
    """Add or edit a patient."""

    def __init__(self, parent=None, patient_id: int | None = None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.name_edit = QLineEdit()
        self.age_edit = QLineEdit()
        self.contact_edit = QLineEdit()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        visit_btn = QPushButton("Add Visit")
        visit_btn.clicked.connect(self.add_visit)

        layout = QFormLayout(self)
        layout.addRow("Name", self.name_edit)
        layout.addRow("Age", self.age_edit)
        layout.addRow("Contact", self.contact_edit)
        layout.addRow(save_btn, visit_btn)

        if patient_id:
            self.load_patient()

    def load_patient(self) -> None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT name, age, contact FROM patients WHERE id=?", (self.patient_id,)
            ).fetchone()
            if row:
                self.name_edit.setText(row[0])
                self.age_edit.setText(str(row[1] or ""))
                self.contact_edit.setText(row[2] or "")

    def save(self) -> None:
        name = self.name_edit.text()
        if not not_empty(name):
            return
        age = self.age_edit.text() or None
        contact = self.contact_edit.text()
        with get_connection() as conn:
            if self.patient_id:
                conn.execute(
                    "UPDATE patients SET name=?, age=?, contact=? WHERE id=?",
                    (name, age, contact, self.patient_id),
                )
            else:
                cur = conn.execute(
                    "INSERT INTO patients (name, age, contact) VALUES (?, ?, ?)",
                    (name, age, contact),
                )
                self.patient_id = cur.lastrowid
        self.accept()

    def add_visit(self) -> None:
        if not self.patient_id:
            self.save()
        if self.patient_id:
            VisitDialog(self.patient_id, self).exec_()
