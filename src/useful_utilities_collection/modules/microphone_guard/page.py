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
    QApplication
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.microphone_guard.controller import (
    MicrophoneGuardController,
)
from useful_utilities_collection.ui.components import BasePage, ToastLabel



def _get_mic_icon(display_name: str, is_default: bool) -> str:
    """Return an emoji icon based on the device name keywords."""
    name_lower = display_name.lower()
    if any(k in name_lower for k in ("controller", "gamepad", "xbox", "playstation", "ps4",
                                      "ps5", "dualsense", "dualshock")):
        return "🎮"
    if any(k in name_lower for k in ("stereo mix", "what u hear", "what you hear", "loopback",
                                      "wave out", "mix", "ausgabe", "wiedergabe")):
        return "🔊"
    if any(k in name_lower for k in ("cam", "camera", "webcam", "kamera")):
        return "📷"
    if any(k in name_lower for k in ("headset", "headphone", "kopfhörer", "kopfhoerer",
                                      "earphone", "ear", "in-ear")):
        return "🎧"
    if any(k in name_lower for k in ("bluetooth", "bt ", "wireless", "funk")):
        return "📡"
    if any(k in name_lower for k in ("usb", "u s b")):
        return "🔌"
    if any(k in name_lower for k in ("virtual", "voicemeeter", "vb-audio", "voip",
                                      "discord", "teamspeak", "software")):
        return "🖥"
    return "🎙"


class MicTag(QFrame):
    """Clickable mic tag.

    Interaction model:
    - Single click on un-selected tag  → selects it (opens its config below).
    - Single click on already-selected tag → toggles guard on/off for this device.
    - Keyboard: Enter/Space = single-click behaviour.
    """

    def __init__(self, device, is_active: bool, is_selected: bool,
                 on_select, on_toggle, on_toggle_all, parent=None):
        super().__init__(parent)
        self._device = device
        self._on_select = on_select
        self._on_toggle = on_toggle
        self._on_toggle_all = on_toggle_all
        self._is_selected = is_selected

        if is_active and is_selected:
            name = "MicTagActiveSelected"
        elif is_active:
            name = "MicTagActive"
        elif is_selected:
            name = "MicTagSelected"
        else:
            name = "MicTagInactive"

        self.setObjectName(name)
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setToolTip(device.display_name)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 12, 6)
        layout.setSpacing(6)

        icon_label = QLabel(_get_mic_icon(device.display_name, device.is_default))
        icon_label.setObjectName("MicTagIcon")

        name_label = QLabel(device.display_name)
        name_label.setObjectName("MicTagText")

        if is_active:
            dot = QLabel("●")
            dot.setObjectName("MicTagDot")
            layout.addWidget(dot)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)

    def _activate_tag(self) -> None:
        if self._is_selected:
            self._on_toggle(self._device)
        else:
            self._on_select(self._device)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._activate_tag()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._activate_tag()
            event.accept()
            return
        super().mouseDoubleClickEvent(event)

    def keyPressEvent(self, event) -> None:
        if event.key() in (Qt.Key_Return, Qt.Key_Space):
            self._activate_tag()
            event.accept()
            return
        super().keyPressEvent(event)


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
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(14)

        self.toast = ToastLabel(scroll.viewport())
        self._scroll = scroll

        # ── Header ───────────────────────────────────────────────────
        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")
        self.subtitle_label.setWordWrap(True)

        # ── Guard Status Panel (info only – NO button) ───────────────
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

        # ── Microphones Panel ────────────────────────────────────────
        self.mics_panel = QFrame()
        self.mics_panel.setObjectName("GuardModePanel")
        mics_layout = QVBoxLayout(self.mics_panel)
        mics_layout.setContentsMargins(16, 14, 16, 14)
        mics_layout.setSpacing(10)

        mics_header_row = QHBoxLayout()
        self.mics_panel_title = QLabel()
        self.mics_panel_title.setObjectName("GuardModeTitle")
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
        self.active_mics_row.setSpacing(8)
        mics_layout.addLayout(self.active_mics_row)

        # ── Device Config Panel (shown when a mic is selected) ────────
        self.level_panel = QFrame()
        self.level_panel.setObjectName("Panel")
        level_layout = QVBoxLayout(self.level_panel)
        level_layout.setContentsMargins(18, 18, 18, 18)
        level_layout.setSpacing(12)

        # Device name label only (no extra toggle button here)
        self.selected_device_label = QLabel()
        self.selected_device_label.setObjectName("SectionTitle")

        self.current_level_label = QLabel()
        self.current_level_label.setObjectName("MutedText")

        self.target_level_label = QLabel()
        self.target_level_label.setObjectName("MutedText")

        self.target_slider = QSlider(Qt.Horizontal)
        self.target_slider.setMinimum(0)
        self.target_slider.setMaximum(100)
        self.target_slider.setFocusPolicy(Qt.StrongFocus)
        self.target_slider.sliderPressed.connect(self.on_target_edit_started)
        self.target_slider.sliderMoved.connect(self.on_target_preview_changed)
        self.target_slider.sliderReleased.connect(self.on_target_committed)

        action_row = QHBoxLayout()
        action_row.setSpacing(12)
        self.restore_button = QPushButton()
        self.restore_button.setFocusPolicy(Qt.StrongFocus)
        self.restore_button.clicked.connect(self.on_restore_target)
        action_row.addWidget(self.restore_button)
        action_row.addStretch()

        level_layout.addWidget(self.selected_device_label)
        level_layout.addWidget(self.current_level_label)
        level_layout.addWidget(self.target_level_label)
        level_layout.addWidget(self.target_slider)
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

        # ── Assemble ─────────────────────────────────────────────────
        root.addWidget(self.title_label)
        root.addWidget(self.subtitle_label)
        root.addWidget(self.status_panel)
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
        self.target_level_label.setText(t("microphone_guard.target_volume", level=value))

    def on_target_committed(self) -> None:
        value = self._pending_target_value
        self._editing_target = False
        self._pending_target_value = None
        if value is None:
            value = self.target_slider.value()
        device_id = self._config_device_id or "default-capture"
        self.controller.set_target_level(device_id, value)
        self.show_toast(t("microphone_guard.toast_target_saved", level=value))

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
        """Core UI refresh – never touches window geometry."""
        self.title_label.setText(t("microphone_guard.page_title"))
        self.subtitle_label.setText(t("microphone_guard.page_subtitle"))

        svc = self.context.microphone_guard_service
        devices = svc._cached_devices or svc.list_devices()
        global_enabled = svc._guard_enabled
        selected_id = svc.get_selected_device_id()

        if self._config_device_id is None:
            self._config_device_id = selected_id

        # ── Status panel (info only) ──────────────────────────────
        if global_enabled:
            self.status_value.setText(t("microphone_guard.status_title_active"))
            self.status_value.setProperty("role", "success")
            self.status_hint.setText(t("microphone_guard.status_desc_active"))
        else:
            self.status_value.setText(t("microphone_guard.status_title_inactive"))
            self.status_value.setProperty("role", "neutral")
            self.status_hint.setText(t("microphone_guard.status_desc_inactive"))

        # ── Mics panel header ─────────────────────────────────────
        self.mics_panel_title.setText("🎙 " + t("microphone_guard.active_mics_title"))
        self.mics_hint_label.setText(t("microphone_guard.mics_hint"))

        if global_enabled:
            self.toggle_all_button.setText(t("microphone_guard.button_deactivate_all"))
            self.toggle_all_button.setObjectName("SmallDangerButton")
        else:
            self.toggle_all_button.setText(t("microphone_guard.button_activate_all"))
            self.toggle_all_button.setObjectName("SmallPrimaryButton")
        self.repolish(self.toggle_all_button)

        # ── Mic tags ──────────────────────────────────────────────
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

        # ── Config panel ──────────────────────────────────────────
        device = svc.get_device(self._config_device_id) if self._config_device_id else None
        if device is None and devices:
            device = devices[0]
            self._config_device_id = device.device_id if device else None

        if device is None:
            self.selected_device_label.setText(t("microphone_guard.status_title_unavailable"))
            self.restore_button.setEnabled(False)
            self.target_slider.setEnabled(False)
            self.repolish(self.status_value)
            return

        self.restore_button.setEnabled(True)
        self.target_slider.setEnabled(True)

        icon = _get_mic_icon(device.display_name, device.is_default)
        suffix = f" ({t('microphone_guard.default_label')})" if device.is_default else ""
        self.selected_device_label.setText(
            t("microphone_guard.config_device_label", icon=icon, name=device.display_name + suffix)
        )

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

        self.restore_button.setText(t("microphone_guard.button_restore"))

        # ── Activity panel ────────────────────────────────────────
        self.guard_title.setText(t("microphone_guard.activity_title"))
        self.guard_info.setText(t("microphone_guard.activity_desc"))
        self.last_correction_label.setText(
            t("microphone_guard.last_correction", time=svc.get_last_correction_text())
        )

        self.repolish(self.status_value, self.last_correction_label)