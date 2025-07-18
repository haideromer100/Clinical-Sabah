"""User registration dialog."""

from __future__ import annotations

from PyQt5.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from ..database.models import create_user, user_exists
from ..utils.validators import not_empty


class RegistrationWindow(QDialog):
    """Dialog to create a new user account."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register")
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.confirm = QLineEdit()
        self.confirm.setEchoMode(QLineEdit.Password)
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register)
        self.confirm.returnPressed.connect(self.register)

        layout = QFormLayout(self)
        layout.addRow("Username", self.username)
        layout.addRow("Password", self.password)
        layout.addRow("Confirm", self.confirm)
        layout.addRow(register_btn)

    def showEvent(self, event):
        super().showEvent(event)
        self.username.setFocus()

    def register(self) -> None:
        username = self.username.text()
        pwd = self.password.text()
        confirm = self.confirm.text()
        if not not_empty(username):
            QMessageBox.warning(self, "Error", "Username required")
            return
        if user_exists(username):
            QMessageBox.warning(self, "Error", "Username already exists")
            return
        if pwd != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
        if len(pwd) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return
        if create_user(username, pwd):
            QMessageBox.information(self, "Success", "Account created")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Could not create user")
