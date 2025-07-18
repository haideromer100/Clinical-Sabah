import pytest

try:
    from PyQt5.QtWidgets import QApplication
except Exception:
    PYQT5 = False
else:
    PYQT5 = True

if PYQT5:
    from src.windows.main_window import MainWindow


@pytest.mark.skipif(not PYQT5, reason="PyQt5 not installed")
def test_sidebar_navigation(qtbot):
    app = QApplication.instance() or QApplication([])
    win = MainWindow()
    qtbot.addWidget(win)
    win.show()

    win.sidebar.buttons["patients"].click()
    assert win.stack.currentWidget() == win.pages["patients"]

    win.sidebar.buttons["dashboard"].click()
    assert win.stack.currentWidget() == win.pages["dashboard"]
