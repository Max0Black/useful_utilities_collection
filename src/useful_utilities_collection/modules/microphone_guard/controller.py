from useful_utilities_collection.core.app_context import AppContext


class MicrophoneGuardController:
    def __init__(self, context: AppContext):
        self.context = context

    def refresh_devices(self) -> None:
        self.context.microphone_guard_service.refresh_devices()
        self.context.microphone_guard_service.refresh_and_enforce_selected()
        self.context.notify_state_changed()

    def refresh_selected(self) -> None:
        self.context.microphone_guard_service.refresh_selected_device_state()
        self.context.microphone_guard_service.refresh_and_enforce_selected()
        self.context.notify_state_changed()

    def select_device(self, device_id: str) -> None:
        self.context.state.selected_microphone_id = device_id
        self.context.microphone_guard_service.set_selected_device_id(device_id)
        self.context.notify_state_changed()

    def set_target_level(self, device_id: str, level: int) -> None:
        self.context.microphone_guard_service.set_target_level(device_id, level)
        self.context.notify_state_changed()

    def set_current_level(self, device_id: str, level: int) -> None:
        self.context.microphone_guard_service.set_current_level(device_id, level)
        self.context.microphone_guard_service.refresh_selected_device_state()
        self.context.notify_state_changed()

    def set_auto_restore(self, device_id: str, enabled: bool) -> None:
        self.context.microphone_guard_service.set_auto_restore(device_id, enabled)
        self.context.notify_state_changed()

    def enable_guard(self, device_id: str) -> None:
        self.context.microphone_guard_service.set_guard_enabled(device_id, True)
        self.context.state.microphone_guard_active = True
        self.context.notify_state_changed()

    def disable_guard(self, device_id: str) -> None:
        self.context.microphone_guard_service.set_guard_enabled(device_id, False)
        self.context.state.microphone_guard_active = False
        self.context.notify_state_changed()

    def sync_target_to_current(self, device_id: str) -> None:
        device = self.context.microphone_guard_service.get_device(device_id)
        if device is None:
            return
        self.context.microphone_guard_service.set_target_level(device_id, device.current_level)
        self.context.notify_state_changed()