"""Settings window."""

from __future__ import annotations

import shutil
from pathlib import Path

from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
)

from ..database.database_manager import DB_PATH, get_connection
from ..utils.security import hash_password, verify_password


class SettingsWindow(QDialog):
    """Application settings, change password and backup."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.old_pwd = QLineEdit()
        self.old_pwd.setEchoMode(QLineEdit.Password)
        self.new_pwd = QLineEdit()
        self.new_pwd.setEchoMode(QLineEdit.Password)
        change_btn = QPushButton("Change Password")
        change_btn.clicked.connect(self.change_password)
        backup_btn = QPushButton("Backup DB")
        backup_btn.clicked.connect(self.backup_db)
        restore_btn = QPushButton("Restore DB")
        restore_btn.clicked.connect(self.restore_db)

        layout = QFormLayout(self)
        layout.addRow("Old Password", self.old_pwd)
        layout.addRow("New Password", self.new_pwd)
        layout.addRow(change_btn)
        layout.addRow(backup_btn)
        layout.addRow(restore_btn)

    def change_password(self) -> None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT password FROM users WHERE username='admin'"
            ).fetchone()
            if row and verify_password(self.old_pwd.text(), row[0]):
                conn.execute(
                    "UPDATE users SET password=? WHERE username='admin'",
                    (hash_password(self.new_pwd.text()),),
                )
                QMessageBox.information(self, "Success", "Password changed")
            else:
                QMessageBox.warning(self, "Error", "Old password incorrect")

    def backup_db(self) -> None:
        dest_dir = Path("data/backups")
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "clinic_backup.db"
        shutil.copy(DB_PATH, dest)
        QMessageBox.information(self, "Backup", f"Saved to {dest}")

    def restore_db(self) -> None:
        file, _ = QFileDialog.getOpenFileName(
            self, "Restore", str(Path("data/backups"))
        )
        if file:
            shutil.copy(file, DB_PATH)
            QMessageBox.information(self, "Restore", "Database restored")
