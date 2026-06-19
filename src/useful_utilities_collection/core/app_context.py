from PySide6.QtCore import QObject, Signal

from useful_utilities_collection.core.app_state import AppState
from useful_utilities_collection.services.keyboard_lock_service import KeyboardLockService
from useful_utilities_collection.services.microphone_guard_service import MicrophoneGuardService
from useful_utilities_collection.services.input_lock_service import InputLockService


class AppContext(QObject):
    state_changed = Signal()

    def __init__(self):
        super().__init__()
        self.state = AppState()
        self.input_lock_service = InputLockService()
        self.microphone_guard_service = MicrophoneGuardService()

    def notify_state_changed(self) -> None:
        self.state_changed.emit()