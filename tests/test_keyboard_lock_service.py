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
        self.assertEqual(service._blocked_keys, [])

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_lock_and_unlock(self, mock_keyboard):
        service = KeyboardLockService()
        
        # Lock first time
        res = service.lock()
        self.assertTrue(res)
        self.assertTrue(service.is_locked())
        self.assertEqual(len(service._blocked_keys), 150)
        self.assertEqual(mock_keyboard.block_key.call_count, 150)
        
        # Lock second time should be no-op
        mock_keyboard.block_key.reset_mock()
        res_repeat = service.lock()
        self.assertTrue(res_repeat)
        self.assertTrue(service.is_locked())
        mock_keyboard.block_key.assert_not_called()
        
        # Unlock
        res_unlock = service.unlock()
        self.assertTrue(res_unlock)
        self.assertFalse(service.is_locked())
        self.assertEqual(service._blocked_keys, [])
        self.assertEqual(mock_keyboard.unblock_key.call_count, 150)
        
        # Unlock second time should be no-op
        mock_keyboard.unblock_key.reset_mock()
        res_unlock_repeat = service.unlock()
        self.assertTrue(res_unlock_repeat)
        mock_keyboard.unblock_key.assert_not_called()

    @patch('useful_utilities_collection.services.keyboard_lock_service.keyboard')
    def test_lock_with_exceptions(self, mock_keyboard):
        # block_key raises exception for some keys
        def side_effect_fn(k):
            if k % 2 != 0:
                raise Exception("Forbidden")
        mock_keyboard.block_key.side_effect = side_effect_fn
        
        service = KeyboardLockService()
        res = service.lock()
        self.assertTrue(res)
        self.assertTrue(service.is_locked())
        # only even keys should be added (75 keys)
        self.assertEqual(len(service._blocked_keys), 75)
        
        # Unlocking should only call unblock_key on the successfully blocked keys
        mock_keyboard.unblock_key.side_effect = Exception("Failed unblock")
        res_unlock = service.unlock()
        self.assertTrue(res_unlock)
        self.assertEqual(mock_keyboard.unblock_key.call_count, 75)
        self.assertFalse(service.is_locked())

if __name__ == "__main__":
    unittest.main()
