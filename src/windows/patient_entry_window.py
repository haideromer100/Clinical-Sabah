"""Patient entry and edit window."""

from __future__ import annotations

from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
)

from ..database.database_manager import get_connection
from ..utils.validators import not_empty
from .visit_dialog import VisitDialog


class PatientEntryWindow(QDialog):
    """Add or edit a patient."""

    def __init__(self, parent=None, patient_id: int | None = None):
        super().__init__(parent)
        self.patient_id = patient_id
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
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)
        visit_btn = QPushButton("Add Visit")
        visit_btn.clicked.connect(self.add_visit)
        xray_btn = QPushButton("Upload X-Ray")
        xray_btn.clicked.connect(self.upload_xray)
        lab_btn = QPushButton("Upload Lab Result")
        lab_btn.clicked.connect(self.upload_lab)

        layout = QFormLayout(self)
        layout.addRow("Serial No.", self.serial_edit)
        layout.addRow("Name", self.name_edit)
        layout.addRow("Age", self.age_edit)
        layout.addRow("Sex", self.sex_combo)
        layout.addRow("Phone", self.phone_edit)
        layout.addRow("Marital Status", self.marital_combo)
        layout.addRow("Chief Complaint", self.chief_edit)
        layout.addRow("Medical History", self.med_history_edit)
        layout.addRow("Drugs Taken", self.drugs_edit)
        layout.addRow(save_btn, visit_btn)
        layout.addRow(xray_btn, lab_btn)

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
        self.accept()

    def add_visit(self) -> None:
        if not self.patient_id:
            self.save()
        if self.patient_id:
            VisitDialog(self.patient_id, self).exec_()

    def _store_file(self, path: str, file_type: str) -> None:
        import shutil
        from pathlib import Path

        serial = self.serial_edit.text() or str(self.patient_id)
        base = Path("data/patients") / serial / file_type
        base.mkdir(parents=True, exist_ok=True)
        src = Path(path)
        dest = base / src.name
        shutil.copy(src, dest)
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO patient_files (patient_id, file_type, file_name, file_path) VALUES (?, ?, ?, ?)",
                (self.patient_id, file_type, src.name, str(dest)),
            )

    def upload_xray(self) -> None:
        from PyQt5.QtWidgets import QFileDialog

        if not self.patient_id:
            self.save()
        if not self.patient_id:
            return
        fname, _ = QFileDialog.getOpenFileName(self, "Select X-Ray")
        if fname:
            self._store_file(fname, "xrays")

    def upload_lab(self) -> None:
        from PyQt5.QtWidgets import QFileDialog

        if not self.patient_id:
            self.save()
        if not self.patient_id:
            return
        fname, _ = QFileDialog.getOpenFileName(self, "Select Lab Result")
        if fname:
            self._store_file(fname, "lab_results")
