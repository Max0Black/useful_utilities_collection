from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.ui.components import BasePage


class DashboardPage(BasePage):
    def __init__(self, context):
        super().__init__(context)


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

        cards.addWidget(self.keyboard_card, 0, 0)
        cards.addWidget(self.mouse_card, 0, 1)
        cards.addWidget(self.microphone_card, 1, 0, 1, 2)

        self.microphone_correction = QLabel("")
        self.microphone_correction.setObjectName("MutedText")
        self.microphone_correction.setStyleSheet("color: #58a6ff; font-weight: 500; margin-top: 4px;")
        self.microphone_correction.setWordWrap(True)
        self.microphone_card.layout().addWidget(self.microphone_correction)

        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addLayout(cards)
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
        svc = self.context.microphone_guard_service
        devices = svc._cached_devices or svc.list_devices()
        active_devices = [d for d in devices if svc.is_device_guard_enabled(d.device_id)]

        if devices:
            if guard_active:
                state_text = t("dashboard.microphone_state_active")
                self.microphone_value.setProperty("role", "success")

                # List active devices with details in the card body
                lines = []
                for d in active_devices:
                    name = d.display_name
                    if d.is_default:
                        name += f" ({t('microphone_guard.default_label')})"
                    lines.append(
                        "• " + t(
                            "dashboard.guard_text_active",
                            name=name,
                            level=d.current_level,
                            target=d.target_level,
                        )
                    )

                if lines:
                    self.microphone_body.setText("\n".join(lines))
                else:
                    self.microphone_body.setText(t("dashboard.microphone_body_inactive"))
            else:
                state_text = t("dashboard.microphone_state_inactive")
                self.microphone_value.setProperty("role", "neutral")
                self.microphone_body.setText(t("dashboard.microphone_body_inactive"))

            self.microphone_value.setText(state_text)
        else:
            self.microphone_value.setText(t("dashboard.microphone_state_unavailable"))
            self.microphone_value.setProperty("role", "danger")
            self.microphone_body.setText(t("dashboard.microphone_body_unavailable"))

        correction_time = self.context.microphone_guard_service.get_last_correction_text()
        self.microphone_correction.setText(
            t(
                "dashboard.last_correction",
                time=correction_time,
            )
        )

        self.repolish(
            self.keyboard_value,
            self.mouse_value,
            self.microphone_value,
        )