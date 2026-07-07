import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, MagicMock

# Import the service. Since ctypes is used inside the class, we can mock user32 directly on the instances.
from useful_utilities_collection.services.mouse_lock_service import MouseLockService

class TestMouseLockService(unittest.TestCase):
    def setUp(self):
        self.mock_settings = MagicMock()
        self.mock_settings.get_mouse_lock_hotkey.return_value = "Shift+Alt+M"

        # Mock keyboard and mouse libraries
        self.keyboard_patcher = patch('useful_utilities_collection.services.mouse_lock_service.keyboard')
        self.mouse_patcher = patch('useful_utilities_collection.services.mouse_lock_service.mouse')
        self.mock_keyboard = self.keyboard_patcher.start()
        self.mock_mouse = self.mouse_patcher.start()

        # Mock the Listener
        self.mock_listener_inst = MagicMock()
        self.mock_mouse.Listener.return_value = self.mock_listener_inst

        # Setup user32 mock
        self.mock_user32 = MagicMock()
        self.mock_user32.ClipCursor.return_value = 1
        
        # Mock GetCursorPos to set point coordinates
        def get_cursor_pos_side_effect(point_ref):
            if hasattr(point_ref, '_obj'):
                point_ref._obj.x = 100
                point_ref._obj.y = 200
            elif hasattr(point_ref, 'contents'):
                point_ref.contents.x = 100
                point_ref.contents.y = 200
            return 1
        self.mock_user32.GetCursorPos.side_effect = get_cursor_pos_side_effect

    def tearDown(self):
        self.keyboard_patcher.stop()
        self.mouse_patcher.stop()

    def test_initial_state(self):
        service = MouseLockService(self.mock_settings)
        service._user32 = self.mock_user32
        
        self.assertFalse(service.is_locked())
        self.assertIsNone(service._anchor)

    def test_lock_success(self):
        service = MouseLockService(self.mock_settings)
        service._user32 = self.mock_user32
        
        res = service.lock()
        
        self.assertTrue(res)
        self.assertTrue(service.is_locked())
        self.assertEqual(service._anchor, (100, 200))
        
        # Verify user32 was called
        self.mock_user32.GetCursorPos.assert_called_once()
        self.mock_user32.ClipCursor.assert_called_once()
        
        # Verify listener started
        self.mock_mouse.Listener.assert_called_once()
        self.mock_listener_inst.start.assert_called_once()
        
        # Verify hotkey registered
        self.mock_keyboard.add_hotkey.assert_called_once()

    def test_lock_failure_in_clip(self):
        self.mock_user32.ClipCursor.return_value = 0  # ClipCursor fails
        
        service = MouseLockService(self.mock_settings)
        service._user32 = self.mock_user32
        
        res = service.lock()
        self.assertFalse(res)
        self.assertFalse(service.is_locked())
        self.assertIsNone(service._anchor)

    def test_unlock_success(self):
        service = MouseLockService(self.mock_settings)
        service._user32 = self.mock_user32
        
        # Lock first
        service.lock()
        self.assertTrue(service.is_locked())
        
        # Reset mocks to verify unlock calls
        self.mock_user32.ClipCursor.reset_mock()
        self.mock_listener_inst.stop.reset_mock()
        self.mock_keyboard.remove_hotkey.reset_mock()
        
        res = service.unlock()
        
        self.assertTrue(res)
        self.assertFalse(service.is_locked())
        self.assertIsNone(service._anchor)
        
        # Verify listener stopped
        self.mock_listener_inst.stop.assert_called_once()
        # Verify hotkey removed
        self.mock_keyboard.remove_hotkey.assert_called_once()
        # Verify cursor released
        self.mock_user32.ClipCursor.assert_called_once_with(None)

    def test_hotkey_conversion(self):
        service = MouseLockService(self.mock_settings)
        # test mapping keys
        self.assertEqual(service._convert_portable_hotkey_to_keyboard("Ctrl+Alt+Shift+Meta+Z"), "ctrl+alt+shift+win+z")
        self.assertEqual(service._convert_portable_hotkey_to_keyboard("PgUp,PgDn"), "page up")
        self.assertEqual(service._convert_portable_hotkey_to_keyboard(""), service.EMERGENCY_HOTKEY)

    def test_emergency_unlock_flow(self):
        service = MouseLockService(self.mock_settings)
        self.assertFalse(service.consume_emergency_unlock_request())
        
        service.request_emergency_unlock()
        self.assertTrue(service.consume_emergency_unlock_request())
        self.assertFalse(service.consume_emergency_unlock_request())

if __name__ == "__main__":
    unittest.main()
