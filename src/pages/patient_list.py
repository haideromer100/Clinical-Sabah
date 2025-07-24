# src/pages/patient_list.py
from __future__ import annotations
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout,
    QHeaderView, QAbstractItemView, QMessageBox
)
from ..windows.patient_entry_window import PatientEntryWindow
from ..database.database_manager import get_connection


class AppState:
    current_patient_id = None


class PatientListPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 ابحث عن مريض...")
        self.search_input.textChanged.connect(self.search_patient)
        layout.addWidget(self.search_input)

        self.counter = QLabel()
        layout.addWidget(self.counter)

        self.add_button = QPushButton("Add Patient")
        self.add_button.clicked.connect(self.add_patient)
        layout.addWidget(self.add_button)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Serial No", "Name", "Phone", "Actions"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.load()

    def load(self) -> None:
        self.table.setRowCount(0)
        try:
            with get_connection() as conn:
                rows = conn.execute(
                    "SELECT id, serial_no, name, phone FROM patients ORDER BY CAST(serial_no AS INTEGER)"
                ).fetchall()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error loading patients:\n{e}")
            return

        self.all_rows = rows
        self.populate_table(rows)

    def populate_table(self, rows):
        self.table.setRowCount(len(rows))
        for row_idx, (patient_id, serial_no, name, phone) in enumerate(rows):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(serial_no)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(phone))

            btn_edit = QPushButton("✏")
            btn_edit.clicked.connect(lambda _, pid=patient_id: self.edit_patient(pid))

            btn_view = QPushButton("👁")
            btn_view.clicked.connect(lambda _, pid=patient_id: self.view_patient(pid))

            btn_delete = QPushButton("❌")
            btn_delete.clicked.connect(lambda _, pid=patient_id: self.delete_patient(pid))

            action_layout = QHBoxLayout()
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_view)
            action_layout.addWidget(btn_delete)
            action_layout.setContentsMargins(0, 0, 0, 0)

            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row_idx, 3, action_widget)

        self.counter.setText(f"Patients: {len(rows)}")

    def add_patient(self) -> None:
        dlg = PatientEntryWindow(self)
        if dlg.exec_():
            self.load()

    def edit_patient(self, patient_id: int) -> None:
        dlg = PatientEntryWindow(self, patient_id)
        if dlg.exec_():
            self.load()

    def view_patient(self, patient_id: int) -> None:
        AppState.current_patient_id = patient_id
        main_window = self.window()
        if hasattr(main_window, "go_to_page"):
            visits_page = main_window.go_to_page("visits")
            if hasattr(visits_page, "filter_by_patient"):
                visits_page.filter_by_patient(patient_id)

            reports_page = main_window.pages.get("reports")
            if hasattr(reports_page, "filter_by_patient"):
                reports_page.filter_by_patient(patient_id)

    def delete_patient(self, patient_id: int) -> None:
        confirm = QMessageBox.question(
            self,
            "Delete Patient",
            f"Are you sure you want to delete patient ID {patient_id}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            try:
                with get_connection() as conn:
                    conn.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
                self.load()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete patient:\n{e}")

    def search_patient(self, text: str) -> None:
        filtered = []
        for row in self.all_rows:
            if any(text.lower() in str(cell).lower() for cell in row):
                filtered.append(row)
        self.populate_table(filtered)
