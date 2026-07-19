from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.input_lock.controller import InputLockController


class InputLockPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.controller = InputLockController(context)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(16)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")
        self.subtitle_label.setWordWrap(True)

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

        self.overview_title = QLabel()
        self.overview_title.setObjectName("SectionTitle")

        self.overview_status = QLabel()
        self.overview_status.setObjectName("CardValue")

        self.overview_hint = QLabel()
        self.overview_hint.setObjectName("MutedText")
        self.overview_hint.setWordWrap(True)

        overview_layout.addWidget(self.overview_title)
        overview_layout.addWidget(self.overview_status)
        overview_layout.addWidget(self.overview_hint)

        self.keyboard_panel = self._create_panel()
        keyboard_layout = QVBoxLayout(self.keyboard_panel)
        keyboard_layout.setContentsMargins(18, 18, 18, 18)
        keyboard_layout.setSpacing(10)

        self.keyboard_title = QLabel()
        self.keyboard_title.setObjectName("SectionTitle")

        self.keyboard_status = QLabel()
        self.keyboard_status.setObjectName("CardValue")

        self.keyboard_hint = QLabel()
        self.keyboard_hint.setObjectName("MutedText")
        self.keyboard_hint.setWordWrap(True)

        self.keyboard_button = QPushButton()
        self.keyboard_button.setObjectName("PrimaryButton")
        self.keyboard_button.setFocusPolicy(Qt.StrongFocus)
        self.keyboard_button.clicked.connect(self.on_toggle_keyboard)

        keyboard_layout.addWidget(self.keyboard_title)
        keyboard_layout.addWidget(self.keyboard_status)
        keyboard_layout.addWidget(self.keyboard_hint)
        keyboard_layout.addWidget(self.keyboard_button)

        self.mouse_panel = self._create_panel()
        mouse_layout = QVBoxLayout(self.mouse_panel)
        mouse_layout.setContentsMargins(18, 18, 18, 18)
        mouse_layout.setSpacing(10)

        self.mouse_title = QLabel()
        self.mouse_title.setObjectName("SectionTitle")

        self.mouse_status = QLabel()
        self.mouse_status.setObjectName("CardValue")

        self.mouse_hint = QLabel()
        self.mouse_hint.setObjectName("MutedText")
        self.mouse_hint.setWordWrap(True)

        self.mouse_button = QPushButton()
        self.mouse_button.setObjectName("PrimaryButton")
        self.mouse_button.setFocusPolicy(Qt.StrongFocus)
        self.mouse_button.clicked.connect(self.on_toggle_mouse)

        mouse_layout.addWidget(self.mouse_title)
        mouse_layout.addWidget(self.mouse_status)
        mouse_layout.addWidget(self.mouse_hint)
        mouse_layout.addWidget(self.mouse_button)

        panels = QGridLayout()
        panels.setHorizontalSpacing(16)
        panels.setVerticalSpacing(16)
        panels.addWidget(self.keyboard_panel, 0, 0)
        panels.addWidget(self.mouse_panel, 0, 1)

        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addWidget(self.overview_panel)
        root.addLayout(panels)
        root.addStretch()

        self.mouse_enforce_timer = QTimer(self)
        self.mouse_enforce_timer.timeout.connect(self.on_mouse_enforce_tick)
        self.mouse_enforce_timer.start(50)

        self.context.input_lock_service.state.changed.connect(self.refresh)
        self.context.state_changed.connect(self.refresh)
        self.refresh()

    def _create_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        return panel

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._position_toast()

    def _position_toast(self) -> None:
        if not self.toast_label.isHidden():
            self.toast_label.adjustSize()
        margin = 20
        x = max(margin, self.width() - self.toast_label.width() - margin)
        y = margin
        self.toast_label.move(x, y)

    def show_toast(self, message: str) -> None:
        self.toast_label.setText(message)
        self.toast_label.adjustSize()
        self._position_toast()
        self.toast_label.show()
        self.toast_label.raise_()
        self.toast_timer.start(2200)

    def on_mouse_enforce_tick(self) -> None:
        self.controller.enforce()

        mouse_service = self.context.input_lock_service.mouse_lock_service
        if mouse_service.consume_emergency_unlock_request():
            self.controller.unlock_all()
            self.show_toast(t("input_lock.toast_emergency_unlock"))

    def on_toggle_keyboard(self) -> None:
        service = self.context.input_lock_service
        was_locked = service.keyboard_locked()
        mouse_was_locked = service.mouse_locked()

        self.controller.toggle_keyboard_lock()

        if was_locked:
            self.show_toast(t("input_lock.toast_keyboard_disabled"))
        else:
            if mouse_was_locked:
                self.show_toast(t("input_lock.toast_mouse_unlocked_keyboard_enabled"))
            else:
                self.show_toast(t("input_lock.toast_keyboard_enabled"))

    def on_toggle_mouse(self) -> None:
        service = self.context.input_lock_service
        was_locked = service.mouse_locked()
        keyboard_was_locked = service.keyboard_locked()

        self.controller.toggle_mouse_lock()

        if was_locked:
            self.show_toast(t("input_lock.toast_mouse_disabled"))
        else:
            if keyboard_was_locked:
                self.show_toast(t("input_lock.toast_keyboard_unlocked_mouse_enabled"))
            else:
                self.show_toast(t("input_lock.toast_mouse_enabled"))

    def refresh(self) -> None:
        self.title_label.setText(t("input_lock.page_title"))
        self.subtitle_label.setText(t("input_lock.page_subtitle"))

        self.overview_title.setText(t("input_lock.status_title"))
        self.keyboard_title.setText(t("input_lock.keyboard_title"))
        self.keyboard_hint.setText(t("input_lock.keyboard_hint"))
        self.mouse_title.setText(t("input_lock.mouse_title"))

        settings = self.context.settings_service
        shortcut_text = settings.get_mouse_lock_hotkey() if settings else "Shift+Alt+M"

        self.mouse_hint.setText(t("input_lock.mouse_hint", shortcut=shortcut_text))

        state = self.context.input_lock_service.state
        keyboard_locked = state.keyboard_locked()
        mouse_locked = state.mouse_locked()

        self.keyboard_status.setText(
            t("input_lock.status_keyboard_locked")
            if keyboard_locked
            else t("input_lock.status_unlocked")
        )
        self.keyboard_status.setProperty("role", "danger" if keyboard_locked else "success")

        self.mouse_status.setText(
            t("input_lock.status_mouse_locked")
            if mouse_locked
            else t("input_lock.status_unlocked")
        )
        self.mouse_status.setProperty("role", "danger" if mouse_locked else "success")

        self.keyboard_button.setText(
            t("input_lock.keyboard_button_unlock")
            if keyboard_locked
            else t("input_lock.keyboard_button_lock")
        )
        self.mouse_button.setText(
            t("input_lock.mouse_button_unlock")
            if mouse_locked
            else t("input_lock.mouse_button_lock")
        )

        if keyboard_locked:
            self.overview_status.setText(t("input_lock.status_keyboard_locked"))
            self.overview_status.setProperty("role", "danger")
            self.overview_hint.setText(t("input_lock.status_hint_keyboard"))
        elif mouse_locked:
            self.overview_status.setText(t("input_lock.status_mouse_locked"))
            self.overview_status.setProperty("role", "danger")
            self.overview_hint.setText(t("input_lock.status_hint_mouse", shortcut=shortcut_text))
        else:
            self.overview_status.setText(t("input_lock.status_unlocked"))
            self.overview_status.setProperty("role", "success")
            self.overview_hint.setText(t("input_lock.status_hint_unlocked"))

        self._repolish_status_widgets()

    def _repolish_status_widgets(self) -> None:
        keyboard_locked = self.context.input_lock_service.state.keyboard_locked()
        mouse_locked = self.context.input_lock_service.state.mouse_locked()

        # Update button styles to reflect locked/unlocked state
        if keyboard_locked:
            self.keyboard_button.setObjectName("DangerButton")
        else:
            self.keyboard_button.setObjectName("PrimaryButton")

        if mouse_locked:
            self.mouse_button.setObjectName("DangerButton")
        else:
            self.mouse_button.setObjectName("PrimaryButton")

        widgets = [
            self.overview_status,
            self.keyboard_status,
            self.mouse_status,
            self.keyboard_button,
            self.mouse_button,
        ]

        for widget in widgets:
            self.style().unpolish(widget)
            self.style().polish(widget)
            widget.update()

        self.setStyleSheet(self.styleSheet())