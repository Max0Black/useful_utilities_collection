from PySide6.QtCore import QObject, Signal

from useful_utilities_collection.core.app_state import AppState
from useful_utilities_collection.services.microphone_guard_service import MicrophoneGuardService
from useful_utilities_collection.services.input_lock_service import InputLockService
from useful_utilities_collection.services.settings_service import SettingsService
from useful_utilities_collection.core.translation import set_language


class AppContext(QObject):
    state_changed = Signal()
    notification_requested = Signal(str, str)

    def __init__(self):
        super().__init__()
        from PySide6.QtWidgets import QApplication

        self.state = AppState()
        QApplication.processEvents()

        self.settings_service = SettingsService()
        QApplication.processEvents()
        
        # Initialize translation language
        set_language(self.settings_service.get_language())
        QApplication.processEvents()
        
        self.input_lock_service = InputLockService(self.settings_service)
        QApplication.processEvents()

        self.microphone_guard_service = MicrophoneGuardService()
        QApplication.processEvents()

        self.state.microphone_guard_active = self.microphone_guard_service._guard_enabled

    def notify_state_changed(self) -> None:
        self.state_changed.emit()