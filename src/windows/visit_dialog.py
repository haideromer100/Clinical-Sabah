from __future__ import annotations

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..database.database_manager import get_connection


class VisitDialog(QDialog):
    """Add or edit a visit, supporting multiple teeth."""

    def __init__(self, patient_id: int, parent=None, visit_id: int | None = None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.visit_id = visit_id
        self.setWindowTitle("Edit Visit" if visit_id else "Add Visit")
        self.teeth_info = []

        # Widgets
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.side_combo = QComboBox()
        self.side_combo.addItems(["Right", "Left"])

        self.tooth_number_combo = QComboBox()
        self.tooth_number_combo.addItems([str(i) for i in range(1, 9)])

        self.surface_checkboxes = []
        surfaces = ["Mesial", "Distal", "Buccal", "Lingual", "Occlusal"]
        for surface in surfaces:
            cb = QCheckBox(surface)
            self.surface_checkboxes.append(cb)

        self.add_tooth_btn = QPushButton("Add Tooth")
        self.add_tooth_btn.clicked.connect(self.add_tooth_info)

        self.teeth_list = QListWidget()

        self.details_edit = QTextEdit()
        self.treatment_edit = QLineEdit()
        self.next_date_edit = QDateEdit()
        self.next_date_edit.setCalendarPopup(True)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save)

        # Layout
        layout = QFormLayout(self)
        layout.addRow("Date", self.date_edit)
        layout.addRow("Tooth Side", self.side_combo)
        layout.addRow("Tooth Number", self.tooth_number_combo)

        surface_layout = QHBoxLayout()
        for cb in self.surface_checkboxes:
            surface_layout.addWidget(cb)
        surface_widget = QWidget()
        surface_widget.setLayout(surface_layout)
        layout.addRow("Tooth Surfaces", surface_widget)

        layout.addRow(self.add_tooth_btn)
        layout.addRow("Added Teeth", self.teeth_list)
        layout.addRow("Details", self.details_edit)
        layout.addRow("Treatment", self.treatment_edit)
        layout.addRow("Next Appointment", self.next_date_edit)
        layout.addRow(save_btn)

        if self.visit_id:
            self.load_visit_data()

    def add_tooth_info(self):
        side = self.side_combo.currentText()
        number = self.tooth_number_combo.currentText()
        surfaces = [cb.text() for cb in self.surface_checkboxes if cb.isChecked()]
        if not surfaces:
            tooth_desc = f"{side} {number}"
        else:
            tooth_desc = f"{side} {number}: {', '.join(surfaces)}"

        self.teeth_info.append(tooth_desc)
        self.teeth_list.addItem(QListWidgetItem(tooth_desc))

        for cb in self.surface_checkboxes:
            cb.setChecked(False)

    def load_visit_data(self):
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT visit_date, visit_details, treatment_performed, next_appointment, tooth_location
                FROM visits
                WHERE id = ?
            """,
                (self.visit_id,),
            ).fetchone()

        if not row:
            return

        visit_date, details, treatment, next_date, tooth_info = row

        self.date_edit.setDate(QDate.fromString(visit_date, "yyyy-MM-dd"))
        self.details_edit.setPlainText(details or "")
        self.treatment_edit.setText(treatment or "")
        if next_date:
            self.next_date_edit.setDate(QDate.fromString(next_date, "yyyy-MM-dd"))

        self.teeth_info = []
        self.teeth_list.clear()
        if tooth_info:
            lines = tooth_info.strip().split("\n")
            for line in lines:
                if line.strip():
                    self.teeth_info.append(line.strip())
                    self.teeth_list.addItem(QListWidgetItem(line.strip()))

    def save(self) -> None:
        tooth_info_str = "\n".join(self.teeth_info) if self.teeth_info else ""

        data = (
            self.date_edit.date().toString("yyyy-MM-dd"),
            self.details_edit.toPlainText(),
            self.treatment_edit.text(),
            self.next_date_edit.date().toString("yyyy-MM-dd"),
            tooth_info_str,
        )

        with get_connection() as conn:
            if self.visit_id:
                conn.execute(
                    """
                    UPDATE visits
                    SET visit_date = ?, visit_details = ?, treatment_performed = ?, next_appointment = ?, tooth_location = ?
                    WHERE id = ?
                    """,
                    (*data, self.visit_id),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO visits (patient_id, visit_date, visit_details, treatment_performed, next_appointment, tooth_location)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (self.patient_id, *data),
                )
        self.accept()
