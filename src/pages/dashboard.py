from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ..utils.dashboard_stats import (
    get_patient_count,
    get_pending_reports,
    get_today_visits,
)


class InfoCard(QWidget):
    def __init__(self, title: str, value: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("InfoCard")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignHCenter)
        self.title_lbl = QLabel(title)
        self.title_lbl.setObjectName("title")
        self.value_lbl = QLabel(value)
        self.value_lbl.setObjectName("value")
        layout.addWidget(self.title_lbl, 0, Qt.AlignHCenter)
        layout.addWidget(self.value_lbl, 0, Qt.AlignHCenter)

    def set_value(self, value: str) -> None:
        self.value_lbl.setText(value)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        banner = QWidget()
        banner.setObjectName("Banner")
        b_layout = QHBoxLayout(banner)
        b_layout.setAlignment(Qt.AlignCenter)
        icon_lbl = QLabel("\U0001f6e1")  # shield unicode
        text_lbl = QLabel("YOU ARE PROTECTED")
        b_layout.addWidget(icon_lbl)
        b_layout.addWidget(text_lbl)
        layout.addWidget(banner, 0, Qt.AlignHCenter)

        cards = QHBoxLayout()
        cards.setSpacing(20)
        self.patients_card = InfoCard("Patients", str(get_patient_count()))
        self.visits_card = InfoCard("Today's Visits", str(get_today_visits()))
        self.reports_card = InfoCard("Reports", f"{get_pending_reports()} pending")
        cards.addWidget(self.patients_card)
        cards.addWidget(self.visits_card)
        cards.addWidget(self.reports_card)
        layout.addLayout(cards)
        layout.addStretch()

    def refresh(self) -> None:
        self.patients_card.set_value(str(get_patient_count()))
        self.visits_card.set_value(str(get_today_visits()))
        self.reports_card.set_value(f"{get_pending_reports()} pending")
