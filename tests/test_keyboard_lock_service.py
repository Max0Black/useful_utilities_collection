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
        self.assertEqual(service._allowed_keys, set())

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_lock_and_unlock(self, mock_keyboard):
        service = KeyboardLockService()
        
        # Lock first time
        res = service.lock(allowed_keys={42, 54})
        self.assertTrue(res)
        self.assertTrue(service.is_locked())
        mock_keyboard.hook.assert_called_once()
        
        # Lock second time should be no-op
        mock_keyboard.hook.reset_mock()
        res_repeat = service.lock(allowed_keys={42, 54})
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
    def test_lock_blocks_non_allowed_keys(self, mock_keyboard):
        service = KeyboardLockService()
        service.lock(allowed_keys={42, 54})
        
        # Allowed key event
        allowed_event = unittest.mock.Mock()
        allowed_event.scan_code = 42
        self.assertTrue(service._on_key_event(allowed_event))
        
        # Blocked key event
        blocked_event = unittest.mock.Mock()
        blocked_event.scan_code = 30
        self.assertFalse(service._on_key_event(blocked_event))

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_shutdown(self, mock_keyboard):
        service = KeyboardLockService()
        service.lock(allowed_keys={42, 54})
        self.assertTrue(service.is_locked())
        
        service.shutdown()
        self.assertFalse(service.is_locked())
        mock_keyboard.unhook.assert_called_once()

if __name__ == "__main__":
    unittest.main()
