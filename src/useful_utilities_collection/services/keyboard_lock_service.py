import keyboard


class KeyboardLockService:
    def __init__(self):
        self._locked = False
        self._blocked_keys: list[int] = []

    def lock(self) -> bool:
        if self._locked:
            return True

        for key_code in range(150):
            try:
                keyboard.block_key(key_code)
                self._blocked_keys.append(key_code)
            except Exception:
                pass

        self._locked = True
        return True

    def unlock(self) -> bool:
        if not self._locked:
            return True

        for key_code in self._blocked_keys:
            try:
                keyboard.unblock_key(key_code)
            except Exception:
                pass

        self._blocked_keys.clear()
        self._locked = False
        return True

    @property
    def is_locked(self) -> bool:
        return self._locked