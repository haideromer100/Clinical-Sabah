from __future__ import annotations

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QStyle, QVBoxLayout, QWidget


class SidebarButton(QPushButton):
    """Button used inside the sidebar."""

    def __init__(
        self,
        text: str,
        key: str,
        icon: QStyle.StandardPixmap | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(text, parent)
        self.key = key
        if icon is not None:
            self.setIcon(self.style().standardIcon(icon))
        self.setCheckable(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setProperty("selected", False)

    def set_selected(self, state: bool) -> None:
        self.setChecked(state)
        self.setProperty("selected", "true" if state else "false")
        self.style().unpolish(self)
        self.style().polish(self)


class Sidebar(QWidget):
    """Fixed navigation sidebar."""

    page_selected = pyqtSignal(str)

    def __init__(
        self,
        items: list[tuple[str, QStyle.StandardPixmap | None, str]],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(200)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.buttons: dict[str, SidebarButton] = {}
        for text, icon, key in items:
            btn = SidebarButton(text, key, icon, self)
            btn.clicked.connect(self._handle_click)
            layout.addWidget(btn)
            self.buttons[key] = btn
        layout.addStretch()
        logout_btn = SidebarButton("🚪 Logout", "logout", None, self)
        layout.addWidget(logout_btn)
        self.buttons["logout"] = logout_btn
        logout_btn.clicked.connect(lambda: self.page_selected.emit("logout"))

    def _handle_click(self) -> None:
        btn: SidebarButton = self.sender()  # type: ignore
        if not isinstance(btn, SidebarButton):
            return
        self.set_current(btn.key)
        self.page_selected.emit(btn.key)

    def set_current(self, key: str) -> None:
        for b in self.buttons.values():
            b.set_selected(False)
        if key in self.buttons:
            self.buttons[key].set_selected(True)
