import sys
import os
import subprocess
from pathlib import Path

if sys.platform == "win32":
    import winreg


class AutostartService:
    """Service handling Windows autostart registration via registry and startup folder shortcut.
    Mirrors the previous implementation in SettingsService but isolated for reuse.
    """
    APP_NAME = "UsefulUtilitiesCollection"
    RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

    def enable(self) -> bool:
        """Enable autostart. Returns True if either registry or shortcut succeeded."""
        if sys.platform != "win32":
            return False
        reg_success = self._enable_registry()
        shortcut_success = self._create_startup_shortcut(True)
        return reg_success or shortcut_success

    def disable(self) -> bool:
        """Disable autostart. Returns True if either registry or shortcut succeeded."""
        if sys.platform != "win32":
            return False
        reg_success = self._disable_registry()
        shortcut_success = self._create_startup_shortcut(False)
        return reg_success or shortcut_success

    def is_enabled(self) -> bool:
        """Check if autostart is enabled via registry or shortcut."""
        if sys.platform != "win32":
            return False
        reg_exists = False
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.RUN_KEY, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, self.APP_NAME)
            winreg.CloseKey(key)
            reg_exists = True
        except Exception:
            pass
        startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(startup_dir, f"{self.APP_NAME}.lnk")
        shortcut_exists = os.path.exists(shortcut_path)
        return reg_exists or shortcut_exists

    # ---------------------------------------------------------------------
    # Internal helpers for registry manipulation
    # ---------------------------------------------------------------------
    def _enable_registry(self) -> bool:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.RUN_KEY, 0, winreg.KEY_SET_VALUE)
            exe_path = sys.executable
            if "python.exe" in exe_path.lower() or "pythonw.exe" in exe_path.lower():
                # Development mode – point to main.py
                main_py_path = Path(__file__).resolve().parents[2] / "main.py"
                cmd = f'"{exe_path}" "{main_py_path}" --minimized'
            else:
                cmd = f'"{exe_path}" --minimized'
            winreg.SetValueEx(key, self.APP_NAME, 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def _disable_registry(self) -> bool:
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.RUN_KEY, 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, self.APP_NAME)
            except FileNotFoundError:
                pass
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    # ---------------------------------------------------------------------
    # Shortcut creation / removal – copied from SettingsService
    # ---------------------------------------------------------------------
    @staticmethod
    def _create_startup_shortcut(enabled: bool) -> bool:
        """Create or delete the startup folder shortcut.
        Returns True on success (or when disabling and shortcut does not exist)."""
        startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
        shortcut_path = os.path.join(startup_dir, "UsefulUtilitiesCollection.lnk")
        if not enabled:
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                except Exception:
                    pass
            return True
        # Determine target and arguments
        exe_path = sys.executable
        if "python.exe" in exe_path.lower() or "pythonw.exe" in exe_path.lower():
            main_py_path = Path(__file__).resolve().parents[2] / "main.py"
            target_path = exe_path
            arguments = f'"{main_py_path}" --minimized'
            working_dir = str(main_py_path.parent)
        else:
            target_path = exe_path
            arguments = "--minimized"
            working_dir = str(Path(exe_path).parent)
        # PowerShell command to create shortcut
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
