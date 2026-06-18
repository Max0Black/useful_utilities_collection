from PySide6.QtWidgets import QFrame, QLabel, QGridLayout, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel("A compact overview of the current utility state.")
        subtitle.setObjectName("MutedText")

        cards = QGridLayout()
        cards.setHorizontalSpacing(16)
        cards.setVerticalSpacing(16)

        self.keyboard_status_card = self._create_card(
            "Keyboard Lock",
            "Current keyboard input state.",
        )
        self.keyboard_status_value = self.keyboard_status_card.findChild(QLabel, "CardValue")

        self.mouse_status_card = self._create_card(
            "Mouse Access",
            "Mouse stays available while the keyboard is locked.",
        )
        self.mouse_status_value = self.mouse_status_card.findChild(QLabel, "CardValue")

        self.microphone_guard_card = self._create_card(
            "Microphone Guard",
            "Protection state of the Windows default microphone volume.",
        )
        self.microphone_guard_value = self.microphone_guard_card.findChild(QLabel, "CardValue")

        self.guard_panel = QFrame()
        self.guard_panel.setObjectName("Panel")
        guard_layout = QVBoxLayout(self.guard_panel)
        guard_layout.setContentsMargins(18, 18, 18, 18)
        guard_layout.setSpacing(10)

        guard_title = QLabel("Microphone Protection")
        guard_title.setObjectName("SectionTitle")

        self.guard_text = QLabel()
        self.guard_text.setObjectName("MutedText")
        self.guard_text.setWordWrap(True)

        self.guard_correction = QLabel()
        self.guard_correction.setObjectName("CardValue")
        self.guard_correction.setProperty("role", "accent")

        guard_layout.addWidget(guard_title)
        guard_layout.addWidget(self.guard_text)
        guard_layout.addWidget(self.guard_correction)

        cards.addWidget(self.keyboard_status_card, 0, 0)
        cards.addWidget(self.mouse_status_card, 0, 1)
        cards.addWidget(self.microphone_guard_card, 1, 0, 1, 2)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(cards)
        layout.addWidget(self.guard_panel)
        layout.addStretch()

        self.context.state_changed.connect(self.refresh)
        self.refresh()

    def _create_card(self, title_text: str, body_text: str) -> QFrame:
        card = QFrame()
        card.setObjectName("Panel")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("SectionTitle")

        value = QLabel("")
        value.setObjectName("CardValue")
        value.setProperty("role", "neutral")

        body = QLabel(body_text)
        body.setObjectName("MutedText")
        body.setWordWrap(True)

        card_layout.addWidget(title)
        card_layout.addWidget(value)
        card_layout.addWidget(body)

        return card

    def refresh(self) -> None:
        if self.context.state.keyboard_locked:
            self.keyboard_status_value.setText("Locked")
            self.keyboard_status_value.setProperty("role", "danger")
            self.mouse_status_value.setText("Available")
            self.mouse_status_value.setProperty("role", "success")
        else:
            self.keyboard_status_value.setText("Unlocked")
            self.keyboard_status_value.setProperty("role", "success")
            self.mouse_status_value.setText("Available")
            self.mouse_status_value.setProperty("role", "success")

        device = self.context.microphone_guard_service.get_device("default-capture")

        if device is not None:
            state_text = "Active" if device.guard_enabled else "Inactive"
            self.microphone_guard_value.setText(
                f"{state_text} · {device.current_level}%"
            )
            self.microphone_guard_value.setProperty(
                "role",
                "success" if device.guard_enabled else "neutral",
            )

            self.guard_text.setText(
                f"Default microphone: {device.display_name} · Current volume: {device.current_level}% · Target: {device.target_level}%"
            )
        else:
            self.microphone_guard_value.setText("Unavailable")
            self.microphone_guard_value.setProperty("role", "danger")
            self.guard_text.setText(
                "The Windows default microphone could not be accessed."
            )

        self.guard_correction.setText(
            f"Last correction: {self.context.microphone_guard_service.get_last_correction_text()}"
        )

        self.style().unpolish(self.keyboard_status_value)
        self.style().polish(self.keyboard_status_value)
        self.style().unpolish(self.mouse_status_value)
        self.style().polish(self.mouse_status_value)
        self.style().unpolish(self.microphone_guard_value)
        self.style().polish(self.microphone_guard_value)