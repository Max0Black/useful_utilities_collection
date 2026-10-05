import keyboard


class KeyboardLockService:
    def __init__(self):
        self._locked = False
        self._hook = None

    def lock(self, allowed_keys: set[int] | None = None) -> bool:
        if self._locked:
            return True

        self._hook = keyboard.hook(self._on_key_event, suppress=True)
        self._locked = True
        return True

    def unlock(self) -> bool:
        if not self._locked:
            return True

        if self._hook is not None:
            try:
                keyboard.unhook(self._hook)
            except Exception:
                pass
            self._hook = None

        self._locked = False
        return True

    def is_locked(self) -> bool:
        return self._locked

    def shutdown(self) -> None:
        self.unlock()

    def _on_key_event(self, event) -> bool:
        """
        Windows keyboard hook callback.
        Return True to allow the event to pass through to other apps.
        Return False to block (suppress) all keys unconditionally.
        """
        if not self._locked:
            return True

        # Block ALL keys unconditionally — 100% lock
        return False