from PySide6.QtCore import QObject, Signal

from useful_utilities_collection.core.app_state import AppState
from useful_utilities_collection.services.keyboard_lock_service import KeyboardLockService
from useful_utilities_collection.services.microphone_guard_service import MicrophoneGuardService
from useful_utilities_collection.services.input_lock_service import InputLockService
from useful_utilities_collection.services.settings_service import SettingsService
from useful_utilities_collection.core.translation import set_language


class AppContext(QObject):
    state_changed = Signal()
    notification_requested = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.state = AppState()
        self.settings_service = SettingsService()
        
        # Initialize translation language
        set_language(self.settings_service.get_language())
        
        self.input_lock_service = InputLockService(self.settings_service)
        self.microphone_guard_service = MicrophoneGuardService()

    def notify_state_changed(self) -> None:
        self.state_changed.emit()