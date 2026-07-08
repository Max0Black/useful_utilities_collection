from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
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

        # ── Scroll area so content doesn't get clipped ──────────────
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(14)
        scroll.setWidget(content)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

        # ── Toast ────────────────────────────────────────────────────
        self.toast_label = QLabel("", self)
        self.toast_label.hide()
        self.toast_label.setObjectName("ToastMessage")
        self.toast_label.setWordWrap(True)
        self.toast_timer = QTimer(self)
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self.toast_label.hide)

        # ── Header ───────────────────────────────────────────────────
        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")

        # ── Guard Status Panel ───────────────────────────────────────
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

        # ── Guard Mode Panel (highlighted, prominent) ─────────────────
        self.guard_mode_panel = QFrame()
        self.guard_mode_panel.setObjectName("GuardModePanel")
        guard_mode_layout = QVBoxLayout(self.guard_mode_panel)
        guard_mode_layout.setContentsMargins(16, 14, 16, 14)
        guard_mode_layout.setSpacing(10)

        guard_mode_header = QHBoxLayout()
        self.guard_mode_title_label = QLabel()
        self.guard_mode_title_label.setObjectName("GuardModeTitle")
        guard_mode_header.addWidget(self.guard_mode_title_label)
        guard_mode_header.addStretch()

        guard_mode_row = QHBoxLayout()
        self.guard_mode_label = QLabel()
        self.guard_mode_label.setObjectName("MutedText")
        self.guard_mode_combo = QComboBox()
        self.guard_mode_combo.currentIndexChanged.connect(self.on_guard_mode_changed)
        guard_mode_row.addWidget(self.guard_mode_label)
        guard_mode_row.addWidget(self.guard_mode_combo)
        guard_mode_row.addStretch()

        guard_mode_layout.addLayout(guard_mode_header)
        guard_mode_layout.addLayout(guard_mode_row)

        # Active microphones list (tags)
        self.active_mics_row = QHBoxLayout()
        self.active_mics_row.setSpacing(6)
        self.active_mics_label = QLabel()
        self.active_mics_label.setObjectName("MutedText")
        guard_mode_layout.addWidget(self.active_mics_label)
        guard_mode_layout.addLayout(self.active_mics_row)

        # ── Device Configuration Panel ───────────────────────────────
        self.level_panel = QFrame()
        self.level_panel.setObjectName("Panel")
        level_layout = QVBoxLayout(self.level_panel)
        level_layout.setContentsMargins(18, 18, 18, 18)
        level_layout.setSpacing(12)

        # Device selection row
        device_row = QHBoxLayout()
        self.select_device_label = QLabel()
        self.select_device_label.setObjectName("SectionTitle")
        self.device_combo = QComboBox()
        self.device_combo.currentIndexChanged.connect(self.on_device_changed)
        device_row.addWidget(self.select_device_label)
        device_row.addStretch()
        device_row.addWidget(self.device_combo)

        # Device guard enabled checkbox (only in specific mode)
        self.device_guard_enabled_checkbox = QCheckBox()
        self.device_guard_enabled_checkbox.stateChanged.connect(self.on_device_guard_enabled_changed)

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

        level_layout.addLayout(device_row)
        level_layout.addWidget(self.device_guard_enabled_checkbox)
        level_layout.addWidget(self.current_level_label)
        level_layout.addWidget(self.target_level_label)
        level_layout.addWidget(self.target_slider)
        level_layout.addWidget(self.auto_restore_checkbox)
        level_layout.addLayout(action_row)

        # ── Activity Panel ───────────────────────────────────────────
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

        # ── Assemble layout ──────────────────────────────────────────
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.status_panel)
        layout.addWidget(self.guard_mode_panel)
        layout.addWidget(self.level_panel)
        layout.addWidget(self.guard_panel)
        layout.addStretch()

        # ── Timer ────────────────────────────────────────────────────
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

    def on_guard_mode_changed(self, index: int) -> None:
        mode = self.guard_mode_combo.itemData(index)
        if mode:
            self.controller.set_guard_mode(mode)
            mode_text = self.guard_mode_combo.itemText(index)
            self.show_toast(t("microphone_guard.toast_guard_mode_changed", mode=mode_text))
            self.refresh()

    def on_device_changed(self, index: int) -> None:
        device_id = self.device_combo.itemData(index)
        if device_id:
            self.controller.select_device(device_id)
            self.refresh()

    def on_device_guard_enabled_changed(self, state: int) -> None:
        device_id = self.device_combo.currentData()
        if device_id:
            enabled = self.device_guard_enabled_checkbox.isChecked()
            self.controller.set_device_guard_enabled(device_id, enabled)
            if enabled:
                self.show_toast(t("microphone_guard.toast_guard_enabled"))
            else:
                self.show_toast(t("microphone_guard.toast_guard_disabled"))

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

        # Save per-device target level
        device_id = self.device_combo.currentData() or "default-capture"
        self.controller.set_target_level(device_id, value)
        self.show_toast(t("microphone_guard.toast_target_saved", level=value))

    def on_auto_restore_changed(self, state: int) -> None:
        enabled = self.auto_restore_checkbox.isChecked()
        device_id = self.device_combo.currentData() or "default-capture"
        self.controller.set_auto_restore(device_id, enabled)
        if enabled:
            self.show_toast(t("microphone_guard.toast_auto_restore_enabled"))
        else:
            self.show_toast(t("microphone_guard.toast_auto_restore_disabled"))

    def on_guard_toggle(self) -> None:
        is_active = self.context.microphone_guard_service._guard_enabled
        # Use currently selected device
        device_id = self.device_combo.currentData() or "default-capture"
        if is_active:
            self.controller.disable_guard(device_id)
            self.show_toast(t("microphone_guard.toast_guard_disabled"))
        else:
            self.controller.enable_guard(device_id)
            self.show_toast(t("microphone_guard.toast_guard_enabled"))

    def on_restore_target(self) -> None:
        device_id = self.device_combo.currentData() or "default-capture"
        device = self.context.microphone_guard_service.get_device(device_id)
        if device is None:
            self.show_toast(t("microphone_guard.toast_no_mic"))
            return

        success = self.context.microphone_guard_service.set_current_level(
            device_id,
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

        if result.restored:
            # Only update UI when something actually changed
            self.context.notify_state_changed()

            if hasattr(result, "corrected_devices") and result.corrected_devices:
                if len(result.corrected_devices) > 1:
                    details = "\n".join([
                        f"• {d['name']}: {d['previous']}% → {d['target']}%"
                        for d in result.corrected_devices
                    ])
                    message = t("microphone_guard.toast_multiple_corrected", details=details)
                else:
                    d = result.corrected_devices[0]
                    message = t(
                        "microphone_guard.toast_volume_corrected",
                        previous=d["previous"],
                        target=d["target"],
                    )
            else:
                message = t(
                    "microphone_guard.toast_volume_corrected",
                    previous=result.previous_level,
                    target=result.target_level,
                )

            self.show_toast(message)
            self.context.notification_requested.emit(
                t("microphone_guard.notification_title"), message
            )

    def _clear_mic_tags(self) -> None:
        """Remove all mic tag widgets from the active_mics_row."""
        while self.active_mics_row.count():
            item = self.active_mics_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh(self) -> None:
        current_interval = self.context.settings_service.get_guard_interval()
        if self.timer.interval() != current_interval:
            self.timer.setInterval(current_interval)

        self.title_label.setText(t("microphone_guard.page_title"))
        self.subtitle_label.setText(t("microphone_guard.page_subtitle"))

        # ── Guard Mode panel ──────────────────────────────────────
        self.guard_mode_title_label.setText("⚡ " + t("microphone_guard.guard_mode_label").rstrip(":"))
        self.guard_mode_label.setText(t("microphone_guard.guard_mode_label"))

        self.guard_mode_combo.blockSignals(True)
        self.guard_mode_combo.clear()
        self.guard_mode_combo.addItem(t("microphone_guard.guard_mode_selected"), "selected")
        self.guard_mode_combo.addItem(t("microphone_guard.guard_mode_all"), "all")
        self.guard_mode_combo.addItem(t("microphone_guard.guard_mode_specific"), "specific")

        current_mode = self.context.microphone_guard_service.get_guard_mode()
        for idx in range(self.guard_mode_combo.count()):
            if self.guard_mode_combo.itemData(idx) == current_mode:
                self.guard_mode_combo.setCurrentIndex(idx)
                break
        self.guard_mode_combo.blockSignals(False)

        # Performance: use cached devices (already refreshed by the timer tick)
        devices = self.context.microphone_guard_service._cached_devices or self.context.microphone_guard_service.list_devices()
        global_enabled = self.context.microphone_guard_service._guard_enabled

        self._clear_mic_tags()

        if current_mode == "all":
            self.active_mics_label.setText(t("microphone_guard.guard_mode_all") + ":")
            for d in devices:
                tag = QLabel(("🎙 " if d.is_default else "") + d.display_name)
                tag.setObjectName("MicTag" if global_enabled else "MicTagInactive")
                tag.setToolTip(f"ID: {d.device_id}")
                self.active_mics_row.addWidget(tag)
        elif current_mode == "specific":
            guarded = [d for d in devices if d.guard_enabled]
            self.active_mics_label.setText(
                t("microphone_guard.guard_mode_specific") + f" ({len(guarded)}):"
            )
            for d in devices:
                is_active = d.guard_enabled and global_enabled
                tag = QLabel(("✔ " if d.guard_enabled else "○ ") + d.display_name)
                tag.setObjectName("MicTag" if is_active else "MicTagInactive")
                tag.setToolTip(f"ID: {d.device_id}")
                self.active_mics_row.addWidget(tag)
        else:
            # "selected" mode
            selected_id = self.context.microphone_guard_service.get_selected_device_id()
            self.active_mics_label.setText(t("microphone_guard.guard_mode_selected") + ":")
            for d in devices:
                is_selected = d.device_id == selected_id
                is_active = is_selected and global_enabled
                tag = QLabel(("🎙 " if is_selected else "○ ") + d.display_name)
                tag.setObjectName("MicTag" if is_active else "MicTagInactive")
                self.active_mics_row.addWidget(tag)

        self.active_mics_row.addStretch()

        # ── Device selection combobox ──────────────────────────────
        self.select_device_label.setText(t("microphone_guard.select_device_label"))
        selected_id = self.context.microphone_guard_service.get_selected_device_id()

        self.device_combo.blockSignals(True)
        self.device_combo.clear()
        for d in devices:
            display = f"🎙 {d.display_name} (Standard)" if d.is_default else d.display_name
            self.device_combo.addItem(display, d.device_id)

        selected_idx = 0
        for idx in range(self.device_combo.count()):
            if self.device_combo.itemData(idx) == selected_id:
                selected_idx = idx
                break
        self.device_combo.setCurrentIndex(selected_idx)
        self.device_combo.blockSignals(False)

        selected_device_id = self.device_combo.itemData(selected_idx)
        device = self.context.microphone_guard_service.get_device(selected_device_id)

        if device is None:
            self.status_value.setText(t("microphone_guard.status_title_unavailable"))
            self.status_value.setProperty("role", "danger")
            self.status_hint.setText(t("microphone_guard.status_desc_unavailable"))
            self.device_guard_enabled_checkbox.setEnabled(False)
            self.restore_button.setEnabled(False)
            self.auto_restore_checkbox.setEnabled(False)
            self.target_slider.setEnabled(False)
            self.enable_guard_button.setEnabled(False)
            self._repolish(self.status_value)
            return

        self.device_guard_enabled_checkbox.setEnabled(True)
        self.restore_button.setEnabled(True)
        self.auto_restore_checkbox.setEnabled(True)
        self.target_slider.setEnabled(True)
        self.enable_guard_button.setEnabled(True)

        # ── Status panel ───────────────────────────────────────────
        if global_enabled:
            self.status_value.setText(t("microphone_guard.status_title_active"))
            self.status_value.setProperty("role", "success")
            self.status_hint.setText(t("microphone_guard.status_desc_active"))
            self.enable_guard_button.setObjectName("DangerButton")
            self.enable_guard_button.setText(t("microphone_guard.button_disable"))
        else:
            self.status_value.setText(t("microphone_guard.status_title_inactive"))
            self.status_value.setProperty("role", "neutral")
            self.status_hint.setText(t("microphone_guard.status_desc_inactive"))
            self.enable_guard_button.setObjectName("PrimaryButton")
            self.enable_guard_button.setText(t("microphone_guard.button_enable"))

        # ── Device guard checkbox (specific mode only) ─────────────
        self.device_guard_enabled_checkbox.blockSignals(True)
        self.device_guard_enabled_checkbox.setChecked(device.guard_enabled)
        self.device_guard_enabled_checkbox.setText(t("microphone_guard.device_guard_enabled_checkbox"))
        self.device_guard_enabled_checkbox.blockSignals(False)
        self.device_guard_enabled_checkbox.setVisible(current_mode == "specific")

        # ── Volume controls ────────────────────────────────────────
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

        # ── Activity panel ─────────────────────────────────────────
        self.guard_title.setText(t("microphone_guard.activity_title"))
        self.guard_info.setText(t("microphone_guard.activity_desc"))
        self.last_correction_label.setText(
            t(
                "microphone_guard.last_correction",
                time=self.context.microphone_guard_service.get_last_correction_text(),
            )
        )

        self._repolish(self.status_value, self.last_correction_label, self.enable_guard_button)

    def _repolish(self, *widgets) -> None:
        for widget in widgets:
            self.style().unpolish(widget)
            self.style().polish(widget)
            widget.update()