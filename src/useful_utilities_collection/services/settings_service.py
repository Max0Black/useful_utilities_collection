import sys
from pathlib import Path
from PySide6.QtCore import QSettings

if sys.platform == "win32":
    import winreg


class SettingsService:
    def __init__(self):
        self._settings = QSettings("UsefulUtilitiesCollection", "UsefulUtilitiesCollection")
        self._language = self._settings.value("general/language", "en")
        self._close_to_tray = self._to_bool(self._settings.value("general/close_to_tray", True))
        self._guard_interval = int(self._settings.value("microphone_guard/interval", 1500))
        self._mouse_lock_hotkey = str(self._settings.value("input_lock/mouse_lock_hotkey", "Shift+Alt+M"))
        self._notify_on_correction = self._to_bool(self._settings.value("notifications/notify_on_correction", True))
        self._notify_on_minimize = self._to_bool(self._settings.value("notifications/notify_on_minimize", True))
        # Autostart handling delegated to AutostartService
        from .autostart_service import AutostartService
        self._autostart = AutostartService()

    def get_language(self) -> str:
        return self._language

    def set_language(self, lang: str) -> None:
        self._language = lang
        self._settings.setValue("general/language", lang)
        self._settings.sync()

    def get_close_to_tray(self) -> bool:
        return self._close_to_tray

    def set_close_to_tray(self, enabled: bool) -> None:
        self._close_to_tray = enabled
        self._settings.setValue("general/close_to_tray", enabled)
        self._settings.sync()

    def get_guard_interval(self) -> int:
        return self._guard_interval

    def set_guard_interval(self, interval_ms: int) -> None:
        self._guard_interval = interval_ms
        self._settings.setValue("microphone_guard/interval", interval_ms)
        self._settings.sync()

    def get_mouse_lock_hotkey(self) -> str:
        return self._mouse_lock_hotkey

    def set_mouse_lock_hotkey(self, hotkey: str) -> None:
        self._mouse_lock_hotkey = hotkey
        self._settings.setValue("input_lock/mouse_lock_hotkey", hotkey)
        self._settings.sync()

    def get_notify_on_correction(self) -> bool:
        return self._notify_on_correction

    def set_notify_on_correction(self, enabled: bool) -> None:
        self._notify_on_correction = enabled
        self._settings.setValue("notifications/notify_on_correction", enabled)
        self._settings.sync()

    def get_notify_on_minimize(self) -> bool:
        return self._notify_on_minimize

    def set_notify_on_minimize(self, enabled: bool) -> None:
        self._notify_on_minimize = enabled
        self._settings.setValue("notifications/notify_on_minimize", enabled)
        self._settings.sync()

    # New setting: start minimized flag
    def is_start_minimized(self) -> bool:
        """Return whether the app should start minimized (default False)."""
        return self._to_bool(self._settings.value("general/start_minimized", False))

    def set_start_minimized(self, enabled: bool) -> None:
        """Persist the start minimized setting."""
        self._settings.setValue("general/start_minimized", enabled)
        self._settings.sync()

    def is_startup_enabled(self) -> bool:
        # Delegate to AutostartService for Windows autostart detection
        return self._autostart.is_enabled()

    def set_startup_enabled(self, enabled: bool) -> bool:
        # Delegate to AutostartService for Windows autostart enable/disable
        if enabled:
            return self._autostart.enable()
        return self._autostart.disable()


    @staticmethod
    def _to_bool(value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return bool(value)
