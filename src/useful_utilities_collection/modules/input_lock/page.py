from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.modules.input_lock.controller import InputLockController


class InputLockPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.controller = InputLockController(context)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(16)

        title = QLabel("Input Lock")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Lock either the keyboard or the mouse. Only one lock can be active at a time."
        )
        subtitle.setObjectName("MutedText")
        subtitle.setWordWrap(True)

        self.toast_label = QLabel("", self)
        self.toast_label.setObjectName("ToastMessage")
        self.toast_label.setWordWrap(True)
        self.toast_label.hide()

        self.toast_timer = QTimer(self)
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self.toast_label.hide)

        self.overview_panel = self._create_panel()
        overview_layout = QVBoxLayout(self.overview_panel)
        overview_layout.setContentsMargins(18, 18, 18, 18)
        overview_layout.setSpacing(8)

        overview_title = QLabel("Status")
        overview_title.setObjectName("SectionTitle")

        self.overview_status = QLabel("Unlocked")
        self.overview_status.setObjectName("CardValue")

        self.overview_hint = QLabel("No input lock is currently active.")
        self.overview_hint.setObjectName("MutedText")
        self.overview_hint.setWordWrap(True)

        overview_layout.addWidget(overview_title)
        overview_layout.addWidget(self.overview_status)
        overview_layout.addWidget(self.overview_hint)

        self.keyboard_panel = self._create_panel()
        keyboard_layout = QVBoxLayout(self.keyboard_panel)
        keyboard_layout.setContentsMargins(18, 18, 18, 18)
        keyboard_layout.setSpacing(10)

        keyboard_title = QLabel("Keyboard")
        keyboard_title.setObjectName("SectionTitle")

        self.keyboard_status = QLabel("Unlocked")
        self.keyboard_status.setObjectName("CardValue")

        self.keyboard_hint = QLabel(
            "Use this when you want to prevent keyboard input temporarily."
        )
        self.keyboard_hint.setObjectName("MutedText")
        self.keyboard_hint.setWordWrap(True)

        self.keyboard_button = QPushButton("Lock keyboard")
        self.keyboard_button.setObjectName("PrimaryButton")
        self.keyboard_button.clicked.connect(self.on_toggle_keyboard)

        keyboard_layout.addWidget(keyboard_title)
        keyboard_layout.addWidget(self.keyboard_status)
        keyboard_layout.addWidget(self.keyboard_hint)
        keyboard_layout.addWidget(self.keyboard_button)

        self.mouse_panel = self._create_panel()
        mouse_layout = QVBoxLayout(self.mouse_panel)
        mouse_layout.setContentsMargins(18, 18, 18, 18)
        mouse_layout.setSpacing(10)

        mouse_title = QLabel("Mouse")
        mouse_title.setObjectName("SectionTitle")

        self.mouse_status = QLabel("Unlocked")
        self.mouse_status.setObjectName("CardValue")

        self.mouse_hint = QLabel(
            "Use this when you want to prevent mouse movement or clicks. "
            "Emergency unlock remains available via keyboard shortcut."
        )
        self.mouse_hint.setObjectName("MutedText")
        self.mouse_hint.setWordWrap(True)

        self.mouse_button = QPushButton("Lock mouse")
        self.mouse_button.setObjectName("PrimaryButton")
        self.mouse_button.clicked.connect(self.on_toggle_mouse)

        mouse_layout.addWidget(mouse_title)
        mouse_layout.addWidget(self.mouse_status)
        mouse_layout.addWidget(self.mouse_hint)
        mouse_layout.addWidget(self.mouse_button)

        panels = QGridLayout()
        panels.setHorizontalSpacing(16)
        panels.setVerticalSpacing(16)
        panels.addWidget(self.keyboard_panel, 0, 0)
        panels.addWidget(self.mouse_panel, 0, 1)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addWidget(self.toast_label)
        root.addWidget(self.overview_panel)
        root.addLayout(panels)
        root.addStretch()

        self.mouse_enforce_timer = QTimer(self)
        self.mouse_enforce_timer.timeout.connect(self.on_mouse_enforce_tick)
        self.mouse_enforce_timer.start(50)

        self.context.input_lock_service.state.changed.connect(self.refresh)
        self.refresh()

    def _create_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        return panel

    def show_toast(self, message: str) -> None:
        self.toast_label.setText(message)
        self.toast_label.show()
        self.toast_timer.start(2200)

    def on_mouse_enforce_tick(self) -> None:
        self.controller.enforce()

        mouse_service = self.context.input_lock_service.mouse_lock_service
        if mouse_service.consume_emergency_unlock_request():
            self.controller.unlock_all()
            self.show_toast("Emergency unlock triggered.")

    def on_toggle_keyboard(self) -> None:
        service = self.context.input_lock_service
        was_locked = service.keyboard_locked()
        mouse_was_locked = service.mouse_locked()

        self.controller.toggle_keyboard_lock()

        if was_locked:
            self.show_toast("Keyboard lock disabled.")
        else:
            if mouse_was_locked:
                self.show_toast("Mouse unlocked. Keyboard lock enabled.")
            else:
                self.show_toast("Keyboard lock enabled.")

    def on_toggle_mouse(self) -> None:
        service = self.context.input_lock_service
        was_locked = service.mouse_locked()
        keyboard_was_locked = service.keyboard_locked()

        self.controller.toggle_mouse_lock()

        if was_locked:
            self.show_toast("Mouse lock disabled.")
        else:
            if keyboard_was_locked:
                self.show_toast("Keyboard unlocked. Mouse lock enabled.")
            else:
                self.show_toast("Mouse lock enabled.")

    def refresh(self) -> None:
        state = self.context.input_lock_service.state
        keyboard_locked = state.keyboard_locked()
        mouse_locked = state.mouse_locked()

        self.keyboard_status.setText("Locked" if keyboard_locked else "Unlocked")
        self.keyboard_status.setProperty("role", "danger" if keyboard_locked else "success")

        self.mouse_status.setText("Locked" if mouse_locked else "Unlocked")
        self.mouse_status.setProperty("role", "danger" if mouse_locked else "success")

        self.keyboard_button.setText("Unlock keyboard" if keyboard_locked else "Lock keyboard")
        self.mouse_button.setText("Unlock mouse" if mouse_locked else "Lock mouse")

        if keyboard_locked:
            self.overview_status.setText("Keyboard locked")
            self.overview_status.setProperty("role", "danger")
            self.overview_hint.setText("Keyboard input is currently blocked.")
        elif mouse_locked:
            self.overview_status.setText("Mouse locked")
            self.overview_status.setProperty("role", "danger")
            self.overview_hint.setText(
                "Mouse input is currently blocked. Use Shift + Alt + M if needed."
            )
        else:
            self.overview_status.setText("Unlocked")
            self.overview_status.setProperty("role", "success")
            self.overview_hint.setText("No input lock is currently active.")

        self._repolish_status_widgets()

    def _repolish_status_widgets(self) -> None:
        widgets = [
            self.overview_status,
            self.keyboard_status,
            self.mouse_status,
        ]

        for widget in widgets:
            self.style().unpolish(widget)
            self.style().polish(widget)
            widget.update()
            
        self.setStyleSheet(self.styleSheet())