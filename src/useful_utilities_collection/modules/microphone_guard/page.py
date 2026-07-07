from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.microphone_guard.controller import (
    MicrophoneGuardController,
)


class MicrophoneGuardPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.controller = MicrophoneGuardController(context)

        self._editing_target = False
        self._pending_target_value: int | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")

        self.toast_label = QLabel("", self)
        self.toast_label.hide()
        self.toast_label.setObjectName("ToastMessage")
        self.toast_label.setWordWrap(True)

        self.toast_timer = QTimer(self)
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self.toast_label.hide)

        self.status_panel = QFrame()
        self.status_panel.setObjectName("Panel")
        status_layout = QVBoxLayout(self.status_panel)
        status_layout.setContentsMargins(18, 18, 18, 18)
        status_layout.setSpacing(8)

        self.status_value = QLabel()
        self.status_value.setObjectName("CardValue")

        self.status_hint = QLabel()
        self.status_hint.setObjectName("MutedText")
        self.status_hint.setWordWrap(True)

        status_layout.addWidget(self.status_value)
        status_layout.addWidget(self.status_hint)

        self.level_panel = QFrame()
        self.level_panel.setObjectName("Panel")
        level_layout = QVBoxLayout(self.level_panel)
        level_layout.setContentsMargins(18, 18, 18, 18)
        level_layout.setSpacing(12)

        self.default_label = QLabel()
        self.default_label.setObjectName("MutedText")

        self.current_level_label = QLabel()
        self.current_level_label.setObjectName("SectionTitle")

        self.target_level_label = QLabel()
        self.target_level_label.setObjectName("MutedText")

        self.target_slider = QSlider(Qt.Horizontal)
        self.target_slider.setMinimum(0)
        self.target_slider.setMaximum(100)
        self.target_slider.sliderPressed.connect(self.on_target_edit_started)
        self.target_slider.sliderMoved.connect(self.on_target_preview_changed)
        self.target_slider.sliderReleased.connect(self.on_target_committed)

        self.auto_restore_checkbox = QCheckBox()
        self.auto_restore_checkbox.stateChanged.connect(self.on_auto_restore_changed)

        action_row = QHBoxLayout()
        action_row.setSpacing(12)

        self.enable_guard_button = QPushButton()
        self.enable_guard_button.setObjectName("PrimaryButton")
        self.enable_guard_button.clicked.connect(self.on_guard_toggle)

        self.restore_button = QPushButton()
        self.restore_button.clicked.connect(self.on_restore_target)

        action_row.addWidget(self.enable_guard_button)
        action_row.addWidget(self.restore_button)

        level_layout.addWidget(self.default_label)
        level_layout.addWidget(self.current_level_label)
        level_layout.addWidget(self.target_level_label)
        level_layout.addWidget(self.target_slider)
        level_layout.addWidget(self.auto_restore_checkbox)
        level_layout.addLayout(action_row)

        self.guard_panel = QFrame()
        self.guard_panel.setObjectName("Panel")
        guard_layout = QVBoxLayout(self.guard_panel)
        guard_layout.setContentsMargins(18, 18, 18, 18)
        guard_layout.setSpacing(8)

        self.guard_title = QLabel()
        self.guard_title.setObjectName("SectionTitle")

        self.guard_info = QLabel()
        self.guard_info.setObjectName("MutedText")
        self.guard_info.setWordWrap(True)

        self.last_correction_label = QLabel()
        self.last_correction_label.setObjectName("CardValue")
        self.last_correction_label.setProperty("role", "accent")

        guard_layout.addWidget(self.guard_title)
        guard_layout.addWidget(self.guard_info)
        guard_layout.addWidget(self.last_correction_label)

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.status_panel)
        layout.addWidget(self.level_panel)
        layout.addWidget(self.guard_panel)
        layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(self.context.settings_service.get_guard_interval())

        self.context.state_changed.connect(self.refresh)
        self.controller.refresh_devices()

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

    def on_target_edit_started(self) -> None:
        self._editing_target = True
        self._pending_target_value = self.target_slider.value()

    def on_target_preview_changed(self, value: int) -> None:
        self._pending_target_value = value
        self.target_level_label.setText(t("microphone_guard.target_volume", level=value))

    def on_target_committed(self) -> None:
        value = self._pending_target_value
        self._editing_target = False
        self._pending_target_value = None

        if value is None:
            value = self.target_slider.value()

        self.controller.set_target_level("default-capture", value)
        self.show_toast(t("microphone_guard.toast_target_saved", level=value))

    def on_auto_restore_changed(self, state: int) -> None:
        enabled = self.auto_restore_checkbox.isChecked()
        self.controller.set_auto_restore("default-capture", enabled)
        if enabled:
            self.show_toast(t("microphone_guard.toast_auto_restore_enabled"))
        else:
            self.show_toast(t("microphone_guard.toast_auto_restore_disabled"))

    def on_guard_toggle(self) -> None:
        device = self.context.microphone_guard_service.get_device("default-capture")
        if device is None:
            self.show_toast(t("microphone_guard.toast_no_mic"))
            return

        if device.guard_enabled:
            self.controller.disable_guard("default-capture")
            self.show_toast(t("microphone_guard.toast_guard_disabled"))
        else:
            self.controller.enable_guard("default-capture")
            self.show_toast(t("microphone_guard.toast_guard_enabled"))

    def on_restore_target(self) -> None:
        device = self.context.microphone_guard_service.get_device("default-capture")
        if device is None:
            self.show_toast(t("microphone_guard.toast_no_mic"))
            return

        success = self.context.microphone_guard_service.set_current_level(
            "default-capture",
            device.target_level,
        )
        self.context.microphone_guard_service.refresh_selected_device_state()
        self.context.notify_state_changed()

        if success:
            self.show_toast(t("microphone_guard.toast_restored", level=device.target_level))
        else:
            self.show_toast(t("microphone_guard.toast_restore_failed"))

    def on_timer_tick(self) -> None:
        result = self.context.microphone_guard_service.refresh_and_enforce_selected()
        self.context.notify_state_changed()

        if (
            result.restored
            and result.previous_level is not None
            and result.target_level is not None
            and result.previous_level != result.target_level
        ):
            message = t(
                "microphone_guard.toast_volume_corrected",
                previous=result.previous_level,
                target=result.target_level,
            )
            self.show_toast(message)
            self.context.notification_requested.emit(
                t("microphone_guard.notification_title"), message
            )

    def refresh(self) -> None:
        # Check and update timer interval dynamically if modified in Settings
        current_interval = self.context.settings_service.get_guard_interval()
        if self.timer.interval() != current_interval:
            self.timer.setInterval(current_interval)

        self.title_label.setText(t("microphone_guard.page_title"))
        self.subtitle_label.setText(t("microphone_guard.page_subtitle"))

        device = self.context.microphone_guard_service.get_device("default-capture")
        if device is None:
            self.status_value.setText(t("microphone_guard.status_title_unavailable"))
            self.status_value.setProperty("role", "danger")
            self.status_hint.setText(t("microphone_guard.status_desc_unavailable"))
            self.default_label.setText(t("microphone_guard.device_label_unavailable"))
            self.restore_button.setEnabled(False)
            self.auto_restore_checkbox.setEnabled(False)
            return

        self.restore_button.setEnabled(True)
        self.auto_restore_checkbox.setEnabled(True)

        if device.guard_enabled:
            self.status_value.setText(t("microphone_guard.status_title_active"))
            self.status_value.setProperty("role", "success")
            self.status_hint.setText(t("microphone_guard.status_desc_active"))
            self.enable_guard_button.setText(t("microphone_guard.button_disable"))
        else:
            self.status_value.setText(t("microphone_guard.status_title_inactive"))
            self.status_value.setProperty("role", "neutral")
            self.status_hint.setText(t("microphone_guard.status_desc_inactive"))
            self.enable_guard_button.setText(t("microphone_guard.button_enable"))

        self.default_label.setText(t("microphone_guard.device_label", name=device.display_name))
        self.current_level_label.setText(
            t("microphone_guard.current_volume", level=device.current_level)
        )

        shown_target = (
            self._pending_target_value
            if self._editing_target and self._pending_target_value is not None
            else device.target_level
        )
        self.target_level_label.setText(t("microphone_guard.target_volume", level=shown_target))

        if not self._editing_target:
            self.target_slider.blockSignals(True)
            self.target_slider.setValue(device.target_level)
            self.target_slider.blockSignals(False)

        self.auto_restore_checkbox.blockSignals(True)
        self.auto_restore_checkbox.setChecked(device.auto_restore)
        self.auto_restore_checkbox.setText(t("microphone_guard.auto_restore_checkbox"))
        self.auto_restore_checkbox.blockSignals(False)

        self.restore_button.setText(t("microphone_guard.button_restore"))

        self.guard_title.setText(t("microphone_guard.activity_title"))
        self.guard_info.setText(t("microphone_guard.activity_desc"))
        self.last_correction_label.setText(
            t(
                "microphone_guard.last_correction",
                time=self.context.microphone_guard_service.get_last_correction_text(),
            )
        )

        self.style().unpolish(self.status_value)
        self.style().polish(self.status_value)