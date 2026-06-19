class InputLockController:
    def __init__(self, context):
        self.context = context

    def toggle_keyboard_lock(self) -> None:
        service = self.context.input_lock_service

        if service.keyboard_locked():
            service.unlock_keyboard()
        else:
            service.lock_keyboard()

    def toggle_mouse_lock(self) -> None:
        service = self.context.input_lock_service

        if service.mouse_locked():
            service.unlock_mouse()
        else:
            service.lock_mouse()

    def unlock_all(self) -> None:
        self.context.input_lock_service.unlock()

    def enforce(self) -> None:
        service = self.context.input_lock_service
        mouse_service = getattr(service, "mouse_lock_service", None)
        if mouse_service is None:
            return

        enforce = getattr(mouse_service, "enforce", None)
        if callable(enforce):
            enforce()