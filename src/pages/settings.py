from __future__ import annotations

from PyQt5.QtWidgets import QFormLayout, QLineEdit, QMessageBox, QPushButton, QWidget

from ..database.database_manager import get_connection
from ..utils.security import hash_password, verify_password


class SettingsPage(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        form = QFormLayout(self)
        self.old_pwd = QLineEdit()
        self.old_pwd.setEchoMode(QLineEdit.Password)
        self.new_pwd = QLineEdit()
        self.new_pwd.setEchoMode(QLineEdit.Password)
        change_btn = QPushButton("Change Password")
        change_btn.clicked.connect(self.change_password)
        form.addRow("Old Password", self.old_pwd)
        form.addRow("New Password", self.new_pwd)
        form.addRow(change_btn)

    def change_password(self) -> None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT password FROM users WHERE username='admin'"
            ).fetchone()
        if row:
            stored_hash, salt = row[0].split(":")
            if verify_password(self.old_pwd.text(), stored_hash, salt):
                new_hash, new_salt = hash_password(self.new_pwd.text())
                with get_connection() as conn:
                    conn.execute(
                        "UPDATE users SET password=? WHERE username='admin'",
                        (f"{new_hash}:{new_salt}",),
                    )
                QMessageBox.information(self, "Success", "Password changed")
                return
        QMessageBox.warning(self, "Error", "Old password incorrect")
