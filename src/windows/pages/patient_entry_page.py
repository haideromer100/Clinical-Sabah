from __future__ import annotations

from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ...database.database_manager import get_connection
from ...utils.validators import not_empty
from ..visit_dialog import VisitDialog


class PatientEntryPage(QWidget):
    """Page to add or edit a patient."""

    def __init__(
        self, patient_id: int | None = None, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.patient_id = patient_id
        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.serial_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.age_edit = QLineEdit()
        self.sex_combo = QComboBox()
        self.sex_combo.addItems(["Male", "Female"])
        self.phone_edit = QLineEdit()
        self.marital_combo = QComboBox()
        self.marital_combo.addItems(["Single", "Married"])
        self.chief_edit = QTextEdit()
        self.med_history_edit = QTextEdit()
        self.drugs_edit = QTextEdit()

        form.addRow("Serial No.", self.serial_edit)
        form.addRow("Name", self.name_edit)
        form.addRow("Age", self.age_edit)
        form.addRow("Sex", self.sex_combo)
        form.addRow("Phone", self.phone_edit)
        form.addRow("Marital Status", self.marital_combo)
        form.addRow("Chief Complaint", self.chief_edit)
        form.addRow("Medical History", self.med_history_edit)
        form.addRow("Drugs Taken", self.drugs_edit)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        visit_btn = QPushButton("Add Visit")
        visit_btn.clicked.connect(self.add_visit)
        btn_row.addWidget(save_btn)
        btn_row.addWidget(visit_btn)
        layout.addLayout(btn_row)

        if patient_id:
            self.load_patient()

    def load_patient(self) -> None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT serial_no, name, age, sex, phone, marital_status, chief_complaint, medical_history, drug_taken FROM patients WHERE id=?",
                (self.patient_id,),
            ).fetchone()
        if row:
            (
                serial_no,
                name,
                age,
                sex,
                phone,
                marital_status,
                chief,
                med_hist,
                drugs,
            ) = row
            self.serial_edit.setText(serial_no or "")
            self.name_edit.setText(name)
            self.age_edit.setText(str(age or ""))
            if sex:
                idx = self.sex_combo.findText(sex)
                if idx >= 0:
                    self.sex_combo.setCurrentIndex(idx)
            self.phone_edit.setText(phone or "")
            if marital_status:
                idx = self.marital_combo.findText(marital_status)
                if idx >= 0:
                    self.marital_combo.setCurrentIndex(idx)
            self.chief_edit.setPlainText(chief or "")
            self.med_history_edit.setPlainText(med_hist or "")
            self.drugs_edit.setPlainText(drugs or "")

    def save(self) -> None:
        name = self.name_edit.text()
        if not not_empty(name):
            return
        age = self.age_edit.text() or None
        serial_no = self.serial_edit.text() or None
        sex = self.sex_combo.currentText()
        phone = self.phone_edit.text()
        marital = self.marital_combo.currentText()
        chief = self.chief_edit.toPlainText()
        med_hist = self.med_history_edit.toPlainText()
        drugs = self.drugs_edit.toPlainText()
        with get_connection() as conn:
            if self.patient_id:
                conn.execute(
                    "UPDATE patients SET serial_no=?, name=?, age=?, sex=?, phone=?, marital_status=?, chief_complaint=?, medical_history=?, drug_taken=?, last_modified=CURRENT_TIMESTAMP WHERE id=?",
                    (
                        serial_no,
                        name,
                        age,
                        sex,
                        phone,
                        marital,
                        chief,
                        med_hist,
                        drugs,
                        self.patient_id,
                    ),
                )
            else:
                cur = conn.execute(
                    "INSERT INTO patients (serial_no, name, age, sex, phone, marital_status, chief_complaint, medical_history, drug_taken, created_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        serial_no,
                        name,
                        age,
                        sex,
                        phone,
                        marital,
                        chief,
                        med_hist,
                        drugs,
                        "admin",
                    ),
                )
                self.patient_id = cur.lastrowid

    def add_visit(self) -> None:
        if not self.patient_id:
            self.save()
        if self.patient_id:
            VisitDialog(self.patient_id, self).exec_()
