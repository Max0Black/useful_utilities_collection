import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, MagicMock
from PySide6.QtCore import QSettings

from useful_utilities_collection.services.settings_service import SettingsService

class TestSettingsService(unittest.TestCase):
    def setUp(self):
        # We mock QSettings to prevent tests from writing to the system registry/config
        self.mock_settings_data = {}
        
        def mock_value(key, default=None):
            return self.mock_settings_data.get(key, default)
            
        def mock_set_value(key, value):
            self.mock_settings_data[key] = value

        self.qsettings_patcher = patch('useful_utilities_collection.services.settings_service.QSettings')
        self.mock_qsettings_class = self.qsettings_patcher.start()
        
        self.mock_qsettings_inst = MagicMock(spec=QSettings)
        self.mock_qsettings_inst.value.side_effect = mock_value
        self.mock_qsettings_inst.setValue.side_effect = mock_set_value
        self.mock_qsettings_class.return_value = self.mock_qsettings_inst

    def tearDown(self):
        self.qsettings_patcher.stop()

    def test_default_values(self):
        # When settings are empty, verify the default fallbacks
        service = SettingsService()
        self.assertEqual(service.get_language(), "en")
        self.assertTrue(service.get_close_to_tray())
        self.assertEqual(service.get_guard_interval(), 1500)
        self.assertEqual(service.get_mouse_lock_hotkey(), "Shift+Alt+M")

    def test_get_set_language(self):
        service = SettingsService()
        service.set_language("de")
        self.assertEqual(service.get_language(), "de")
        self.assertEqual(self.mock_settings_data["general/language"], "de")

    def test_get_set_close_to_tray(self):
        service = SettingsService()
        service.set_close_to_tray(False)
        self.assertFalse(service.get_close_to_tray())
        self.assertEqual(self.mock_settings_data["general/close_to_tray"], False)

    def test_get_set_guard_interval(self):
        service = SettingsService()
        service.set_guard_interval(2000)
        self.assertEqual(service.get_guard_interval(), 2000)
        self.assertEqual(self.mock_settings_data["microphone_guard/interval"], 2000)

    def test_get_set_mouse_lock_hotkey(self):
        service = SettingsService()
        service.set_mouse_lock_hotkey("Ctrl+Alt+X")
        self.assertEqual(service.get_mouse_lock_hotkey(), "Ctrl+Alt+X")
        self.assertEqual(self.mock_settings_data["input_lock/mouse_lock_hotkey"], "Ctrl+Alt+X")

    @patch('sys.platform', 'win32')
    @patch('winreg.CloseKey')
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx')
    def test_is_startup_enabled_win32(self, mock_query, mock_open, mock_close):
        # Mock winreg behavior for win32
        mock_query.return_value = ("some_cmd", 1)
        service = SettingsService()
        self.assertTrue(service.is_startup_enabled())
        mock_open.assert_called_once()
        mock_close.assert_called_once()

    @patch('sys.platform', 'linux')
    def test_is_startup_enabled_non_win32(self):
        service = SettingsService()
        self.assertFalse(service.is_startup_enabled())

if __name__ == "__main__":
    unittest.main()
