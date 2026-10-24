from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel


def get_mic_icon(display_name: str, is_default: bool = False) -> str:
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

        icon_label = QLabel(get_mic_icon(device.display_name, device.is_default))
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
