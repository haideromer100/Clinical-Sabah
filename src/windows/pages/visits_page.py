from __future__ import annotations

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class VisitsPage(QWidget):
    """Placeholder page for visit logs."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Visits Page"))
