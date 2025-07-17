"""GUI smoke tests using pytest-qt."""

import pytest

try:
    from PyQt5.QtWidgets import QApplication
except Exception:  # pragma: no cover - skip if PyQt5 missing
    PyQt5 = None  # type: ignore
else:
    PyQt5 = True

if PyQt5:
    from src.windows.login_window import LoginWindow


@pytest.mark.skipif(not PyQt5, reason="PyQt5 not installed")
def test_login_window_shows(qtbot):
    app = QApplication.instance() or QApplication([])
    win = LoginWindow()
    qtbot.addWidget(win)
    win.show()
    assert win.isVisible()
