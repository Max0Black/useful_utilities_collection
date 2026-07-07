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

    def is_startup_enabled(self) -> bool:
        if sys.platform != "win32":
            return False
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ,
            )
            value, _ = winreg.QueryValueEx(key, "UsefulUtilitiesCollection")
            winreg.CloseKey(key)
            return True
        except WindowsError:
            return False

    def set_startup_enabled(self, enabled: bool) -> bool:
        if sys.platform != "win32":
            return False
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE,
            )
            if enabled:
                # Get executable path
                exe_path = sys.executable
                if "python.exe" in exe_path.lower() or "pythonw.exe" in exe_path.lower():
                    # For development mode, run main.py
                    main_py_path = Path(__file__).resolve().parents[1] / "main.py"
                    cmd = f'"{exe_path}" "{main_py_path}" --minimized'
                else:
                    cmd = f'"{exe_path}" --minimized'
                winreg.SetValueEx(key, "UsefulUtilitiesCollection", 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, "UsefulUtilitiesCollection")
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    @staticmethod
    def _to_bool(value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return bool(value)
