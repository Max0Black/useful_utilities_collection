import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, call

from useful_utilities_collection.services.keyboard_lock_service import KeyboardLockService

class TestKeyboardLockService(unittest.TestCase):
    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_initial_state(self, mock_keyboard):
        service = KeyboardLockService()
        self.assertFalse(service.is_locked())

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_lock_and_unlock(self, mock_keyboard):
        service = KeyboardLockService()
        
        # Lock first time
        res = service.lock()
        self.assertTrue(res)
        self.assertTrue(service.is_locked())
        mock_keyboard.hook.assert_called_once()
        
        # Lock second time should be no-op
        mock_keyboard.hook.reset_mock()
        res_repeat = service.lock()
        self.assertTrue(res_repeat)
        self.assertTrue(service.is_locked())
        mock_keyboard.hook.assert_not_called()
        
        # Unlock
        res_unlock = service.unlock()
        self.assertTrue(res_unlock)
        self.assertFalse(service.is_locked())
        mock_keyboard.unhook.assert_called_once()
        
        # Unlock second time should be no-op
        mock_keyboard.unhook.reset_mock()
        res_unlock_repeat = service.unlock()
        self.assertTrue(res_unlock_repeat)
        mock_keyboard.unhook.assert_not_called()

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_lock_blocks_all_keys(self, mock_keyboard):
        service = KeyboardLockService()
        service.lock()
        
        # Any key press should return False (False = block in Windows keyboard hook)
        event_shift_dn = unittest.mock.Mock()
        event_shift_dn.name = "shift"
        event_shift_dn.event_type = "down"
        self.assertFalse(service._on_key_event(event_shift_dn))  # False = block

        # Pressing 'a' key alone should be blocked
        event_a_dn = unittest.mock.Mock()
        event_a_dn.name = "a"
        event_a_dn.event_type = "down"
        self.assertFalse(service._on_key_event(event_a_dn))

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_shutdown(self, mock_keyboard):
        service = KeyboardLockService()
        service.lock()
        self.assertTrue(service.is_locked())
        
        service.shutdown()
        self.assertFalse(service.is_locked())
        mock_keyboard.unhook.assert_called_once()

if __name__ == "__main__":
    unittest.main()
