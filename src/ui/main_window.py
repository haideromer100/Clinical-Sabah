from __future__ import annotations

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
)
from PyQt5.QtGui import QIcon

from .dashboard_view import DashboardView
from .patients_view import PatientsView
from .visits_view import VisitsView
from .reports_view import ReportsView
from .settings_view import SettingsView


class NavigationButton(QPushButton):
    def __init__(self, text: str, icon: str, key: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.key = key
        self.setIcon(QIcon(icon))
        self.setCheckable(True)
        self.setProperty("selected", False)

    def set_selected(self, state: bool) -> None:
        self.setChecked(state)
        self.setProperty("selected", "true" if state else "false")
        self.style().unpolish(self)
        self.style().polish(self)


class NavigationPane(QWidget):
    page_selected = pyqtSignal(str)

    def __init__(self, items: list[tuple[str, str, str]], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("NavigationPane")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.buttons: dict[str, NavigationButton] = {}
        for text, icon, key in items:
            btn = NavigationButton(text, icon, key, self)
            btn.clicked.connect(self._on_click)
            layout.addWidget(btn)
            self.buttons[key] = btn
        layout.addStretch()

    def _on_click(self) -> None:
        btn: NavigationButton = self.sender()  # type: ignore
        if not isinstance(btn, NavigationButton):
            return
        self.set_current(btn.key)
        self.page_selected.emit(btn.key)

    def set_current(self, key: str) -> None:
        for b in self.buttons.values():
            b.set_selected(False)
        if key in self.buttons:
            self.buttons[key].set_selected(True)


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Clinical Sabah")

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)

        self.sidebar = NavigationPane(
            [
                ("Dashboard", ":/icons/home.svg", "dashboard"),
                ("Patients", ":/icons/user.svg", "patients"),
                ("Visits", ":/icons/calendar.svg", "visits"),
                ("Reports", ":/icons/report.svg", "reports"),
                ("Settings", ":/icons/settings.svg", "settings"),
            ]
        )
        root.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        self.pages = {
            "dashboard": DashboardView(),
            "patients": PatientsView(),
            "visits": VisitsView(),
            "reports": ReportsView(),
            "settings": SettingsView(),
        }
        for page in self.pages.values():
            self.stack.addWidget(page)

        self.sidebar.page_selected.connect(self.show_page)
        self.sidebar.set_current("dashboard")
        self.stack.setCurrentWidget(self.pages["dashboard"])

    def show_page(self, key: str) -> None:
        widget = self.pages.get(key)
        if widget:
            self.stack.setCurrentWidget(widget)
