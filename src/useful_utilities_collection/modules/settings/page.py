from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QKeySequenceEdit,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.translation import get_available_languages, set_language, t


class SettingsPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.service = context.settings_service

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("MutedText")

        self.toast_label = QLabel("", self)
        self.toast_label.setObjectName("ToastMessage")
        self.toast_label.setWordWrap(True)
        self.toast_label.hide()

        self.toast_timer = QTimer(self)
        self.toast_timer.setSingleShot(True)
        self.toast_timer.timeout.connect(self.toast_label.hide)

        # Panel General
        self.general_panel = QFrame()
        self.general_panel.setObjectName("Panel")
        general_layout = QVBoxLayout(self.general_panel)
        general_layout.setContentsMargins(18, 18, 18, 18)
        general_layout.setSpacing(14)

        self.general_title = QLabel()
        self.general_title.setObjectName("SectionTitle")

        lang_row = QHBoxLayout()
        self.lang_label = QLabel()
        self.lang_combo = QComboBox()
        # Dynamically populate languages from available JSON files
        self._populate_language_combo()
        lang_row.addWidget(self.lang_label)
        lang_row.addWidget(self.lang_combo)

        self.tray_checkbox = QCheckBox()
        self.startup_checkbox = QCheckBox()

        general_layout.addWidget(self.general_title)
        general_layout.addLayout(lang_row)
        general_layout.addWidget(self.tray_checkbox)
        general_layout.addWidget(self.startup_checkbox)

        # Panel Microphone
        self.mic_panel = QFrame()
        self.mic_panel.setObjectName("Panel")
        mic_layout = QVBoxLayout(self.mic_panel)
        mic_layout.setContentsMargins(18, 18, 18, 18)
        mic_layout.setSpacing(14)

        self.mic_title = QLabel()
        self.mic_title.setObjectName("SectionTitle")

        # Interval row
        interval_row = QHBoxLayout()
        self.interval_label = QLabel()
        self.interval_combo = QComboBox()
        self.interval_combo.addItem("1.0 second (Highly responsive)", 1000)
        self.interval_combo.addItem("1.5 seconds (Default)", 1500)
        self.interval_combo.addItem("2.0 seconds (Recommended)", 2000)
        self.interval_combo.addItem("3.0 seconds (Eco mode)", 3000)
        self.interval_combo.addItem("Custom...", "custom")
        interval_row.addWidget(self.interval_label)
        interval_row.addWidget(self.interval_combo)

        # Custom interval container
        self.custom_interval_container = QWidget()
        custom_interval_layout = QHBoxLayout(self.custom_interval_container)
        custom_interval_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_interval_label = QLabel()
        self.custom_interval_spin = QDoubleSpinBox()
        self.custom_interval_spin.setRange(0.1, 300.0)
        self.custom_interval_spin.setSingleStep(0.1)
        self.custom_interval_spin.setSuffix(" s")
        custom_interval_layout.addWidget(self.custom_interval_label)
        custom_interval_layout.addWidget(self.custom_interval_spin)

        mic_layout.addWidget(self.mic_title)
        mic_layout.addLayout(interval_row)
        mic_layout.addWidget(self.custom_interval_container)

        # Panel Shortcut
        self.shortcut_panel = QFrame()
        self.shortcut_panel.setObjectName("Panel")
        shortcut_layout = QVBoxLayout(self.shortcut_panel)
        shortcut_layout.setContentsMargins(18, 18, 18, 18)
        shortcut_layout.setSpacing(14)

        self.shortcut_title = QLabel()
        self.shortcut_title.setObjectName("SectionTitle")

        shortcut_row = QHBoxLayout()
        self.shortcut_label = QLabel()
        self.shortcut_edit = QKeySequenceEdit()
        shortcut_row.addWidget(self.shortcut_label)
        shortcut_row.addWidget(self.shortcut_edit)

        self.shortcut_hint = QLabel()
        self.shortcut_hint.setObjectName("MutedText")
        self.shortcut_hint.setWordWrap(True)

        shortcut_layout.addWidget(self.shortcut_title)
        shortcut_layout.addLayout(shortcut_row)
        shortcut_layout.addWidget(self.shortcut_hint)

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.general_panel)
        layout.addWidget(self.mic_panel)
        layout.addWidget(self.shortcut_panel)
        layout.addStretch()

        self.load_settings()

        # Connect change signals
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        self.tray_checkbox.stateChanged.connect(self.on_tray_changed)
        self.startup_checkbox.stateChanged.connect(self.on_startup_changed)
        self.interval_combo.currentIndexChanged.connect(self.on_interval_changed)
        self.custom_interval_spin.valueChanged.connect(self.on_custom_interval_changed)
        self.shortcut_edit.keySequenceChanged.connect(self.on_shortcut_changed)

        self.context.state_changed.connect(self.refresh)
        self.refresh()

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

    # Human-readable display names for language codes
    _LANG_DISPLAY_NAMES = {
        "en": "English",
        "de": "Deutsch",
        "fr": "Français",
        "es": "Español",
        "it": "Italiano",
        "nl": "Nederlands",
        "pl": "Polski",
        "pt": "Português",
        "ru": "Русский",
        "tr": "Türkçe",
        "zh": "中文",
        "ja": "日本語",
        "ko": "한국어",
    }

    def _populate_language_combo(self) -> None:
        """Populate language dropdown from all available JSON language files."""
        self.lang_combo.blockSignals(True)
        self.lang_combo.clear()
        available = get_available_languages()
        # Sort: ensure 'en' and 'de' are first
        priority = ["en", "de"]
        sorted_langs = [l for l in priority if l in available] + [
            l for l in sorted(available) if l not in priority
        ]
        for code in sorted_langs:
            display = self._LANG_DISPLAY_NAMES.get(code, code.upper())
            self.lang_combo.addItem(display, code)
        self.lang_combo.blockSignals(False)

    def load_settings(self) -> None:

        # Load values into UI widgets without firing signals
        self.lang_combo.blockSignals(True)
        idx = self.lang_combo.findData(self.service.get_language())
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.blockSignals(False)

        self.tray_checkbox.blockSignals(True)
        self.tray_checkbox.setChecked(self.service.get_close_to_tray())
        self.tray_checkbox.blockSignals(False)

        self.startup_checkbox.blockSignals(True)
        self.startup_checkbox.setChecked(self.service.is_startup_enabled())
        self.startup_checkbox.blockSignals(False)

        interval = self.service.get_guard_interval()
        self.interval_combo.blockSignals(True)
        idx = self.interval_combo.findData(interval)
        if idx >= 0:
            self.interval_combo.setCurrentIndex(idx)
            self.custom_interval_container.hide()
        else:
            custom_idx = self.interval_combo.findData("custom")
            if custom_idx >= 0:
                self.interval_combo.setCurrentIndex(custom_idx)
            self.custom_interval_container.show()
            self.custom_interval_spin.blockSignals(True)
            self.custom_interval_spin.setValue(interval / 1000.0)
            self.custom_interval_spin.blockSignals(False)
        self.interval_combo.blockSignals(False)

        self.shortcut_edit.blockSignals(True)
        self.shortcut_edit.setKeySequence(QKeySequence(self.service.get_mouse_lock_hotkey()))
        self.shortcut_edit.blockSignals(False)

    def on_language_changed(self, index: int) -> None:
        lang = self.lang_combo.currentData()
        if lang:
            self.service.set_language(lang)
            set_language(lang)
            self.context.notify_state_changed()
            self.show_toast(t("settings.toast_saved"))

    def on_tray_changed(self, state: int) -> None:
        enabled = self.tray_checkbox.isChecked()
        self.service.set_close_to_tray(enabled)
        self.context.notify_state_changed()
        self.show_toast(t("settings.toast_saved"))

    def on_startup_changed(self, state: int) -> None:
        enabled = self.startup_checkbox.isChecked()
        success = self.service.set_startup_enabled(enabled)
        if success:
            msg = t("settings.toast_startup_enabled") if enabled else t("settings.toast_startup_disabled")
            self.show_toast(msg)
        else:
            self.show_toast("Failed to configure auto-startup.")
        self.load_settings() # Reload just in case it failed

    def on_interval_changed(self, index: int) -> None:
        val = self.interval_combo.currentData()
        if val == "custom":
            self.custom_interval_container.show()
            ms = int(self.custom_interval_spin.value() * 1000)
            self.service.set_guard_interval(ms)
            self.context.notify_state_changed()
            self.show_toast(t("settings.toast_saved"))
        elif val:
            self.custom_interval_container.hide()
            self.service.set_guard_interval(val)
            self.context.notify_state_changed()
            self.show_toast(t("settings.toast_saved"))

    def on_custom_interval_changed(self, val: float) -> None:
        ms = int(val * 1000)
        self.service.set_guard_interval(ms)
        self.context.notify_state_changed()
        self.show_toast(t("settings.toast_saved"))

    def on_shortcut_changed(self, key_sequence: QKeySequence) -> None:
        portable_seq = key_sequence.toString(QKeySequence.PortableText)
        if portable_seq:
            self.service.set_mouse_lock_hotkey(portable_seq)
            self.context.notify_state_changed()
            self.show_toast(t("settings.toast_saved"))

    def refresh(self) -> None:
        # Update text labels to support active language
        self.title_label.setText(t("settings.page_title"))
        self.subtitle_label.setText(t("settings.page_subtitle"))

        self.general_title.setText(t("settings.section_general"))
        self.lang_label.setText(t("settings.language_label"))
        self.tray_checkbox.setText(t("settings.tray_checkbox"))
        self.startup_checkbox.setText(t("settings.startup_checkbox"))

        self.mic_title.setText(t("settings.section_microphone"))
        self.interval_label.setText(t("settings.interval_label"))

        # Update combo items dynamically without resetting currentIndex
        self.interval_combo.setItemText(0, t("settings.interval_sec_1"))
        self.interval_combo.setItemText(1, t("settings.interval_sec_1_5"))
        self.interval_combo.setItemText(2, t("settings.interval_sec_2"))
        self.interval_combo.setItemText(3, t("settings.interval_sec_3"))
        self.interval_combo.setItemText(4, t("settings.interval_custom"))

        self.custom_interval_label.setText(t("settings.custom_interval_label"))

        self.shortcut_title.setText(t("settings.section_shortcut"))
        self.shortcut_label.setText(t("settings.shortcut_label"))
        self.shortcut_hint.setText(t("settings.shortcut_hint"))
