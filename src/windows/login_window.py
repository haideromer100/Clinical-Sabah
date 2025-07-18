"""Login window."""

from __future__ import annotations

from PyQt5.QtCore import QPoint, QPropertyAnimation, Qt
from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from ..database.database_manager import get_connection
from ..utils.security import verify_password
from .main_window import MainWindow
from .registration_window import RegistrationWindow


class LoginWindow(QDialog):
    """User login dialog."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.handle_login)
        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.open_registration)

        self.password.returnPressed.connect(self.handle_login)

        self.username.returnPressed.connect(self.handle_login)
        register_btn.setAutoDefault(False)

        layout = QFormLayout(self)
        layout.addRow("Username", self.username)
        layout.addRow("Password", self.password)
        layout.addRow(login_btn, register_btn)

    def showEvent(self, event):
        super().showEvent(event)
        self.username.setFocus()

    def handle_login(self) -> None:
        username = self.username.text()
        pwd = self.password.text()
        with get_connection() as conn:
            row = conn.execute(
                "SELECT password FROM users WHERE username=?",
                (username,),
            ).fetchone()
        if row:
            stored_hash, salt = row[0].split(":")
            if verify_password(pwd, stored_hash, salt):
                self.accept()
                self.main_win = MainWindow()
                self.main_win.show()
                self.close()
                return
        self.shake()
        QMessageBox.warning(self, "Error", "Invalid credentials")

    def open_registration(self) -> None:
        RegistrationWindow(self).exec_()

    def shake(self) -> None:
        self._shake_anim = QPropertyAnimation(self, b"pos")
        self._shake_anim.setDuration(200)
        self._shake_anim.setLoopCount(3)
        start = self.pos()
        self._shake_anim.setKeyValueAt(0, start)
        self._shake_anim.setKeyValueAt(0.25, start + QPoint(-10, 0))
        self._shake_anim.setKeyValueAt(0.5, start + QPoint(10, 0))
        self._shake_anim.setKeyValueAt(0.75, start + QPoint(-10, 0))
        self._shake_anim.setKeyValueAt(1, start)
        self._shake_anim.start()
