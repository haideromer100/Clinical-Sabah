from __future__ import annotations

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class VisitsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("VisitsView")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Visits View"))
