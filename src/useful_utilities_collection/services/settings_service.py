# settings_service.py
"""Settings service for UUC.

Provides persistence for user settings via QSettings and exposes helper
functions for autostart and start‑minimized flags.
"""

import sys
from PySide6.QtCore import QSettings

# Import autostart service lazily to avoid circular imports.
from .autostart_service import enable as autostart_enable, disable as autostart_disable, is_enabled as autostart_is_enabled


class SettingsService:
    """Simple wrapper around QSettings for boolean flags.

    The class stores values under the organization and application name
    ``UsefulUtilitiesCollection``.  Boolean values are stored as ``bool`` and
    retrieved with a safe conversion helper.
    """

    def __init__(self):
        self._settings = QSettings("UsefulUtilitiesCollection", "UsefulUtilitiesCollection")

    # ---------------------------------------------------------------------
    # Helper conversion
    # ---------------------------------------------------------------------
    @staticmethod
    def _to_bool(value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return bool(value)

    # ---------------------------------------------------------------------
    # Autostart handling
    # ---------------------------------------------------------------------
    def set_autostart(self, enabled: bool) -> None:
        """Enable or disable Windows autostart and persist the flag."""
        if enabled:
            autostart_enable()
        else:
            autostart_disable()
        self._settings.setValue("autostart_enabled", enabled)

    def is_autostart_enabled(self) -> bool:
        """Return persisted autostart flag (defaults to ``False``)."""
        raw = self._settings.value("autostart_enabled", False)
        return self._to_bool(raw)

    # ---------------------------------------------------------------------
    # Start‑minimized handling (existing functionality)
    # ---------------------------------------------------------------------
    def set_start_minimized(self, enabled: bool) -> None:
        self._settings.setValue("start_minimized", enabled)

    def is_start_minimized(self) -> bool:
        raw = self._settings.value("start_minimized", False)
        return self._to_bool(raw)

    # ---------------------------------------------------------------------
    # Additional getters/setters can be added here as needed.
    # ---------------------------------------------------------------------
