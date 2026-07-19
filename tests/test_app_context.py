import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, MagicMock

# We need a QApplication context for QObject to function properly in PySide6 unit tests
from PySide6.QtWidgets import QApplication

# Initialize a dummy QApplication for the test suite if not already created
qt_app = QApplication.instance()
if qt_app is None:
    qt_app = QApplication([])

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.core.app_state import AppState

class TestAppContext(unittest.TestCase):
    @patch('useful_utilities_collection.core.app_context.SettingsService')
    @patch('useful_utilities_collection.core.app_context.InputLockService')
    @patch('useful_utilities_collection.core.app_context.MicrophoneGuardService')
    @patch('useful_utilities_collection.core.app_context.set_language')
    def test_app_context_initialization(self, mock_set_language, mock_mic_service, mock_input_lock, mock_settings):
        # Setup settings service mock to return a default language
        mock_settings_inst = mock_settings.return_value
        mock_settings_inst.get_language.return_value = "de"
        
        # Setup mic service mock
        mock_mic_service.return_value._guard_enabled = False
        
        context = AppContext()
        
        # Verify app state is initialized
        self.assertIsInstance(context.state, AppState)
        self.assertIsNone(context.state.selected_microphone_id)
        self.assertFalse(context.state.microphone_guard_active)
        
        # Verify dependencies were instantiated and called
        mock_settings.assert_called_once()
        mock_settings_inst.get_language.assert_called_once()
        mock_set_language.assert_called_once_with("de")
        mock_input_lock.assert_called_once_with(mock_settings_inst)
        mock_mic_service.assert_called_once()

    @patch('useful_utilities_collection.core.app_context.SettingsService')
    @patch('useful_utilities_collection.core.app_context.InputLockService')
    @patch('useful_utilities_collection.core.app_context.MicrophoneGuardService')
    @patch('useful_utilities_collection.core.app_context.set_language')
    def test_app_context_signals(self, mock_set_language, mock_mic_service, mock_input_lock, mock_settings):
        context = AppContext()
        
        # Set up a listener for the state_changed signal
        state_changed_called = False
        def on_state_changed():
            nonlocal state_changed_called
            state_changed_called = True
            
        context.state_changed.connect(on_state_changed)
        
        # Trigger changes
        context.notify_state_changed()
        self.assertTrue(state_changed_called)

if __name__ == "__main__":
    unittest.main()
