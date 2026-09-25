# autostart_service.py
"""Windows autostart service.

Provides functions to enable, disable, and query a Windows registry entry
that starts the Useful Utilities Collection application on user login.
"""

import os
import sys
import winreg
from pathlib import Path

APP_NAME = "UsefulUtilitiesCollection"
RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def _executable_path() -> str:
    """Return the absolute path that should be launched on login.

    In a development environment this points to the main entry script;
    in a packaged distribution it would be the installed executable.
    """
    # Resolve to the main app.py relative to the repository root.
    repo_root = Path(__file__).resolve().parents[3]  # .../services/ -> repo root
    entry = repo_root / "app.py"
    return str(entry)


def enable() -> None:
    """Create a registry entry under HKCU\Software\Microsoft\Windows\CurrentVersion\Run.

    The entry points to the executable path returned by ``_executable_path``.
    """
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, _executable_path())


def disable() -> None:
    """Remove the autostart registry entry if it exists."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_NAME)
    except FileNotFoundError:
        pass


def is_enabled() -> bool:
    """Return ``True`` if the registry entry exists and points to the current executable."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            return value == _executable_path()
    except FileNotFoundError:
        return False
