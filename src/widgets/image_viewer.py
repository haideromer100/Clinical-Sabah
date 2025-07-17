"""Simple image viewer with zoom and pan."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class ImageViewer(QLabel):
    """Display an image with basic zoom capability."""

    def load(self, path: str) -> None:
        img = Image.open(Path(path))
        qt_img = QPixmap.fromImage(ImageQt(img))
        self.setPixmap(qt_img)
