import time
from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.input_lock.controller import InputLockController
from useful_utilities_collection.ui.components import BasePage


class InputLockPage(BasePage):
    def __init__(self, context):
        super().__init__(context)
        self.controller = InputLockController(context)


        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(16)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")
        self.subtitle_label.setWordWrap(True)



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

        self.countdown_panel = self._create_panel()
        countdown_layout = QVBoxLayout(self.countdown_panel)
        countdown_layout.setContentsMargins(18, 18, 18, 18)
        countdown_layout.setSpacing(10)

        self.countdown_title = QLabel()
        self.countdown_title.setObjectName("SectionTitle")

        preset_row = QHBoxLayout()
        preset_row.setContentsMargins(0, 0, 0, 0)
        preset_row.setSpacing(8)

        self.countdown_preset_label = QLabel()
        self.countdown_preset_label.setObjectName("AboutFieldLabel")
        self.countdown_preset_label.setMinimumWidth(150)

        self.countdown_preset_combo = QComboBox()
        countdown_presets = [
            (t("input_lock.countdown_preset_30s"), 30),
            (t("input_lock.countdown_preset_1min"), 60),
            (t("input_lock.countdown_preset_5min"), 300),
            (t("input_lock.countdown_preset_10min"), 600),
            (t("input_lock.countdown_preset_30min"), 1800),
            (t("input_lock.countdown_preset_1hour"), 3600),
            (t("input_lock.countdown_preset_custom"), "custom"),
            (t("input_lock.countdown_preset_unlimited"), None),
        ]
        for text, data in countdown_presets:
            self.countdown_preset_combo.addItem(text, data)
        self.countdown_preset_combo.currentIndexChanged.connect(self._on_preset_changed)

        self.countdown_start_button = QPushButton()
        self.countdown_start_button.setObjectName("PrimaryButton")
        self.countdown_start_button.clicked.connect(self._on_start_countdown)

        preset_row.addWidget(self.countdown_preset_label)
        preset_row.addWidget(self.countdown_preset_combo)
        preset_row.addWidget(self.countdown_start_button)

        self.countdown_custom_container = QWidget()
        custom_row = QHBoxLayout(self.countdown_custom_container)
        custom_row.setContentsMargins(0, 0, 0, 0)
        custom_row.setSpacing(8)

        self.countdown_custom_label = QLabel()
        self.countdown_custom_label.setObjectName("MutedText")

        self.countdown_custom_spin = QSpinBox()
        self.countdown_custom_spin.setRange(1, 9999)
        self.countdown_custom_spin.setValue(5)

        self.countdown_unit_combo = QComboBox()
        self.countdown_unit_combo.addItems([
            t("input_lock.countdown_unit_seconds"),
            t("input_lock.countdown_unit_minutes"),
            t("input_lock.countdown_unit_hours"),
        ])
        self.countdown_unit_combo.setCurrentIndex(1)

        custom_row.addWidget(self.countdown_custom_label)
        custom_row.addWidget(self.countdown_custom_spin)
        custom_row.addWidget(self.countdown_unit_combo)

        self.countdown_running_container = QWidget()
        running_row = QHBoxLayout(self.countdown_running_container)
        running_row.setContentsMargins(0, 0, 0, 0)
        running_row.setSpacing(8)

        self.countdown_display = QLabel()
        self.countdown_display.setObjectName("CardValue")

        self.countdown_stop_button = QPushButton()
        self.countdown_stop_button.setObjectName("DangerButton")
        self.countdown_stop_button.clicked.connect(self._on_stop_countdown)

        running_row.addWidget(self.countdown_display)
        running_row.addStretch()
        running_row.addWidget(self.countdown_stop_button)

        countdown_layout.addWidget(self.countdown_title)
        countdown_layout.addLayout(preset_row)
        countdown_layout.addWidget(self.countdown_custom_container)
        countdown_layout.addWidget(self.countdown_running_container)

        self.countdown_custom_container.hide()
        self.countdown_running_container.hide()

        panels = QGridLayout()
        panels.setHorizontalSpacing(16)
        panels.setVerticalSpacing(16)
        panels.addWidget(self.keyboard_panel, 0, 0)
        panels.addWidget(self.mouse_panel, 0, 1)

        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addWidget(self.overview_panel)
        root.addWidget(self.countdown_panel)
        root.addLayout(panels)
        root.addStretch()

        self.mouse_enforce_timer = QTimer(self)
        self.mouse_enforce_timer.timeout.connect(self.on_mouse_enforce_tick)
        self.mouse_enforce_timer.start(50)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._on_countdown_tick)
        self._countdown_end = None
        self._countdown_unlimited = False

        self.context.input_lock_service.state.changed.connect(self.refresh)
        self.context.state_changed.connect(self.refresh)
        self.refresh()

    def _create_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("Panel")
        return panel



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

    def _on_preset_changed(self, index: int) -> None:
        is_custom = self.countdown_preset_combo.currentData() == "custom"
        self.countdown_custom_container.setVisible(is_custom)

    def _get_duration_seconds(self) -> int | None:
        data = self.countdown_preset_combo.currentData()
        if data == "custom":
            value = self.countdown_custom_spin.value()
            unit_index = self.countdown_unit_combo.currentIndex()
            multipliers = [1, 60, 3600]
            return value * multipliers[unit_index]
        return data

    def _format_time(self, seconds: int) -> str:
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{sec:02d}"
        return f"{minutes:d}:{sec:02d}"

    def _format_duration(self, seconds: int) -> str:
        if seconds >= 3600:
            hours = seconds / 3600
            if seconds % 3600 == 0:
                return f"{int(hours)}h"
            return f"{hours:.1f}h"
        if seconds >= 60:
            minutes = seconds / 60
            if seconds % 60 == 0:
                return f"{int(minutes)}min"
            return f"{minutes:.1f}min"
        return f"{seconds}s"

    def _show_running_state(self) -> None:
        self.countdown_preset_combo.setEnabled(False)
        self.countdown_custom_container.setEnabled(False)
        self.countdown_start_button.hide()
        self.countdown_running_container.show()

    def _show_idle_state(self) -> None:
        self.countdown_preset_combo.setEnabled(True)
        self.countdown_custom_container.setEnabled(True)
        self.countdown_start_button.show()
        self.countdown_running_container.hide()
        self.countdown_display.setText("")
        self._countdown_end = None
        self._countdown_unlimited = False

    def _on_start_countdown(self) -> None:
        duration = self._get_duration_seconds()
        if duration is None:
            self._countdown_unlimited = True
            self.controller.lock_both()
            self.countdown_display.setText(t("input_lock.countdown_running", time="∞"))
            self._show_running_state()
            self.show_toast(t("input_lock.countdown_started", duration=t("input_lock.countdown_preset_unlimited")))
            return

        self._countdown_end = time.time() + duration
        self._countdown_unlimited = False
        self.controller.lock_both()
        self._countdown_timer.start(1000)
        self._on_countdown_tick()
        self._show_running_state()
        self.show_toast(t("input_lock.countdown_started", duration=self._format_duration(duration)))

    def _on_stop_countdown(self) -> None:
        self._countdown_timer.stop()
        self._countdown_end = None
        self._countdown_unlimited = False
        self.controller.unlock_both()
        self._show_idle_state()
        self.show_toast(t("input_lock.countdown_stopped"))

    def _on_countdown_tick(self) -> None:
        if self._countdown_unlimited:
            return
        remaining = max(0, int(self._countdown_end - time.time()))
        if remaining <= 0:
            self._countdown_timer.stop()
            self._countdown_end = None
            self._show_idle_state()
            self.show_toast(t("input_lock.countdown_complete"))
            return
        self.countdown_display.setText(t("input_lock.countdown_running", time=self._format_time(remaining)))

    def refresh(self) -> None:
        self.title_label.setText(t("input_lock.page_title"))
        self.subtitle_label.setText(t("input_lock.page_subtitle"))

        self.overview_title.setText(t("input_lock.status_title"))
        self.keyboard_title.setText(t("input_lock.keyboard_title"))
        self.keyboard_hint.setText(t("input_lock.keyboard_hint"))
        self.mouse_title.setText(t("input_lock.mouse_title"))

        self.countdown_title.setText(t("input_lock.countdown_title"))
        self.countdown_preset_label.setText(t("input_lock.countdown_preset_label"))
        self.countdown_custom_label.setText(t("input_lock.countdown_custom_label"))
        self.countdown_start_button.setText(t("input_lock.countdown_start"))
        self.countdown_stop_button.setText(t("input_lock.countdown_stop"))

        # Refresh preset items in case language changed
        presets = [
            (t("input_lock.countdown_preset_30s"), 30),
            (t("input_lock.countdown_preset_1min"), 60),
            (t("input_lock.countdown_preset_5min"), 300),
            (t("input_lock.countdown_preset_10min"), 600),
            (t("input_lock.countdown_preset_30min"), 1800),
            (t("input_lock.countdown_preset_1hour"), 3600),
            (t("input_lock.countdown_preset_custom"), "custom"),
            (t("input_lock.countdown_preset_unlimited"), None),
        ]
        current_data = self.countdown_preset_combo.currentData()
        self.countdown_preset_combo.blockSignals(True)
        self.countdown_preset_combo.clear()
        for text, data in presets:
            self.countdown_preset_combo.addItem(text, data)
        idx = self.countdown_preset_combo.findData(current_data)
        if idx >= 0:
            self.countdown_preset_combo.setCurrentIndex(idx)
        self.countdown_preset_combo.blockSignals(False)
        self._on_preset_changed(self.countdown_preset_combo.currentIndex())

        units = [
            t("input_lock.countdown_unit_seconds"),
            t("input_lock.countdown_unit_minutes"),
            t("input_lock.countdown_unit_hours"),
        ]
        for i, text in enumerate(units):
            self.countdown_unit_combo.setItemText(i, text)

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

        if self.countdown_running_container.isVisible():
            widgets.extend([
                self.countdown_display,
                self.countdown_stop_button,
            ])

        self.repolish(*widgets)