"""Main application window with sidebar navigation."""

from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from ..widgets.sidebar import Sidebar
from .pages import (
    DashboardPage,
    PatientListPage,
    ReportsPage,
    SettingsPage,
    VisitsPage,
)


class MainWindow(QMainWindow):
    """Main window using a fixed sidebar and stacked pages."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Clinical Sabah")
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        self.sidebar = Sidebar(
            [
                ("Dashboard", ":/icons/home.svg", "dashboard"),
                ("Patients", ":/icons/patients.svg", "patients"),
                ("Visits", ":/icons/visits.svg", "visits"),
                ("Reports", ":/icons/reports.svg", "reports"),
                ("Settings", ":/icons/settings.svg", "settings"),
            ]
        )
        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)
        self.pages = {
            "dashboard": DashboardPage(),
            "patients": PatientListPage(),
            "visits": VisitsPage(),
            "reports": ReportsPage(),
            "settings": SettingsPage(),
        }
        for p in self.pages.values():
            self.stack.addWidget(p)

        self.sidebar.page_selected.connect(self._set_page)
        self.sidebar.set_current("dashboard")

    def _set_page(self, key: str) -> None:
        if key == "logout":
            self.close()
            return
        widget = self.pages.get(key)
        if widget:
            self.stack.setCurrentWidget(widget)
