from useful_utilities_collection.core.app_context import AppContext


class KeyboardLockController:
    def __init__(self, context: AppContext):
        self.context = context

    def lock(self) -> None:
        if self.context.keyboard_lock_service.lock():
            self.context.state.keyboard_locked = True
            self.context.state.keyboard_mode = "Locked"

    def unlock(self) -> None:
        if self.context.keyboard_lock_service.unlock():
            self.context.state.keyboard_locked = False
            self.context.state.keyboard_mode = "Unlocked"

    def toggle(self) -> None:
        if self.context.state.keyboard_locked:
            self.unlock()
        else:
            self.lock()