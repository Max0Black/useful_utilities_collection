from useful_utilities_collection.core.app_state import AppState
from useful_utilities_collection.services.keyboard_lock_service import KeyboardLockService

class AppContext:
    def __init__(self):
        self.state = AppState()
        self.keyboard_lock_service = KeyboardLockService()