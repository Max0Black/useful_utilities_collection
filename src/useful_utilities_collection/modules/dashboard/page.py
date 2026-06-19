from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(16)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel("A compact overview of the current utility state.")
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)

        cards = QGridLayout()
        cards.setHorizontalSpacing(16)
        cards.setVerticalSpacing(16)

        self.keyboard_card, self.keyboard_value, self.keyboard_body = self._create_card(
            "Keyboard Lock",
            "Shows whether keyboard input is currently locked.",
        )

        self.mouse_card, self.mouse_value, self.mouse_body = self._create_card(
            "Mouse Lock",
            "Shows whether mouse input is currently locked.",
        )

        self.microphone_card, self.microphone_value, self.microphone_body = self._create_card(
            "Microphone Guard",
            "Protection state of the Windows default microphone volume.",
        )

        self.guard_panel = QFrame()
        self.guard_panel.setObjectName("Panel")

        guard_layout = QVBoxLayout(self.guard_panel)
        guard_layout.setContentsMargins(18, 18, 18, 18)
        guard_layout.setSpacing(10)

        guard_title = QLabel("Microphone Protection")
        guard_title.setObjectName("SectionTitle")

        self.guard_text = QLabel("")
        self.guard_text.setObjectName("MutedText")
        self.guard_text.setWordWrap(True)

        self.guard_correction = QLabel("")
        self.guard_correction.setObjectName("CardValue")
        self.guard_correction.setProperty("role", "accent")

        guard_layout.addWidget(guard_title)
        guard_layout.addWidget(self.guard_text)
        guard_layout.addWidget(self.guard_correction)

        cards.addWidget(self.keyboard_card, 0, 0)
        cards.addWidget(self.mouse_card, 0, 1)
        cards.addWidget(self.microphone_card, 1, 0, 1, 2)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addLayout(cards)
        root.addWidget(self.guard_panel)
        root.addStretch()

        self.context.input_lock_service.state.changed.connect(self.refresh)
        self.context.state_changed.connect(self.refresh)
        self.refresh()

    def _create_card(self, title_text: str, body_text: str):
        card = QFrame()
        card.setObjectName("Panel")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("SectionTitle")

        value = QLabel("")
        value.setObjectName("CardValue")
        value.setProperty("role", "neutral")

        body = QLabel(body_text)
        body.setObjectName("MutedText")
        body.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(value)
        layout.addWidget(body)

        return card, value, body

    def refresh(self) -> None:
        input_lock_state = self.context.input_lock_service.state
        keyboard_locked = input_lock_state.keyboard_locked()
        mouse_locked = input_lock_state.mouse_locked()

        if keyboard_locked:
            self.keyboard_value.setText("Locked")
            self.keyboard_value.setProperty("role", "danger")
            self.keyboard_body.setText("Keyboard input is currently blocked.")
        else:
            self.keyboard_value.setText("Unlocked")
            self.keyboard_value.setProperty("role", "success")
            self.keyboard_body.setText("Keyboard input is currently available.")

        if mouse_locked:
            self.mouse_value.setText("Locked")
            self.mouse_value.setProperty("role", "danger")
            self.mouse_body.setText(
                "Mouse input is currently blocked. Emergency unlock remains available."
            )
        else:
            self.mouse_value.setText("Unlocked")
            self.mouse_value.setProperty("role", "success")
            self.mouse_body.setText("Mouse input is currently available.")

        device = self.context.microphone_guard_service.get_device("default-capture")

        if device is not None:
            guard_active = bool(device.guard_enabled)
            state_text = "Active" if guard_active else "Inactive"

            self.microphone_value.setText(f"{state_text} · {device.current_level}%")
            self.microphone_value.setProperty(
                "role",
                "success" if guard_active else "neutral",
            )
            self.microphone_body.setText(
                "Protection state of the Windows default microphone volume."
            )
            self.guard_text.setText(
                f"Default microphone: {device.display_name} · Current volume: {device.current_level}% · Target: {device.target_level}%"
            )
        else:
            self.microphone_value.setText("Unavailable")
            self.microphone_value.setProperty("role", "danger")
            self.microphone_body.setText(
                "The default capture device could not be read."
            )
            self.guard_text.setText(
                "The Windows default microphone could not be accessed."
            )

        self.guard_correction.setText(
            f"Last correction: {self.context.microphone_guard_service.get_last_correction_text()}"
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