import ctypes
from ctypes import wintypes

import keyboard
from pynput import mouse


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]


class MouseLockService:
    EMERGENCY_HOTKEY = "shift+alt+m"

    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    WM_RBUTTONDOWN = 0x0204
    WM_RBUTTONUP = 0x0205
    WM_MBUTTONDOWN = 0x0207
    WM_MBUTTONUP = 0x0208
    WM_MOUSEWHEEL = 0x020A
    WM_MOUSEHWHEEL = 0x020E
    WM_MOUSEMOVE = 0x0200

    def __init__(self):
        self._locked = False
        self._listener = None
        self._hotkey_handle = None
        self._user32 = ctypes.windll.user32
        self._anchor = None
        self._emergency_unlock_requested = False

    def lock(self) -> bool:
        if self._locked:
            return True

        point = POINT()
        if not self._user32.GetCursorPos(ctypes.byref(point)):
            point.x = 0
            point.y = 0

        self._anchor = (point.x, point.y)
        self._emergency_unlock_requested = False

        if not self._clip_cursor_to_anchor():
            self._anchor = None
            return False

        try:
            self._listener = mouse.Listener(
                suppress=True,
                on_click=self._on_click,
                on_scroll=self._on_scroll,
                win32_event_filter=self._win32_event_filter,
            )
            self._listener.start()
            self._register_hotkey()
            self._locked = True
            return True
        except Exception:
            self.unlock()
            return False

    def unlock(self) -> bool:
        self._cleanup_hotkey()
        self._cleanup_listener()
        self._release_cursor()
        self._anchor = None
        self._locked = False
        self._emergency_unlock_requested = False
        return True

    def is_locked(self) -> bool:
        return self._locked

    def enforce(self) -> None:
        return

    def request_emergency_unlock(self) -> None:
        self._emergency_unlock_requested = True

    def consume_emergency_unlock_request(self) -> bool:
        if not self._emergency_unlock_requested:
            return False

        self._emergency_unlock_requested = False
        return True

    def _clip_cursor_to_anchor(self) -> bool:
        if self._anchor is None:
            return False

        x, y = self._anchor
        rect = RECT(x, y, x + 1, y + 1)
        return bool(self._user32.ClipCursor(ctypes.byref(rect)))

    def _release_cursor(self) -> None:
        try:
            self._user32.ClipCursor(None)
        except Exception:
            pass

    def _register_hotkey(self) -> None:
        try:
            self._hotkey_handle = keyboard.add_hotkey(
                self.EMERGENCY_HOTKEY,
                self.request_emergency_unlock,
                suppress=False,
                trigger_on_release=False,
            )
        except Exception:
            self._hotkey_handle = None

    def _cleanup_hotkey(self) -> None:
        if self._hotkey_handle is not None:
            try:
                keyboard.remove_hotkey(self._hotkey_handle)
            except Exception:
                pass
        self._hotkey_handle = None

    def _cleanup_listener(self) -> None:
        if self._listener is not None:
            try:
                self._listener.stop()
            except Exception:
                pass
        self._listener = None

    def _win32_event_filter(self, msg, data) -> None:
        if not self._locked or self._listener is None:
            return

        blocked_messages = {
            self.WM_MOUSEMOVE,
            self.WM_LBUTTONDOWN,
            self.WM_LBUTTONUP,
            self.WM_RBUTTONDOWN,
            self.WM_RBUTTONUP,
            self.WM_MBUTTONDOWN,
            self.WM_MBUTTONUP,
            self.WM_MOUSEWHEEL,
            self.WM_MOUSEHWHEEL,
        }

        if msg in blocked_messages:
            self._listener.suppress_event()

    def _on_click(self, x, y, button, pressed):
        if not self._locked:
            return True
        return False

    def _on_scroll(self, x, y, dx, dy):
        if not self._locked:
            return True
        return False