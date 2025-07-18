from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class BannerWidget(QWidget):
    """Top banner with shield icon and protection text."""

    def __init__(self, icon: str, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Banner")
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon).pixmap(64, 64))
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        layout.addWidget(icon_label)
        layout.addWidget(text_label)


class DashboardView(QWidget):
    """Main dashboard view with summary cards."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("DashboardView")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(30)

        banner = BannerWidget(":/icons/shield.svg", "YOU ARE\nPROTECTED")
        layout.addWidget(banner, 0, Qt.AlignHCenter)

        cards = QHBoxLayout()
        cards.setSpacing(20)
        cards.addWidget(self._card(":/icons/user.svg", "Patients", "125"))
        cards.addWidget(self._card(":/icons/calendar.svg", "Today's Visits", "4"))
        cards.addWidget(self._card(":/icons/report.svg", "Reports", "2 pending"))
        layout.addLayout(cards)
        layout.addStretch()

    def _card(self, icon: str, title: str, value: str) -> QWidget:
        card = QWidget()
        card.setObjectName("InfoCard")
        eff = QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=0, yOffset=2, color=Qt.gray
        )
        card.setGraphicsEffect(eff)

        v = QVBoxLayout(card)
        v.setAlignment(Qt.AlignHCenter)
        icon_lbl = QLabel()
        icon_lbl.setPixmap(QIcon(icon).pixmap(32, 32))
        title_lbl = QLabel(title)
        title_lbl.setObjectName("title")
        value_lbl = QLabel(value)
        value_lbl.setObjectName("value")
        v.addWidget(icon_lbl, 0, Qt.AlignHCenter)
        v.addWidget(title_lbl, 0, Qt.AlignHCenter)
        v.addWidget(value_lbl, 0, Qt.AlignHCenter)
        return card
