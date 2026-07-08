from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.translation import t


class DashboardPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(18)

        # ── Header ───────────────────────────────────────────────────
        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")
        self.subtitle_label.setWordWrap(True)

        # ── Status cards ─────────────────────────────────────────────
        cards = QGridLayout()
        cards.setHorizontalSpacing(14)
        cards.setVerticalSpacing(14)

        (
            self.keyboard_card,
            self.keyboard_card_title,
            self.keyboard_icon,
            self.keyboard_value,
            self.keyboard_body,
        ) = self._create_card("⌨")

        (
            self.mouse_card,
            self.mouse_card_title,
            self.mouse_icon,
            self.mouse_value,
            self.mouse_body,
        ) = self._create_card("🖱")

        (
            self.microphone_card,
            self.microphone_card_title,
            self.microphone_icon,
            self.microphone_value,
            self.microphone_body,
        ) = self._create_card("🎙")

        # ── Microphone Guard Details Panel ───────────────────────────
        self.guard_panel = QFrame()
        self.guard_panel.setObjectName("Panel")

        guard_layout = QVBoxLayout(self.guard_panel)
        guard_layout.setContentsMargins(18, 18, 18, 18)
        guard_layout.setSpacing(10)

        self.guard_title = QLabel()
        self.guard_title.setObjectName("SectionTitle")

        self.guard_text = QLabel("")
        self.guard_text.setObjectName("MutedText")
        self.guard_text.setWordWrap(True)

        self.guard_correction = QLabel("")
        self.guard_correction.setObjectName("CardValue")
        self.guard_correction.setProperty("role", "accent")
        self.guard_correction.setWordWrap(True)

        guard_layout.addWidget(self.guard_title)
        guard_layout.addWidget(self.guard_text)
        guard_layout.addWidget(self.guard_correction)

        cards.addWidget(self.keyboard_card, 0, 0)
        cards.addWidget(self.mouse_card, 0, 1)
        cards.addWidget(self.microphone_card, 1, 0, 1, 2)

        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addLayout(cards)
        root.addWidget(self.guard_panel)
        root.addStretch()

        self.context.input_lock_service.state.changed.connect(self.refresh)
        self.context.state_changed.connect(self.refresh)
        self.refresh()

    def _create_card(self, icon: str):
        card = QFrame()
        card.setObjectName("Panel")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(6)

        header = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setObjectName("MutedText")
        icon_label.setStyleSheet("font-size: 18pt; background: transparent;")

        title = QLabel("")
        title.setObjectName("SectionTitle")

        header.addWidget(icon_label)
        header.addWidget(title)
        header.addStretch()

        value = QLabel("")
        value.setObjectName("CardValue")
        value.setProperty("role", "neutral")

        body = QLabel("")
        body.setObjectName("MutedText")
        body.setWordWrap(True)

        layout.addLayout(header)
        layout.addWidget(value)
        layout.addWidget(body)

        return card, title, icon_label, value, body

    def refresh(self) -> None:
        self.title_label.setText(t("dashboard.page_title"))
        self.subtitle_label.setText(t("dashboard.page_subtitle"))

        self.keyboard_card_title.setText(t("dashboard.keyboard_card_title"))
        self.mouse_card_title.setText(t("dashboard.mouse_card_title"))
        self.microphone_card_title.setText(t("dashboard.microphone_card_title"))
        self.guard_title.setText(t("dashboard.protection_section_title"))

        input_lock_state = self.context.input_lock_service.state
        keyboard_locked = input_lock_state.keyboard_locked()
        mouse_locked = input_lock_state.mouse_locked()

        if keyboard_locked:
            self.keyboard_value.setText(t("dashboard.locked"))
            self.keyboard_value.setProperty("role", "danger")
            self.keyboard_body.setText(t("dashboard.keyboard_locked_desc"))
        else:
            self.keyboard_value.setText(t("dashboard.unlocked"))
            self.keyboard_value.setProperty("role", "success")
            self.keyboard_body.setText(t("dashboard.keyboard_unlocked_desc"))

        if mouse_locked:
            self.mouse_value.setText(t("dashboard.locked"))
            self.mouse_value.setProperty("role", "danger")
            self.mouse_body.setText(t("dashboard.mouse_locked_desc"))
        else:
            self.mouse_value.setText(t("dashboard.unlocked"))
            self.mouse_value.setProperty("role", "success")
            self.mouse_body.setText(t("dashboard.mouse_unlocked_desc"))

        guard_active = self.context.microphone_guard_service._guard_enabled
        device = self.context.microphone_guard_service.get_device("default-capture")

        if device is not None:
            if guard_active:
                state_text = t("dashboard.microphone_state_active", level=device.current_level)
                self.microphone_value.setProperty("role", "success")
            else:
                state_text = t("dashboard.microphone_state_inactive", level=device.current_level)
                self.microphone_value.setProperty("role", "neutral")

            self.microphone_value.setText(state_text)
            self.microphone_body.setText(t("dashboard.microphone_body_active"))
            self.guard_text.setText(
                t(
                    "dashboard.guard_text_active",
                    name=device.display_name,
                    level=device.current_level,
                    target=device.target_level,
                )
            )
        else:
            self.microphone_value.setText(t("dashboard.microphone_state_unavailable"))
            self.microphone_value.setProperty("role", "danger")
            self.microphone_body.setText(t("dashboard.microphone_body_unavailable"))
            self.guard_text.setText(t("dashboard.guard_text_unavailable"))

        correction_time = self.context.microphone_guard_service.get_last_correction_text()
        self.guard_correction.setText(
            t(
                "dashboard.last_correction",
                time=correction_time,
            )
        )

        self._repolish(
            self.keyboard_value,
            self.mouse_value,
            self.microphone_value,
            self.guard_correction,
        )

    def _repolish(self, *widgets) -> None:
        for widget in widgets:
            self.style().unpolish(widget)
            self.style().polish(widget)
            widget.update()