from __future__ import annotations

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings View"))
