"""Arabic RTL support helpers."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


def enable_rtl(widget: QWidget) -> None:
    """Enable right-to-left layout for the given widget."""
    widget.setLayoutDirection(Qt.RightToLeft)
