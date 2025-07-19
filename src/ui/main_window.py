from __future__ import annotations

from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QStackedWidget, QWidget

from ..pages import (
    DashboardPage,
    PatientListPage,
    ReportsPage,
    SettingsPage,
    VisitsPage,
)
from ..widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    """Main window with sidebar navigation."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Clinical Sabah")
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)

        self.sidebar = Sidebar(
            [
                ("🏠 Dashboard", None, "dashboard"),
                ("👤 Patients", None, "patients"),
                ("📅 Visits", None, "visits"),
                ("📊 Reports", None, "reports"),
                ("⚙ Settings", None, "settings"),
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
        for page in self.pages.values():
            self.stack.addWidget(page)

        self.sidebar.page_selected.connect(self._set_page)
        self.sidebar.set_current("dashboard")

    def _set_page(self, key: str) -> None:
        if key == "logout":
            self.close()
            return
        widget = self.pages.get(key)
        if widget:
            if hasattr(widget, "load"):
                widget.load()  # type: ignore[attr-defined]
            if hasattr(widget, "refresh"):
                widget.refresh()  # type: ignore[attr-defined]
            self.stack.setCurrentWidget(widget)
