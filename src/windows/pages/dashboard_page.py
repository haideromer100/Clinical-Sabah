from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from ...utils.dashboard_stats import (
    get_patient_count,
    get_pending_reports,
    get_today_visits,
)


class BannerWidget(QWidget):
    def __init__(self, icon: str, text: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("Banner")
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        icon_label = QLabel()
        icon_label.setPixmap(QIcon(icon).pixmap(64, 64))
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        layout.addWidget(text_label)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Page")
        layout = QVBoxLayout(self)
        banner = BannerWidget(":/icons/shield.svg", "YOU ARE\nPROTECTED")
        layout.addWidget(banner, 0, Qt.AlignHCenter)

        h = QHBoxLayout()
        h.addWidget(
            self._card(":/icons/patients.svg", "Patients", str(get_patient_count()))
        )
        h.addWidget(
            self._card(":/icons/visits.svg", "Today's Visits", str(get_today_visits()))
        )
        h.addWidget(
            self._card(
                ":/icons/reports.svg",
                "Reports",
                f"{get_pending_reports()} pending",
            )
        )
        layout.addLayout(h)

    def _card(self, icon: str, title: str, value: str) -> QWidget:
        card = QWidget()
        card.setObjectName("InfoCard")
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
