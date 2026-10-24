from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSlider,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.microphone_guard.controller import (
    MicrophoneGuardController,
)
from useful_utilities_collection.ui.components import BasePage, ToastLabel
from useful_utilities_collection.ui.mic_tag import MicTag, get_mic_icon


class MicrophoneGuardPage(BasePage):
    def __init__(self, context):
        super().__init__(context)
        self.controller = MicrophoneGuardController(context)

        self._editing_target = False
        self._pending_target_value: int | None = None
        self._config_device_id: str | None = None

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        scroll = QScrollArea()
        scroll.setObjectName("MicGuardScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        inner = QWidget()
        inner.setObjectName("MicGuardInner")
        inner.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        scroll.setWidget(inner)
        outer_layout.addWidget(scroll)

        root = QVBoxLayout(inner)
        root.setContentsMargins(28, 24, 28, 28)
        root.setSpacing(18)

        self.toast = ToastLabel(scroll.viewport())
        self._scroll = scroll

        # ── Header with inline status indicator ───────────────────────
        header_row = QHBoxLayout()
        header_left = QVBoxLayout()
        header_left.setSpacing(4)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")
        self.subtitle_label.setWordWrap(True)

        header_left.addWidget(self.title_label)
        header_left.addWidget(self.subtitle_label)
        header_row.addLayout(header_left, 1)

        # Inline status indicator (simple dot + text, no boxy hero card)
        status_box = QHBoxLayout()
        status_box.setSpacing(8)
        self.status_dot = QLabel("●")
        self.status_dot.setObjectName("StatusIndicatorDot")
        self.status_text = QLabel()
        self.status_text.setObjectName("StatusIndicatorText")
        status_box.addWidget(self.status_dot)
        status_box.addWidget(self.status_text)
        header_row.addLayout(status_box)

        root.addLayout(header_row)

        # ── Microphones Selection Panel ──────────────────────────────
        self.mics_panel = QFrame()
        self.mics_panel.setObjectName("ModernPanel")
        mics_layout = QVBoxLayout(self.mics_panel)
        mics_layout.setContentsMargins(18, 16, 18, 16)
        mics_layout.setSpacing(12)

        mics_header_row = QHBoxLayout()
        self.mics_panel_title = QLabel()
        self.mics_panel_title.setObjectName("ModernSectionHeader")
        mics_header_row.addWidget(self.mics_panel_title)
        mics_header_row.addStretch()

        self.toggle_all_button = QPushButton()
        self.toggle_all_button.setObjectName("SmallPrimaryButton")
        self.toggle_all_button.setCursor(Qt.PointingHandCursor)
        self.toggle_all_button.setFocusPolicy(Qt.StrongFocus)
        self.toggle_all_button.clicked.connect(self.on_toggle_all)
        mics_header_row.addWidget(self.toggle_all_button)

        mics_layout.addLayout(mics_header_row)

        self.mics_hint_label = QLabel()
        self.mics_hint_label.setObjectName("MutedText")
        mics_layout.addWidget(self.mics_hint_label)

        self.active_mics_row = QHBoxLayout()
        self.active_mics_row.setSpacing(10)
        mics_layout.addLayout(self.active_mics_row)

        # ── Device Config Panel (Volume & Targets) ───────────────────
        self.level_panel = QFrame()
        self.level_panel.setObjectName("ModernPanel")
        level_layout = QVBoxLayout(self.level_panel)
        level_layout.setContentsMargins(18, 16, 18, 16)
        level_layout.setSpacing(14)

        self.selected_device_label = QLabel()
        self.selected_device_label.setObjectName("ModernSectionHeader")
        level_layout.addWidget(self.selected_device_label)

        # Side-by-Side metric cards (Current Volume vs Target Volume)
        metrics_row = QHBoxLayout()
        metrics_row.setSpacing(14)

        # Current Volume Card
        self.current_vol_card = QFrame()
        self.current_vol_card.setObjectName("VolumeMetricCard")
        curr_layout = QVBoxLayout(self.current_vol_card)
        curr_layout.setContentsMargins(12, 10, 12, 10)
        curr_layout.setSpacing(4)
        self.current_caption = QLabel()
        self.current_caption.setObjectName("VolumeMetricCaption")
        self.current_val_label = QLabel("0%")
        self.current_val_label.setObjectName("VolumeMetricValue")
        curr_layout.addWidget(self.current_caption)
        curr_layout.addWidget(self.current_val_label)
        metrics_row.addWidget(self.current_vol_card, 1)

        # Target Volume Card
        self.target_vol_card = QFrame()
        self.target_vol_card.setObjectName("VolumeMetricCard")
        target_card_layout = QVBoxLayout(self.target_vol_card)
        target_card_layout.setContentsMargins(12, 10, 12, 10)
        target_card_layout.setSpacing(4)
        self.target_caption = QLabel()
        self.target_caption.setObjectName("VolumeMetricCaption")
        self.target_val_label = QLabel("80%")
        self.target_val_label.setObjectName("VolumeMetricValue")
        self.target_val_label.setProperty("accent", "true")
        target_card_layout.addWidget(self.target_caption)
        target_card_layout.addWidget(self.target_val_label)
        metrics_row.addWidget(self.target_vol_card, 1)

        level_layout.addLayout(metrics_row)

        # Target Slider
        self.target_slider = QSlider(Qt.Horizontal)
        self.target_slider.setMinimum(0)
        self.target_slider.setMaximum(100)
        self.target_slider.setFocusPolicy(Qt.StrongFocus)
        self.target_slider.sliderPressed.connect(self.on_target_edit_started)
        self.target_slider.sliderMoved.connect(self.on_target_preview_changed)
        self.target_slider.sliderReleased.connect(self.on_target_committed)
        level_layout.addWidget(self.target_slider)

        # Action Buttons: Set target to current & Restore now
        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.set_target_to_current_btn = QPushButton()
        self.set_target_to_current_btn.setObjectName("SmallSecondaryButton")
        self.set_target_to_current_btn.setCursor(Qt.PointingHandCursor)
        self.set_target_to_current_btn.clicked.connect(self.on_set_target_to_current)

        self.restore_button = QPushButton()
        self.restore_button.setObjectName("SmallPrimaryButton")
        self.restore_button.setCursor(Qt.PointingHandCursor)
        self.restore_button.clicked.connect(self.on_restore_target)

        action_row.addWidget(self.set_target_to_current_btn)
        action_row.addWidget(self.restore_button)
        action_row.addStretch()
        level_layout.addLayout(action_row)

        # ── Activity Panel ───────────────────────────────────────────
        self.guard_panel = QFrame()
        self.guard_panel.setObjectName("ModernPanel")
        guard_layout = QVBoxLayout(self.guard_panel)
        guard_layout.setContentsMargins(18, 16, 18, 16)
        guard_layout.setSpacing(8)

        self.guard_title = QLabel()
        self.guard_title.setObjectName("ModernSectionHeader")

        self.guard_info = QLabel()
        self.guard_info.setObjectName("MutedText")
        self.guard_info.setWordWrap(True)

        self.last_correction_label = QLabel()
        self.last_correction_label.setObjectName("CardValue")
        self.last_correction_label.setProperty("role", "accent")

        guard_layout.addWidget(self.guard_title)
        guard_layout.addWidget(self.guard_info)
        guard_layout.addWidget(self.last_correction_label)

        # ── Assemble ─────────────────────────────────────────────────
        root.addWidget(self.mics_panel)
        root.addWidget(self.level_panel)
        root.addWidget(self.guard_panel)
        root.addStretch()

        # ── Timer ────────────────────────────────────────────────────
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer_tick)
        self.timer.start(self.context.settings_service.get_guard_interval())

        self.context.state_changed.connect(self.refresh)
        self.controller.refresh_devices()

    # ─────────────────────────────────────────────────────────────────
    # Toast
    # ─────────────────────────────────────────────────────────────────
    def show_toast(self, message: str) -> None:
        self.toast.show_message(message)

    # ─────────────────────────────────────────────────────────────────
    # Mic interactions
    # ─────────────────────────────────────────────────────────────────
    def on_mic_tag_select(self, device) -> None:
        """Single click on un-selected mic → select it."""
        self._config_device_id = device.device_id
        self.controller.select_device(device.device_id)
        self._do_refresh()

    def on_mic_tag_toggle(self, device) -> None:
        """Toggle guard only for this device."""
        svc = self.context.microphone_guard_service
        is_enabled = svc.is_device_guard_enabled(device.device_id)

        if is_enabled:
            self.controller.disable_guard(device.device_id)
            self.show_toast(t("microphone_guard.toast_guard_disabled"))
        else:
            self.controller.enable_guard(device.device_id)
            self.show_toast(t("microphone_guard.toast_guard_enabled"))

        self._do_refresh()

    def on_toggle_all(self) -> None:
        svc = self.context.microphone_guard_service
        if svc._guard_enabled:
            for d in svc.list_devices():
                self.controller.disable_guard(d.device_id)
            self.show_toast(t("microphone_guard.toast_guard_disabled"))
        else:
            svc.set_guard_mode("all")
            for d in svc.list_devices():
                self.controller.enable_guard(d.device_id)
            self.show_toast(t("microphone_guard.toast_guard_enabled"))
        self._do_refresh()

    def on_target_edit_started(self) -> None:
        self._editing_target = True
        self._pending_target_value = self.target_slider.value()

    def on_target_preview_changed(self, value: int) -> None:
        self._pending_target_value = value
        self.target_val_label.setText(f"{value}%")

    def on_target_committed(self) -> None:
        value = self._pending_target_value
        self._editing_target = False
        self._pending_target_value = None
        if value is None:
            value = self.target_slider.value()
        device_id = self._config_device_id or "default-capture"
        self.controller.set_target_level(device_id, value)
        self.show_toast(t("microphone_guard.toast_target_saved", level=value))
        self._do_refresh()

    def on_set_target_to_current(self) -> None:
        """Set target volume to match the current microphone volume."""
        device_id = self._config_device_id or "default-capture"
        device = self.context.microphone_guard_service.get_device(device_id)
        if device is None:
            self.show_toast(t("microphone_guard.toast_no_mic"))
            return
        current_level = int(device.current_level)
        self.controller.set_target_level(device_id, current_level)
        self.show_toast(t("microphone_guard.toast_target_saved", level=current_level))
        self._do_refresh()

    def on_restore_target(self) -> None:
        device_id = self._config_device_id or "default-capture"
        device = self.context.microphone_guard_service.get_device(device_id)
        if device is None:
            self.show_toast(t("microphone_guard.toast_no_mic"))
            return
        success = self.context.microphone_guard_service.set_current_level(
            device_id, device.target_level
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
            if self.context.settings_service.get_notify_on_correction():
                self.context.notification_requested.emit(
                    t("microphone_guard.notification_title"), message
                )

    # ─────────────────────────────────────────────────────────────────
    # Refresh
    # ─────────────────────────────────────────────────────────────────
    def _clear_mic_tags(self) -> None:
        while self.active_mics_row.count():
            item = self.active_mics_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def refresh(self) -> None:
        """Called by state_changed signal – updates timer interval then redraws."""
        current_interval = self.context.settings_service.get_guard_interval()
        if self.timer.interval() != current_interval:
            self.timer.setInterval(current_interval)
        self._do_refresh()

    def _do_refresh(self) -> None:
        """Core UI refresh."""
        self.title_label.setText(t("microphone_guard.page_title"))
        self.subtitle_label.setText(t("microphone_guard.page_subtitle"))

        svc = self.context.microphone_guard_service
        devices = svc._cached_devices or svc.list_devices()
        global_enabled = svc._guard_enabled
        selected_id = svc.get_selected_device_id()

        if self._config_device_id is None:
            self._config_device_id = selected_id

        # ── Inline Status Indicator ───────────────────────────────────
        if global_enabled:
            self.status_dot.setProperty("active", "true")
            self.status_text.setText(t("microphone_guard.status_title_active"))
        else:
            self.status_dot.setProperty("active", "false")
            self.status_text.setText(t("microphone_guard.status_title_inactive"))
        self.repolish(self.status_dot)

        # ── Mics panel header ─────────────────────────────────────────
        self.mics_panel_title.setText(t("microphone_guard.active_mics_title"))
        self.mics_hint_label.setText(t("microphone_guard.mics_hint"))

        if global_enabled:
            self.toggle_all_button.setText(t("microphone_guard.button_deactivate_all"))
            self.toggle_all_button.setObjectName("SmallDangerButton")
        else:
            self.toggle_all_button.setText(t("microphone_guard.button_activate_all"))
            self.toggle_all_button.setObjectName("SmallPrimaryButton")
        self.repolish(self.toggle_all_button)

        # ── Mic tags ──────────────────────────────────────────────────
        self._clear_mic_tags()
        for d in devices:
            is_active = svc.is_device_guard_enabled(d.device_id)
            is_selected = (d.device_id == self._config_device_id)
            tag = MicTag(
                d, is_active, is_selected,
                on_select=self.on_mic_tag_select,
                on_toggle=self.on_mic_tag_toggle,
                on_toggle_all=self.on_toggle_all,
            )
            self.active_mics_row.addWidget(tag)
        self.active_mics_row.addStretch()

        # ── Config panel ──────────────────────────────────────────────
        self.current_caption.setText(t("microphone_guard.current_volume_title"))
        self.target_caption.setText(t("microphone_guard.target_volume_title"))
        self.set_target_to_current_btn.setText(t("microphone_guard.button_sync_target_to_current"))
        self.restore_button.setText(t("microphone_guard.button_restore"))

        device = svc.get_device(self._config_device_id) if self._config_device_id else None
        if device is None and devices:
            device = devices[0]
            self._config_device_id = device.device_id if device else None

        if device is None:
            self.selected_device_label.setText(t("microphone_guard.status_title_unavailable"))
            self.current_val_label.setText("–")
            self.target_val_label.setText("–")
            self.set_target_to_current_btn.setEnabled(False)
            self.restore_button.setEnabled(False)
            self.target_slider.setEnabled(False)
            return

        self.set_target_to_current_btn.setEnabled(True)
        self.restore_button.setEnabled(True)
        self.target_slider.setEnabled(True)

        icon = get_mic_icon(device.display_name, device.is_default)
        suffix = f" ({t('microphone_guard.default_label')})" if device.is_default else ""
        self.selected_device_label.setText(
            t("microphone_guard.config_device_label", icon=icon, name=device.display_name + suffix)
        )

        self.current_val_label.setText(f"{device.current_level}%")

        shown_target = (
            self._pending_target_value
            if self._editing_target and self._pending_target_value is not None
            else device.target_level
        )
        self.target_val_label.setText(f"{shown_target}%")

        if not self._editing_target:
            self.target_slider.blockSignals(True)
            self.target_slider.setValue(device.target_level)
            self.target_slider.blockSignals(False)

        # ── Activity panel ────────────────────────────────────────────
        self.guard_title.setText(t("microphone_guard.activity_title"))
        self.guard_info.setText(t("microphone_guard.activity_desc"))

        time_text = svc.get_last_correction_text()
        from_lvl, to_lvl = svc.get_last_correction_levels()
        if time_text and time_text != "–" and from_lvl is not None and to_lvl is not None:
            self.last_correction_label.setText(
                t("microphone_guard.last_correction_detail", time=time_text, previous=from_lvl, target=to_lvl)
            )
        else:
            self.last_correction_label.setText(
                t("microphone_guard.last_correction", time=time_text)
            )

        self.repolish(self.last_correction_label)
