"""Application entry point."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from .database.migrations import init_schema
from .windows import LoginWindow


def main() -> None:
    """Launch the Clinical Sabah application."""
    init_schema()
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    style_path = (
        Path(__file__).resolve().parent.parent / "assets" / "styles" / "app.qss"
    )
    if style_path.exists():
        with open(style_path) as f:
            app.setStyleSheet(f.read())
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
