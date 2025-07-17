"""Custom Qt widgets used across the application."""

from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget


class LabeledLineEdit(QWidget):
    """A line edit with a label."""

    def __init__(self, label: str, parent=None):
        super().__init__(parent)
        self.label = QLabel(label)
        self.edit = QLineEdit()
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.edit)


class HeaderLabel(QLabel):
    """Header styled label."""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-weight: bold; font-size: 18px;")


class IconButton(QPushButton):
    """A button with an icon."""

    def __init__(self, icon, tooltip: str = "", parent=None):
        super().__init__(parent)
        self.setIcon(icon)
        self.setToolTip(tooltip)
