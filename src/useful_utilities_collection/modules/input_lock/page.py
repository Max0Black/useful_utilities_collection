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


_COUNTDOWN_PRESETS = [
    30,
    300,
    600,
    "custom",
]


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

        self.overview_emergency_label = QLabel()
        self.overview_emergency_label.setObjectName("MutedText")
        self.overview_emergency_label.setWordWrap(True)

        overview_layout.addWidget(self.overview_title)
        overview_layout.addWidget(self.overview_status)
        overview_layout.addWidget(self.overview_hint)
        overview_layout.addWidget(self.overview_emergency_label)

        # ── Countdown / Timer panel ────────────────────────────────────
        self.countdown_panel = self._create_panel()
        countdown_layout = QVBoxLayout(self.countdown_panel)
        countdown_layout.setContentsMargins(18, 18, 18, 18)
        countdown_layout.setSpacing(12)

        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(8)

        self.countdown_title = QLabel()
        self.countdown_title.setObjectName("SectionTitle")

        self.countdown_badge = QLabel()
        self.countdown_badge.setObjectName("AboutVersionBadge")
        self.countdown_badge.hide()

        header_row.addWidget(self.countdown_title)
        header_row.addWidget(self.countdown_badge)
        header_row.addStretch()

        # ── Warning Box for Timed Lock ──────────────────────────────────
        self.countdown_warning_box = QFrame()
        self.countdown_warning_box.setObjectName("TimerWarningBox")
        warning_layout = QVBoxLayout(self.countdown_warning_box)
        warning_layout.setContentsMargins(14, 12, 14, 12)
        warning_layout.setSpacing(4)

        self.countdown_warning_title = QLabel()
        self.countdown_warning_title.setObjectName("TimerWarningTitle")
        self.countdown_warning_title.setWordWrap(True)

        self.countdown_warning_text = QLabel()
        self.countdown_warning_text.setObjectName("TimerWarningText")
        self.countdown_warning_text.setWordWrap(True)

        warning_layout.addWidget(self.countdown_warning_title)
        warning_layout.addWidget(self.countdown_warning_text)

        # ── Preset selection row ───────────────────────────────────────
        action_row = QHBoxLayout()
        action_row.setContentsMargins(0, 0, 0, 0)
        action_row.setSpacing(8)

        self.countdown_preset_combo = QComboBox()
        self.countdown_preset_combo.setMinimumWidth(220)
        for data in _COUNTDOWN_PRESETS:
            self.countdown_preset_combo.addItem(self._build_preset_label(data), data)
        self.countdown_preset_combo.currentIndexChanged.connect(self._on_preset_changed)

        self.countdown_start_button = QPushButton()
        self.countdown_start_button.setObjectName("PrimaryButton")
        self.countdown_start_button.clicked.connect(self._on_start_countdown)

        self.countdown_stop_button = QPushButton()
        self.countdown_stop_button.setObjectName("DangerButton")
        self.countdown_stop_button.clicked.connect(self._on_stop_countdown)
        self.countdown_stop_button.hide()

        action_row.addWidget(self.countdown_preset_combo)
        action_row.addWidget(self.countdown_start_button)
        action_row.addWidget(self.countdown_stop_button)

        # ── Custom duration row (settings-style) ──────────────────────
        self.countdown_custom_container = QFrame()
        self.countdown_custom_container.setObjectName("Panel")
        custom_row = QHBoxLayout(self.countdown_custom_container)
        custom_row.setContentsMargins(14, 10, 14, 10)
        custom_row.setSpacing(10)

        self.countdown_custom_label = QLabel()
        self.countdown_custom_spin = QSpinBox()
        self.countdown_custom_spin.setRange(1, 9999)
        self.countdown_custom_spin.setValue(30)
        self.countdown_custom_spin.setSuffix(" s")
        self.countdown_custom_spin.setMinimumWidth(100)

        self.countdown_unit_combo = QComboBox()
        self.countdown_unit_combo.addItems([
            t("input_lock.countdown_unit_seconds"),
            t("input_lock.countdown_unit_minutes"),
            t("input_lock.countdown_unit_hours"),
        ])
        self.countdown_unit_combo.setCurrentIndex(0)
        self.countdown_unit_combo.currentIndexChanged.connect(self._on_unit_changed)

        custom_row.addWidget(self.countdown_custom_label)
        custom_row.addStretch()
        custom_row.addWidget(self.countdown_custom_spin)
        custom_row.addWidget(self.countdown_unit_combo)

        # ── Timer display panel (premium design) ──────────────────────
        self.timer_display_panel = QFrame()
        self.timer_display_panel.setObjectName("TimerDisplayPanel")
        timer_layout = QVBoxLayout(self.timer_display_panel)
        timer_layout.setContentsMargins(24, 20, 24, 20)
        timer_layout.setSpacing(6)
        timer_layout.setAlignment(Qt.AlignCenter)

        self.timer_countdown_label = QLabel()
        self.timer_countdown_label.setObjectName("TimerCountdown")
        self.timer_countdown_label.setAlignment(Qt.AlignCenter)

        self.timer_info_label = QLabel()
        self.timer_info_label.setObjectName("TimerInfoText")
        self.timer_info_label.setAlignment(Qt.AlignCenter)

        self.timer_emergency_label = QLabel()
        self.timer_emergency_label.setObjectName("TimerInfoText")
        self.timer_emergency_label.setAlignment(Qt.AlignCenter)

        timer_layout.addWidget(self.timer_countdown_label)
        timer_layout.addWidget(self.timer_info_label)
        timer_layout.addWidget(self.timer_emergency_label)

        # ── Assemble countdown panel ──────────────────────────────────
        countdown_layout.addLayout(header_row)
        countdown_layout.addWidget(self.countdown_warning_box)
        countdown_layout.addLayout(action_row)
        countdown_layout.addWidget(self.countdown_custom_container)
        countdown_layout.addWidget(self.timer_display_panel)

        self.countdown_custom_container.hide()
        self.timer_display_panel.hide()

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
        root.addWidget(self.countdown_panel)
        root.addLayout(panels)
        root.addStretch()

        self.mouse_enforce_timer = QTimer(self)
        self.mouse_enforce_timer.timeout.connect(self.on_mouse_enforce_tick)
        self.mouse_enforce_timer.start(50)

        self._countdown_timer = QTimer(self)
        self._countdown_timer.timeout.connect(self._on_countdown_tick)
        self._countdown_end = None

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

        # Emergency hotkey ONLY unlocks standalone mouse lock (never active during timed lock or keyboard lock)
        if mouse_service.consume_emergency_unlock_request():
            if not self._countdown_timer.isActive() and not self.context.input_lock_service.keyboard_locked():
                self.context.input_lock_service.unlock_mouse()
                self.show_toast(t("input_lock.toast_emergency_unlock"))

    def on_toggle_keyboard(self) -> None:
        if self._countdown_timer.isActive():
            return
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
        if self._countdown_timer.isActive():
            return
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

    def _on_unit_changed(self, index: int) -> None:
        suffixes = [" s", " min", " h"]
        self.countdown_custom_spin.setSuffix(suffixes[index] if 0 <= index < len(suffixes) else "")

    def _get_duration_seconds(self) -> int | None:
        data = self.countdown_preset_combo.currentData()
        if data == "custom":
            value = self.countdown_custom_spin.value()
            unit_index = self.countdown_unit_combo.currentIndex()
            multipliers = [1, 60, 3600]
            return value * multipliers[unit_index]
        return data

    def _localized_duration(self, seconds: int) -> str:
        if seconds >= 3600:
            hours = seconds / 3600
            if seconds % 3600 == 0:
                value = int(hours)
                unit = t("input_lock.countdown_unit_hour") if value == 1 else t("input_lock.countdown_unit_hours")
                return f"{value} {unit}"
            unit = t("input_lock.countdown_unit_hours")
            return f"{hours:.1f} {unit}"
        if seconds >= 60:
            minutes = seconds / 60
            if seconds % 60 == 0:
                value = int(minutes)
                unit = t("input_lock.countdown_unit_minute") if value == 1 else t("input_lock.countdown_unit_minutes")
                return f"{value} {unit}"
            unit = t("input_lock.countdown_unit_minutes")
            return f"{minutes:.1f} {unit}"
        value = seconds
        unit = t("input_lock.countdown_unit_second") if value == 1 else t("input_lock.countdown_unit_seconds")
        return f"{value} {unit}"

    def _format_time(self, seconds: int) -> str:
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{sec:02d}"
        return f"{minutes:d}:{sec:02d}"

    def _show_running_state(self, duration_text: str) -> None:
        self.countdown_preset_combo.setEnabled(False)
        self.countdown_custom_container.setEnabled(False)
        self.countdown_start_button.hide()
        self.countdown_stop_button.show()
        self.countdown_badge.setText(t("input_lock.countdown_active_badge"))
        self.countdown_badge.show()

        # Show the premium timer display panel
        self.timer_display_panel.show()
        self.timer_info_label.hide()
        self.timer_emergency_label.hide()

        self.keyboard_button.setEnabled(False)
        self.mouse_button.setEnabled(False)

    def _show_idle_state(self) -> None:
        self.countdown_preset_combo.setEnabled(True)
        self.countdown_custom_container.setEnabled(True)
        self.countdown_start_button.show()
        self.countdown_stop_button.hide()
        self.timer_display_panel.hide()
        self.timer_countdown_label.setText("")
        self.timer_info_label.hide()
        self.timer_emergency_label.hide()
        self.countdown_badge.hide()
        self._countdown_end = None
        self.keyboard_button.setEnabled(True)
        self.mouse_button.setEnabled(True)

    def _on_start_countdown(self) -> None:
        duration = self._get_duration_seconds()
        if duration is None:
            return

        self._countdown_end = time.time() + duration
        self.controller.lock_both()
        self._countdown_timer.start(1000)
        self._on_countdown_tick()
        self._show_running_state(self._localized_duration(duration))
        self.show_toast(t("input_lock.countdown_started", duration=self._localized_duration(duration)))
        self.refresh()

    def _on_stop_countdown(self) -> None:
        self._countdown_timer.stop()
        self._countdown_end = None
        self.controller.unlock_both()
        self._show_idle_state()
        self.show_toast(t("input_lock.countdown_stopped"))

    def _on_countdown_tick(self) -> None:
        remaining = max(0, int(self._countdown_end - time.time()))
        if remaining <= 0:
            self._countdown_timer.stop()
            self._countdown_end = None
            self.controller.unlock_both()
            self._show_idle_state()
            self.show_toast(t("input_lock.countdown_complete"))
            return
        self.timer_countdown_label.setText(self._format_time(remaining))

    def _build_preset_label(self, data) -> str:
        if data == "custom":
            return t("input_lock.countdown_preset_custom")
        return self._localized_duration(data)

    def refresh(self) -> None:
        self.title_label.setText(t("input_lock.page_title"))
        self.subtitle_label.setText(t("input_lock.page_subtitle"))

        self.overview_title.setText(t("input_lock.status_title"))
        self.keyboard_title.setText(t("input_lock.keyboard_title"))
        self.keyboard_hint.setText(t("input_lock.keyboard_hint"))
        self.mouse_title.setText(t("input_lock.mouse_title"))

        self.countdown_title.setText(t("input_lock.countdown_title"))
        self.countdown_warning_title.setText(t("input_lock.countdown_warning_title"))
        self.countdown_warning_text.setText(t("input_lock.countdown_warning_text"))
        self.countdown_custom_label.setText(t("input_lock.countdown_custom_label"))
        self.countdown_start_button.setText(t("input_lock.countdown_start"))
        self.countdown_stop_button.setText(t("input_lock.countdown_stop"))

        current_unit_index = self.countdown_unit_combo.currentIndex()
        self.countdown_unit_combo.blockSignals(True)
        self.countdown_unit_combo.clear()
        self.countdown_unit_combo.addItems([
            t("input_lock.countdown_unit_seconds"),
            t("input_lock.countdown_unit_minutes"),
            t("input_lock.countdown_unit_hours"),
        ])
        if 0 <= current_unit_index < self.countdown_unit_combo.count():
            self.countdown_unit_combo.setCurrentIndex(current_unit_index)
        self.countdown_unit_combo.blockSignals(False)
        suffixes = [" s", " min", " h"]
        self.countdown_custom_spin.setSuffix(suffixes[current_unit_index] if 0 <= current_unit_index < len(suffixes) else "")

        current_data = self.countdown_preset_combo.currentData()
        self.countdown_preset_combo.blockSignals(True)
        self.countdown_preset_combo.clear()
        for data in _COUNTDOWN_PRESETS:
            self.countdown_preset_combo.addItem(self._build_preset_label(data), data)
        idx = self.countdown_preset_combo.findData(current_data)
        if idx >= 0:
            self.countdown_preset_combo.setCurrentIndex(idx)
        self.countdown_preset_combo.blockSignals(False)
        self._on_preset_changed(self.countdown_preset_combo.currentIndex())

        settings = self.context.settings_service
        shortcut_text = settings.get_mouse_lock_hotkey() if settings else "Shift+Alt+M"

        self.mouse_hint.setText(t("input_lock.mouse_hint"))

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

        if keyboard_locked and mouse_locked:
            self.overview_status.setText(t("input_lock.status_both_locked"))
            self.overview_status.setProperty("role", "danger")
            if self._countdown_timer.isActive():
                self.overview_hint.setText(t("input_lock.countdown_unlock_instructions"))
                self.overview_emergency_label.setText("")
            else:
                self.overview_hint.setText(t("input_lock.status_hint_both"))
                self.overview_emergency_label.setText(t("input_lock.status_emergency_disabled"))
        elif keyboard_locked and not self._countdown_timer.isActive():
            self.overview_status.setText(t("input_lock.status_keyboard_locked"))
            self.overview_status.setProperty("role", "danger")
            self.overview_hint.setText(t("input_lock.status_hint_keyboard"))
            self.overview_emergency_label.setText("")
        elif mouse_locked and not self._countdown_timer.isActive():
            self.overview_status.setText(t("input_lock.status_mouse_locked"))
            self.overview_status.setProperty("role", "danger")
            self.overview_hint.setText(t("input_lock.status_hint_mouse"))
            self.overview_emergency_label.setText(t("input_lock.emergency_hint", shortcut=shortcut_text))
        else:
            self.overview_status.setText(t("input_lock.status_unlocked"))
            self.overview_status.setProperty("role", "success")
            self.overview_hint.setText(t("input_lock.status_hint_unlocked"))
            self.overview_emergency_label.setText("")

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
            self.overview_emergency_label,
            self.countdown_warning_title,
            self.countdown_warning_text,
        ]

        if self.timer_display_panel.isVisible():
            widgets.extend([
                self.timer_countdown_label,
                self.countdown_stop_button,
                self.countdown_badge,
            ])

        self.repolish(*widgets)