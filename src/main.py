from __future__ import annotations

import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from .database.migrations import init_schema
from .windows import LoginWindow

print(">>> main.py LOADED from:", __file__)  # ✅ طباعة موقع الملف

def main() -> None:
    init_schema()
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    # ✅ تحميل ملفات QSS
    style_path = Path(__file__).resolve().parent.parent / "assets" / "styles" / "app.qss"
    if style_path.exists():
        css = style_path.read_text(encoding="utf-8")
        print(">>> QSS length:", len(css))
        app.setStyleSheet("")  # مهم لإزالة أي ستايل قديم
        app.setStyleSheet(css)
    else:
        print(">>> QSS NOT FOUND:", style_path)

    # ✅ عرض نافذة تسجيل الدخول
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
