import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import MagicMock, patch

from useful_utilities_collection.modules.microphone_guard.controller import MicrophoneGuardController
from useful_utilities_collection.modules.input_lock.controller import InputLockController

class TestControllers(unittest.TestCase):
    def setUp(self):
        self.mock_context = MagicMock()
        
    def test_microphone_guard_controller_refresh_devices(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.refresh_devices()
        
        self.mock_context.microphone_guard_service.refresh_devices.assert_called_once()
        self.mock_context.microphone_guard_service.refresh_and_enforce_selected.assert_called_once()
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_refresh_selected(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.refresh_selected()
        
        self.mock_context.microphone_guard_service.refresh_selected_device_state.assert_called_once()
        self.mock_context.microphone_guard_service.refresh_and_enforce_selected.assert_called_once()
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_select_device(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.select_device("some-device")
        
        self.assertEqual(self.mock_context.state.selected_microphone_id, "some-device")
        self.mock_context.microphone_guard_service.set_selected_device_id.assert_called_once_with("some-device")
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_set_target_level(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.set_target_level("device-id", 75)
        
        self.mock_context.microphone_guard_service.set_target_level.assert_called_once_with("device-id", 75)
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_set_current_level(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.set_current_level("device-id", 60)
        
        self.mock_context.microphone_guard_service.set_current_level.assert_called_once_with("device-id", 60)
        self.mock_context.microphone_guard_service.refresh_selected_device_state.assert_called_once()
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_set_auto_restore(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.set_auto_restore("device-id", True)
        
        self.mock_context.microphone_guard_service.set_auto_restore.assert_called_once_with("device-id", True)
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_enable_guard(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.enable_guard("device-id")
        
        self.mock_context.microphone_guard_service.set_guard_enabled.assert_called_once_with("device-id", True)
        self.assertTrue(self.mock_context.state.microphone_guard_active)
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_disable_guard(self):
        controller = MicrophoneGuardController(self.mock_context)
        controller.disable_guard("device-id")
        
        self.mock_context.microphone_guard_service.set_guard_enabled.assert_called_once_with("device-id", False)
        self.assertFalse(self.mock_context.state.microphone_guard_active)
        self.mock_context.notify_state_changed.assert_called_once()

    def test_microphone_guard_controller_sync_target_to_current(self):
        mock_device = MagicMock()
        mock_device.current_level = 85
        self.mock_context.microphone_guard_service.get_device.return_value = mock_device
        
        controller = MicrophoneGuardController(self.mock_context)
        controller.sync_target_to_current("device-id")
        
        self.mock_context.microphone_guard_service.get_device.assert_called_once_with("device-id")
        self.mock_context.microphone_guard_service.set_target_level.assert_called_once_with("device-id", 85)
        self.mock_context.notify_state_changed.assert_called_once()

    def test_input_lock_controller_toggle_keyboard_lock(self):
        controller = InputLockController(self.mock_context)
        
        # Scenario 1: Currently locked -> should unlock
        self.mock_context.input_lock_service.keyboard_locked.return_value = True
        controller.toggle_keyboard_lock()
        self.mock_context.input_lock_service.unlock_keyboard.assert_called_once()
        self.mock_context.input_lock_service.lock_keyboard.assert_not_called()
        
        # Scenario 2: Currently unlocked -> should lock
        self.mock_context.input_lock_service.unlock_keyboard.reset_mock()
        self.mock_context.input_lock_service.keyboard_locked.return_value = False
        controller.toggle_keyboard_lock()
        self.mock_context.input_lock_service.lock_keyboard.assert_called_once()
        self.mock_context.input_lock_service.unlock_keyboard.assert_not_called()

    def test_input_lock_controller_toggle_mouse_lock(self):
        controller = InputLockController(self.mock_context)
        
        # Scenario 1: Currently locked -> should unlock
        self.mock_context.input_lock_service.mouse_locked.return_value = True
        controller.toggle_mouse_lock()
        self.mock_context.input_lock_service.unlock_mouse.assert_called_once()
        self.mock_context.input_lock_service.lock_mouse.assert_not_called()
        
        # Scenario 2: Currently unlocked -> should lock
        self.mock_context.input_lock_service.unlock_mouse.reset_mock()
        self.mock_context.input_lock_service.mouse_locked.return_value = False
        controller.toggle_mouse_lock()
        self.mock_context.input_lock_service.lock_mouse.assert_called_once()
        self.mock_context.input_lock_service.unlock_mouse.assert_not_called()

    def test_input_lock_controller_unlock_all(self):
        controller = InputLockController(self.mock_context)
        controller.unlock_all()
        self.mock_context.input_lock_service.unlock.assert_called_once()

    def test_input_lock_controller_enforce(self):
        controller = InputLockController(self.mock_context)
        
        # Service has no mouse_lock_service attribute
        del self.mock_context.input_lock_service.mouse_lock_service
        controller.enforce() # should not raise error
        
        # Service has mouse_lock_service but no enforce method
        mock_mouse_service = MagicMock()
        del mock_mouse_service.enforce
        self.mock_context.input_lock_service.mouse_lock_service = mock_mouse_service
        controller.enforce() # should not raise error
        
        # Service has mouse_lock_service with enforce method
        mock_enforce = MagicMock()
        mock_mouse_service.enforce = mock_enforce
        controller.enforce()
        mock_enforce.assert_called_once()

if __name__ == "__main__":
    unittest.main()
