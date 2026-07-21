import keyboard

from useful_utilities_collection.services.input_lock_state import InputLockState
from useful_utilities_collection.services.keyboard_lock_service import KeyboardLockService
from useful_utilities_collection.services.mouse_lock_service import MouseLockService


_KEY_MAP = {
    "ctrl": "ctrl",
    "alt": "alt",
    "shift": "shift",
    "meta": "win",
    "ins": "insert",
    "del": "delete",
    "pgup": "page up",
    "pgdn": "page down",
    "backspace": "backspace",
    "esc": "esc",
    "enter": "enter",
    "return": "enter",
    "tab": "tab",
    "space": "space",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
}


def _get_hotkey_scan_codes(portable_hotkey: str) -> set[int]:
    if not portable_hotkey:
        return set()

    first_part = portable_hotkey.split(",")[0].strip()
    parts = first_part.split("+")
    scan_codes: set[int] = set()

    for part in parts:
        p = part.strip().lower()
        mapped = _KEY_MAP.get(p, p)
        try:
            codes = keyboard.key_to_scan_codes(mapped)
            scan_codes.update(codes)
        except Exception:
            pass

    return scan_codes


class InputLockService:
    def __init__(self, settings_service=None):
        self.state = InputLockState()
        self.settings_service = settings_service
        self.keyboard_lock_service = KeyboardLockService()
        self.mouse_lock_service = MouseLockService(settings_service)
        self._sync_state()

    def lock_keyboard(self) -> bool:
        self.unlock_mouse()
        allowed_keys = set()
        if self.settings_service:
            hotkey_str = self.settings_service.get_mouse_lock_hotkey()
            if hotkey_str:
                allowed_keys = _get_hotkey_scan_codes(hotkey_str)
        if not allowed_keys:
            allowed_keys = _get_hotkey_scan_codes("shift+alt+m")
        result = self.keyboard_lock_service.lock(allowed_keys=allowed_keys)
        self._sync_state()
        return result

    def unlock_keyboard(self) -> bool:
        result = self.keyboard_lock_service.unlock()
        self._sync_state()
        return result

    def lock_mouse(self) -> bool:
        self.unlock_keyboard()
        result = self.mouse_lock_service.lock()
        self._sync_state()
        return result

    def unlock_mouse(self) -> bool:
        result = self.mouse_lock_service.unlock()
        self._sync_state()
        return result

    def unlock(self) -> bool:
        keyboard_ok = self.keyboard_lock_service.unlock()
        mouse_ok = self.mouse_lock_service.unlock()
        self._sync_state()
        return keyboard_ok and mouse_ok

    def keyboard_locked(self) -> bool:
        return self.state.keyboard_locked()

    def mouse_locked(self) -> bool:
        return self.state.mouse_locked()

    def shutdown(self) -> None:
        self.mouse_lock_service.shutdown()
        self.keyboard_lock_service.shutdown()

    def _sync_state(self) -> None:
        self.state.set_state(
            self.keyboard_lock_service.is_locked(),
            self.mouse_lock_service.is_locked(),
        )