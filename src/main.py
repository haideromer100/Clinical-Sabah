"""Application entry point."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from .database.migrations import init_schema
from .windows import LoginWindow


def main() -> None:
    """Launch the Clinical Sabah application."""
    init_schema()
    app = QApplication(sys.argv)
    style_path = Path("assets/styles/app.qss")
    if style_path.exists():
        with open(style_path) as f:
            app.setStyleSheet(f.read())
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
