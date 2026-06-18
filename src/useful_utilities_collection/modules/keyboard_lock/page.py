from PySide6.QtCore import QEasingCurve, Property, QPropertyAnimation, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget

from useful_utilities_collection.modules.keyboard_lock.controller import KeyboardLockController


class StatusIndicator(QFrame):
    def __init__(self):
        super().__init__()
        self._accent = QColor("#6e7681")
        self.setMinimumHeight(14)
        self.setMaximumHeight(14)

    def get_accent(self):
        return self._accent

    def set_accent(self, color):
        self._accent = color
        self.update()

    accent = Property(QColor, get_accent, set_accent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._accent)
        painter.drawRoundedRect(self.rect(), 7, 7)


class KeyboardLockPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.controller = KeyboardLockController(context)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        title = QLabel("Keyboard Lock")
        title.setObjectName("PageTitle")

        subtitle = QLabel("Lock the keyboard while keeping the mouse active.")
        subtitle.setObjectName("MutedText")

        self.feedback_panel = QFrame()
        self.feedback_panel.setObjectName("Panel")

        panel_layout = QVBoxLayout(self.feedback_panel)
        panel_layout.setContentsMargins(18, 18, 18, 18)
        panel_layout.setSpacing(10)

        self.status_indicator = StatusIndicator()

        self.status_label = QLabel()
        self.status_label.setObjectName("CardValue")

        self.info_label = QLabel()
        self.info_label.setObjectName("MutedText")
        self.info_label.setWordWrap(True)

        panel_layout.addWidget(self.status_indicator)
        panel_layout.addWidget(self.status_label)
        panel_layout.addWidget(self.info_label)

        self.toggle_button = QPushButton()
        self.toggle_button.setObjectName("PrimaryButton")
        self.toggle_button.clicked.connect(self.on_toggle)

        self.animation = QPropertyAnimation(self.status_indicator, b"accent")
        self.animation.setDuration(260)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.feedback_panel)
        layout.addWidget(self.toggle_button)
        layout.addStretch()

        self.context.state_changed.connect(self.refresh)
        self.refresh()

    def on_toggle(self) -> None:
        self.controller.toggle()

    def refresh(self) -> None:
        if self.context.state.keyboard_locked:
            self.status_label.setText("Keyboard is locked")
            self.status_label.setProperty("role", "danger")
            self.info_label.setText(
                "Keyboard input is currently blocked. Mouse input remains active."
            )
            self.toggle_button.setText("Unlock Keyboard")
            self.animate_indicator(QColor("#6e7681"), QColor("#f85149"))
        else:
            self.status_label.setText("Keyboard is unlocked")
            self.status_label.setProperty("role", "success")
            self.info_label.setText(
                "Keyboard input is active. Press the button below to lock the keyboard."
            )
            self.toggle_button.setText("Lock Keyboard")
            self.animate_indicator(QColor("#f85149"), QColor("#2ea043"))

        self.style().unpolish(self.status_label)
        self.style().polish(self.status_label)

    def animate_indicator(self, start: QColor, end: QColor) -> None:
        self.animation.stop()
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()