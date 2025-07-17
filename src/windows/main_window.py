"""Main application window."""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAction,
    QDockWidget,
    QListWidget,
    QMainWindow,
    QMessageBox,
)

from ..database.database_manager import get_connection
from .patient_entry_window import PatientEntryWindow
from .patient_list_window import PatientListWindow
from .settings_window import SettingsWindow


class MainWindow(QMainWindow):
    """Main window with sidebar navigation."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Clinical Sabah")
        self.resize(800, 600)
        self.setup_sidebar()

    def setup_sidebar(self) -> None:
        dock = QDockWidget("Menu", self)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)
        menu = QListWidget()
        menu.addItems(["Patients", "Add Patient", "Settings", "Logout"])
        menu.currentRowChanged.connect(self.handle_menu)
        dock.setWidget(menu)

    def handle_menu(self, index: int) -> None:
        if index == 0:
            self.patients()
        elif index == 1:
            self.add_patient()
        elif index == 2:
            SettingsWindow(self).exec_()
        elif index == 3:
            self.close()

    def patients(self) -> None:
        self.list_win = PatientListWindow(self)
        self.list_win.show()

    def add_patient(self) -> None:
        dlg = PatientEntryWindow(self)
        dlg.exec_()
