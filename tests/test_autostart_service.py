import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, MagicMock

from useful_utilities_collection.services.autostart_service import AutostartService


class TestAutostartService(unittest.TestCase):
    def setUp(self):
        # Patch winreg at module level in autostart_service
        self.mock_winreg = MagicMock()
        self.mock_winreg.HKEY_CURRENT_USER = 0x80000001
        self.mock_winreg.KEY_READ = 0x20019
        self.mock_winreg.KEY_SET_VALUE = 0x0002
        self.mock_winreg.REG_SZ = 1
        self.winreg_patcher = patch(
            'useful_utilities_collection.services.autostart_service.winreg',
            self.mock_winreg
        )
        # Patch sys.platform to win32
        self.platform_patcher = patch(
            'useful_utilities_collection.services.autostart_service.sys.platform',
            'win32'
        )
        # Patch subprocess for shortcut creation
        self.subprocess_patcher = patch(
            'useful_utilities_collection.services.autostart_service.subprocess'
        )
        # Patch os.path.exists for shortcut check
        self.exists_patcher = patch(
            'useful_utilities_collection.services.autostart_service.os.path.exists',
            return_value=False
        )
        self.winreg_patcher.start()
        self.platform_patcher.start()
        self.mock_subprocess = self.subprocess_patcher.start()
        self.exists_patcher.start()

        self.mock_subprocess.run.return_value = MagicMock(returncode=0)

    def tearDown(self):
        self.winreg_patcher.stop()
        self.platform_patcher.stop()
        self.subprocess_patcher.stop()
        self.exists_patcher.stop()

    def test_enable_writes_registry(self):
        svc = AutostartService()
        result = svc.enable()
        self.assertTrue(result)
        self.mock_winreg.OpenKey.assert_called()
        self.mock_winreg.SetValueEx.assert_called()

    def test_disable_deletes_registry(self):
        svc = AutostartService()
        result = svc.disable()
        self.assertTrue(result)
        self.mock_winreg.OpenKey.assert_called()
        self.mock_winreg.DeleteValue.assert_called()

    def test_is_enabled_returns_true_when_key_exists(self):
        self.mock_winreg.QueryValueEx.return_value = ("some_cmd", 1)
        svc = AutostartService()
        result = svc.is_enabled()
        self.assertTrue(result)

    def test_is_enabled_returns_false_when_key_missing(self):
        self.mock_winreg.OpenKey.side_effect = WindowsError("not found")
        svc = AutostartService()
        result = svc.is_enabled()
        self.assertFalse(result)

    def test_is_enabled_non_win32(self):
        self.platform_patcher.stop()
        with patch('useful_utilities_collection.services.autostart_service.sys.platform', 'linux'):
            import importlib
            import useful_utilities_collection.services.autostart_service as autostart_service
            importlib.reload(autostart_service)
            svc = autostart_service.AutostartService()
            self.assertFalse(svc.is_enabled())
        self.platform_patcher.start()


if __name__ == "__main__":
    unittest.main()
