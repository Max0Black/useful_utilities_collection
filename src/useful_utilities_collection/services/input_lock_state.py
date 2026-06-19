from PySide6.QtCore import QObject, Signal


class InputLockState(QObject):
    changed = Signal()

    def __init__(self):
        super().__init__()
        self._keyboard_locked = False
        self._mouse_locked = False

    def keyboard_locked(self) -> bool:
        return self._keyboard_locked

    def mouse_locked(self) -> bool:
        return self._mouse_locked

    def set_keyboard_locked(self, value: bool) -> None:
        if self._keyboard_locked == value:
            return
        self._keyboard_locked = value
        self.changed.emit()

    def set_mouse_locked(self, value: bool) -> None:
        if self._mouse_locked == value:
            return
        self._mouse_locked = value
        self.changed.emit()

    def set_state(self, keyboard_locked: bool, mouse_locked: bool) -> None:
        changed = False

        if self._keyboard_locked != keyboard_locked:
            self._keyboard_locked = keyboard_locked
            changed = True

        if self._mouse_locked != mouse_locked:
            self._mouse_locked = mouse_locked
            changed = True

        if changed:
            self.changed.emit()