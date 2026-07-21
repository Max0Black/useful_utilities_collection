import keyboard


class KeyboardLockService:
    def __init__(self):
        self._locked = False
        self._hook = None
        self._allowed_keys: set[int] = set()

    def lock(self, allowed_keys: set[int] | None = None) -> bool:
        if self._locked:
            return True

        self._allowed_keys = allowed_keys or set()
        self._hook = keyboard.hook(self._on_key_event, suppress=True)
        self._locked = True
        return True

    def unlock(self) -> bool:
        if not self._locked:
            return True

        if self._hook is not None:
            keyboard.unhook(self._hook)
            self._hook = None

        self._locked = False
        return True

    def is_locked(self) -> bool:
        return self._locked

    def shutdown(self) -> None:
        self.unlock()

    def _on_key_event(self, event) -> bool:
        if not self._locked:
            return False

        if event.scan_code in self._allowed_keys:
            return True

        return False