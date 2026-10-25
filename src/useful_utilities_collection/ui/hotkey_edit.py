from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import QLabel

from useful_utilities_collection.core.translation import t


class LiveHotkeyEdit(QLabel):
    """A clickable label that captures a key combination in real time.

    Usage:
    - Click the label to start recording.
    - Press the desired key combo (modifiers + key). The display updates live.
    - Click away (focus loss) to SAVE the recorded combo.
    - Press Escape to CANCEL and keep the old value.
    """

    def __init__(self, on_saved, parent=None):
        super().__init__(parent)
        self._on_saved = on_saved
        self._pressed_keys: set[Qt.Key] = set()
        self._modifier_map = {
            Qt.Key_Control: "Ctrl",
            Qt.Key_Alt: "Alt",
            Qt.Key_Shift: "Shift",
            Qt.Key_Meta: "Meta",
        }
        self._capturing = False
        self._current_sequence = ""  # the last SAVED value
        self._recorded_sequence = ""  # live value while capturing
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.IBeamCursor)
        self.setObjectName("HotkeyEditLabel")
        self.setMinimumWidth(200)
        self.setFixedHeight(36)
        self.setAlignment(Qt.AlignCenter)
        self._style_idle()
        self._update_placeholder()

    # ── Styling ───────────────────────────────────────────────────────
    def _style_idle(self) -> None:
        self.setStyleSheet(
            "border: 1px solid #3a4552; border-radius: 8px; "
            "background: #1a2030; color: #e6edf3; "
            "font-family: 'Segoe UI'; font-size: 10pt; padding: 4px 12px;"
        )

    def _style_recording(self) -> None:
        self.setStyleSheet(
            "border: 2px solid #1f6feb; border-radius: 8px; "
            "background: #0f2038; color: #58a6ff; "
            "font-family: 'Segoe UI'; font-size: 10pt; padding: 4px 12px;"
        )

    # ── Public API ────────────────────────────────────────────────────
    def set_sequence(self, text: str) -> None:
        """Set the displayed (saved) value from outside."""
        self._current_sequence = text
        self._update_placeholder()

    def _update_placeholder(self) -> None:
        self.setText(self._current_sequence or t("settings.shortcut_placeholder"))

    # ── Mouse ─────────────────────────────────────────────────────────
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton and not self._capturing:
            self._start_capture()
        super().mousePressEvent(event)

    # ── Capture lifecycle ─────────────────────────────────────────────
    def _start_capture(self) -> None:
        self._capturing = True
        self._pressed_keys.clear()
        self._recorded_sequence = ""
        self._style_recording()
        self.setText(t("settings.shortcut_recording"))
        self.setFocus()

    def _commit_capture(self) -> None:
        """Save the recorded combo (if any) and leave capture mode."""
        self._capturing = False
        self._pressed_keys.clear()
        self._style_idle()
        if self._recorded_sequence:
            self._current_sequence = self._recorded_sequence
            self._on_saved(self._current_sequence)
        self._update_placeholder()

    def _cancel_capture(self) -> None:
        """Discard the in-progress recording and restore old value."""
        self._capturing = False
        self._pressed_keys.clear()
        self._recorded_sequence = ""
        self._style_idle()
        self._update_placeholder()

    # ── Key events ────────────────────────────────────────────────────
    def keyPressEvent(self, event) -> None:
        if not self._capturing:
            if event.key() in (Qt.Key_Return, Qt.Key_Space):
                self._start_capture()
            return

        if event.key() == Qt.Key_Escape:
            self._cancel_capture()
            return

        self._pressed_keys.add(event.key())
        self._show_live_combo()

        # If a non-modifier key is pressed, commit the capture immediately
        if event.key() not in self._modifier_map:
            self._commit_capture()

    def keyReleaseEvent(self, event) -> None:
        if not self._capturing:
            return
        self._pressed_keys.discard(event.key())
        if self._pressed_keys:
            self._show_live_combo()
        else:
            if self._recorded_sequence:
                self.setText(self._recorded_sequence)
            else:
                self.setText(t("settings.shortcut_recording"))

    def _show_live_combo(self) -> None:
        combo = self._build_sequence_string(self._pressed_keys)
        if combo:
            self._recorded_sequence = combo
        self.setText(combo or t("settings.shortcut_recording"))

    def _build_sequence_string(self, keys: set) -> str:
        modifier_order = [Qt.Key_Control, Qt.Key_Alt, Qt.Key_Shift, Qt.Key_Meta]
        parts = []
        for mod_key in modifier_order:
            if mod_key in keys:
                parts.append(self._modifier_map[mod_key])
        for key in keys:
            if key not in self._modifier_map:
                key_str = QKeySequence(key).toString()
                if key_str:
                    parts.append(key_str)
        return "+".join(parts)

    def focusOutEvent(self, event) -> None:
        if self._capturing:
            self._commit_capture()
        super().focusOutEvent(event)
