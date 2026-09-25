# test_autostart_service.py
"""Unit tests for the Windows autostart service.

The tests mock ``winreg`` to avoid touching the real registry.
"""

import builtins
import importlib
import types
from unittest import mock

# Import the module under test after mocking winreg.

def _import_autostart_module():
    # Ensure winreg is mocked before import.
    mock_winreg = types.SimpleNamespace()
    mock_winreg.HKEY_CURRENT_USER = 0x80000001
    mock_winreg.KEY_SET_VALUE = 0x0002
    mock_winreg.KEY_READ = 0x20019
    mock_winreg.REG_SZ = 1
    mock_winreg._store = {}

    def OpenKey(root, path, reserved=0, access=0):
        return mock_winreg  # use the same object as a context manager

    def SetValueEx(key, name, reserved, type_, value):
        mock_winreg._store[name] = value

    def DeleteValue(key, name):
        mock_winreg._store.pop(name, None)

    def QueryValueEx(key, name):
        if name not in mock_winreg._store:
            raise FileNotFoundError
        return mock_winreg._store[name], mock_winreg.REG_SZ

    mock_winreg.OpenKey = mock.Mock(side_effect=OpenKey)
    mock_winreg.SetValueEx = mock.Mock(side_effect=SetValueEx)
    mock_winreg.DeleteValue = mock.Mock(side_effect=DeleteValue)
    mock_winreg.QueryValueEx = mock.Mock(side_effect=QueryValueEx)

    with mock.patch.dict('sys.modules', {'winreg': mock_winreg}):
        import src.useful_utilities_collection.services.autostart_service as autostart
        return autostart


def test_autostart_enable_disable():
    autostart = _import_autostart_module()
    # Initially disabled
    assert not autostart.is_enabled()
    # Enable and verify
    autostart.enable()
    assert autostart.is_enabled()
    # Disable and verify
    autostart.disable()
    assert not autostart.is_enabled()


def test_settings_service_autostart_integration():
    # Import settings_service after winreg is mocked
    autostart = _import_autostart_module()
    with mock.patch.dict('sys.modules', {'winreg': autostart}):
        from src.useful_utilities_collection.services.settings_service import SettingsService
        svc = SettingsService()
        # Ensure default is False
        assert svc.is_autostart_enabled() is False
        # Enable via settings
        svc.set_autostart(True)
        assert svc.is_autostart_enabled() is True
        assert autostart.is_enabled() is True
        # Disable via settings
        svc.set_autostart(False)
        assert svc.is_autostart_enabled() is False
        assert autostart.is_enabled() is False
