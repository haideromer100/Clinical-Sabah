from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from ...utils.dashboard_stats import (
    get_patient_count,
    get_pending_reports,
    get_today_visits,
)


def drop_shadow(blur=32, x=0, y=8, alpha=70) -> QGraphicsDropShadowEffect:
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setXOffset(x)
    eff.setYOffset(y)
    eff.setColor(QColor(0, 0, 0, alpha))
    return eff


def enable_bg(widget: QWidget) -> None:
    """Qt لا يرسم الخلفية من الـQSS إلا إذا وفّرنا WA_StyledBackground على Widgets المشتقة من QWidget."""
    widget.setAttribute(Qt.WA_StyledBackground, True)


class Banner(QWidget):
    """الشعار والنص الكبير."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("BannerWidget")
        enable_bg(self)                 # <<< مهم جداً
        self.setFixedHeight(180)

        h = QHBoxLayout(self)
        h.setContentsMargins(60, 36, 60, 36)
        h.setSpacing(28)
        h.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        icon = QLabel("🛡")
        icon.setObjectName("BannerIcon")

        text = QLabel("YOU ARE PROTECTED")
        text.setObjectName("BannerText")

        h.addWidget(icon)
        h.addWidget(text)
        h.addStretch()

        self.setGraphicsEffect(drop_shadow(blur=42, y=12, alpha=80))


class InfoCard(QWidget):
    """كارت إحصائية."""
    def __init__(self, emoji: str, title: str, value: str, subtitle: str | None = None, parent=None):
        super().__init__(parent)
        self.setObjectName("InfoCard")
        enable_bg(self)                 # <<< مهم جداً
        self.setMinimumSize(260, 190)

        v = QVBoxLayout(self)
        v.setContentsMargins(40, 30, 40, 30)
        v.setSpacing(8)
        v.setAlignment(Qt.AlignCenter)

        icon = QLabel(emoji)
        icon.setObjectName("CardIcon")

        self.value_lbl = QLabel(value)
        self.value_lbl.setObjectName("CardValue")

        title_lbl = QLabel(title)
        title_lbl.setObjectName("CardTitle")

        v.addWidget(icon)
        v.addWidget(title_lbl)
        v.addWidget(self.value_lbl)

        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("CardSubtitle")
            v.addWidget(sub)

        self.setGraphicsEffect(drop_shadow(blur=36, y=10, alpha=60))

    def set_value(self, val: str):
        self.value_lbl.setText(val)


class DashboardPage(QWidget):
    """صفحة اللوحة كما في التصميم."""

    def __init__(self):
        super().__init__()
        print(">>> DashboardPage LOADED from:", __file__)
        self.setObjectName("DashboardPage")
        enable_bg(self)  # ليس ضروريًا عادة، لكن لا يضر

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignTop)
        root.setContentsMargins(32, 24, 32, 32)
        root.setSpacing(0)

        # اللوحة البيضاء (Panel) التي تحتوي كل شيء
        self.panel = QFrame()
        self.panel.setObjectName("MainPanel")
        enable_bg(self.panel)           # <<< مهم جداً

        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(60, 50, 60, 60)
        self.panel_layout.setSpacing(40)
        self.panel_layout.setAlignment(Qt.AlignTop)

        # Banner داخل اللوحة
        self.banner = Banner(self.panel)
        self.panel_layout.addWidget(self.banner)

        # صف الكروت
        cards_row = QHBoxLayout()
        cards_row.setSpacing(36)
        cards_row.setAlignment(Qt.AlignHCenter)

        self.card_patients = InfoCard("👤", "Patients", str(get_patient_count()))
        self.card_visits   = InfoCard("📅", "Today's Visits", str(get_today_visits()))
        self.card_reports  = InfoCard("📊", "Reports", str(get_pending_reports()), "pending")

        for c in (self.card_patients, self.card_visits, self.card_reports):
            c.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            cards_row.addWidget(c)

        # مسافات مرنة يمين ويسار
        cards_row.insertSpacerItem(0, QSpacerItem(20, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        cards_row.addSpacerItem(QSpacerItem(20, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.panel_layout.addLayout(cards_row)

        # أضف اللوحة إلى الصفحة
        root.addWidget(self.panel, 0, Qt.AlignTop)
        root.addStretch()

        # ظل للوحة الكبيرة
        self.panel.setGraphicsEffect(drop_shadow(blur=60, y=18, alpha=45))

    def refresh(self):
        self.card_patients.set_value(str(get_patient_count()))
        self.card_visits.set_value(str(get_today_visits()))
        self.card_reports.set_value(str(get_pending_reports()))
