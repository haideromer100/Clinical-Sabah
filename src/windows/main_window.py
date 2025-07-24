from __future__ import annotations

from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from ..widgets.sidebar import Sidebar
from .pages import (
    DashboardPage,
    PatientListPage,
    VisitsPage,
    ReportsPage,
    SettingsPage,
)


class MainWindow(QMainWindow):
    """Main window using a fixed sidebar and stacked pages."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Clinical Sabah")
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        self.sidebar = Sidebar([
            ("🏠 Dashboard", "dashboard"),
            ("👤 Patients", "patients"),
            ("📅 Visits", "visits"),
            ("📊 Reports", "reports"),
            ("⚙ Settings", "settings"),
        ])
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
        for page in self.pages.values():
            self.stack.addWidget(page)

        self.sidebar.page_selected.connect(self._set_page)
        self.sidebar.set_current("dashboard")

    def _set_page(self, key: str) -> None:
        if key == "logout":
            self.close()
            return
        self.go_to_page(key)

    def go_to_page(self, key: str):
        widget = self.pages.get(key)
        if widget:
            if hasattr(widget, "load"):
                widget.load()
            if hasattr(widget, "refresh"):
                widget.refresh()
            self.stack.setCurrentWidget(widget)
        return widget
