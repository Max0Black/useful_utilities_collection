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

    def is_startup_enabled(self) -> bool:
        if sys.platform != "win32":
            return False
        
        # Check registry
        reg_exists = False
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ,
            )
            value, _ = winreg.QueryValueEx(key, "UsefulUtilitiesCollection")
            winreg.CloseKey(key)
            reg_exists = True
        except WindowsError:
            pass

        # Check startup folder shortcut
        import os
        startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(startup_dir, "UsefulUtilitiesCollection.lnk")
        shortcut_exists = os.path.exists(shortcut_path)

        return reg_exists or shortcut_exists

    def set_startup_enabled(self, enabled: bool) -> bool:
        if sys.platform != "win32":
            return False
        
        reg_success = False
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
            reg_success = True
        except Exception:
            pass

        shortcut_success = self._create_startup_shortcut(enabled)
        return reg_success or shortcut_success

    def _create_startup_shortcut(self, enabled: bool) -> bool:
        import os
        import subprocess

        startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(startup_dir, "UsefulUtilitiesCollection.lnk")

        if not enabled:
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                except Exception:
                    pass
            return True

        # Get executable path
        exe_path = sys.executable
        if "python.exe" in exe_path.lower() or "pythonw.exe" in exe_path.lower():
            # For development mode, run main.py
            main_py_path = Path(__file__).resolve().parents[1] / "main.py"
            target_path = exe_path
            arguments = f'"{main_py_path}" --minimized'
            working_dir = str(main_py_path.parent)
        else:
            target_path = exe_path
            arguments = "--minimized"
            working_dir = str(Path(exe_path).parent)

        ps_cmd = (
            f'$WshShell = New-Object -ComObject WScript.Shell; '
            f'$Shortcut = $WshShell.CreateShortcut("{shortcut_path}"); '
            f'$Shortcut.TargetPath = "{target_path}"; '
            f'$Shortcut.Arguments = "{arguments}"; '
            f'$Shortcut.WorkingDirectory = "{working_dir}"; '
            f'$Shortcut.Save()'
        )

        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                check=True,
                creationflags=0x08000000  # CREATE_NO_WINDOW
            )
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
