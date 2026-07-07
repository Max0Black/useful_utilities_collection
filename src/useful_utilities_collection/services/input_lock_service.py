from useful_utilities_collection.services.input_lock_state import InputLockState
from useful_utilities_collection.services.keyboard_lock_service import KeyboardLockService
from useful_utilities_collection.services.mouse_lock_service import MouseLockService


class InputLockService:
    def __init__(self, settings_service=None):
        self.state = InputLockState()
        self.keyboard_lock_service = KeyboardLockService()
        self.mouse_lock_service = MouseLockService(settings_service)
        self._sync_state()

    def lock_keyboard(self) -> bool:
        self.unlock_mouse()
        result = self.keyboard_lock_service.lock()
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

    def _sync_state(self) -> None:
        self.state.set_state(
            self.keyboard_lock_service.is_locked(),
            self.mouse_lock_service.is_locked(),
        )