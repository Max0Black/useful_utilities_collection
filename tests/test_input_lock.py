import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, MagicMock

from useful_utilities_collection.services.input_lock_service import InputLockService
from useful_utilities_collection.services.input_lock_state import InputLockState

class TestInputLockService(unittest.TestCase):
    def setUp(self):
        # Patch KeyboardLockService and MouseLockService to prevent locking the runner's keyboard/mouse
        self.k_lock_patcher = patch('useful_utilities_collection.services.input_lock_service.KeyboardLockService')
        self.m_lock_patcher = patch('useful_utilities_collection.services.input_lock_service.MouseLockService')
        
        self.mock_keyboard_lock_class = self.k_lock_patcher.start()
        self.mock_mouse_lock_class = self.m_lock_patcher.start()

        # Set up instance mocks
        self.mock_keyboard_service = MagicMock()
        self.mock_keyboard_service.lock.return_value = True
        self.mock_keyboard_service.unlock.return_value = True
        self.mock_keyboard_service.is_locked.return_value = False
        self.mock_keyboard_lock_class.return_value = self.mock_keyboard_service

        self.mock_mouse_service = MagicMock()
        self.mock_mouse_service.lock.return_value = True
        self.mock_mouse_service.unlock.return_value = True
        self.mock_mouse_service.is_locked.return_value = False
        self.mock_mouse_lock_class.return_value = self.mock_mouse_service

        # Mock SettingsService to pass to InputLockService
        self.mock_settings = MagicMock()
        self.mock_settings.get_mouse_lock_hotkey.return_value = "Shift+Alt+M"

    def tearDown(self):
        self.k_lock_patcher.stop()
        self.m_lock_patcher.stop()

    def test_initial_state_is_unlocked(self):
        service = InputLockService(self.mock_settings)
        self.assertFalse(service.keyboard_locked())
        self.assertFalse(service.mouse_locked())

    def test_lock_keyboard_blocks_keyboard_and_frees_mouse(self):
        service = InputLockService(self.mock_settings)
        
        # Configure mocked services to report keyboard locked
        self.mock_keyboard_service.is_locked.return_value = True
        self.mock_mouse_service.is_locked.return_value = False
        
        result = service.lock_keyboard()
        
        self.assertTrue(result)
        self.mock_mouse_service.unlock.assert_called_once()
        self.mock_keyboard_service.lock.assert_called_once()
        
        self.assertTrue(service.keyboard_locked())
        self.assertFalse(service.mouse_locked())

    def test_lock_mouse_blocks_mouse_and_frees_keyboard(self):
        service = InputLockService(self.mock_settings)
        
        # Configure mocked services to report mouse locked
        self.mock_keyboard_service.is_locked.return_value = False
        self.mock_mouse_service.is_locked.return_value = True
        
        result = service.lock_mouse()
        
        self.assertTrue(result)
        self.mock_keyboard_service.unlock.assert_called_once()
        self.mock_mouse_service.lock.assert_called_once()
        
        self.assertFalse(service.keyboard_locked())
        self.assertTrue(service.mouse_locked())

    def test_unlock_frees_both_inputs(self):
        service = InputLockService(self.mock_settings)
        
        # Force locked states, then unlock
        self.mock_keyboard_service.is_locked.return_value = False
        self.mock_mouse_service.is_locked.return_value = False
        
        result = service.unlock()
        
        self.assertTrue(result)
        self.mock_keyboard_service.unlock.assert_called()
        self.mock_mouse_service.unlock.assert_called()
        self.assertFalse(service.keyboard_locked())
        self.assertFalse(service.mouse_locked())

if __name__ == "__main__":
    unittest.main()
