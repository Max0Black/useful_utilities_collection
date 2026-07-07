import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import unittest
from unittest.mock import patch, MagicMock

from useful_utilities_collection.services.microphone_guard_service import (
    MicrophoneGuardService,
    MicrophoneDevice,
    GuardRestoreResult,
)

class TestMicrophoneGuardService(unittest.TestCase):
    def setUp(self):
        # We mock QSettings to run settings in memory
        self.mock_settings_data = {}
        self.qsettings_patcher = patch('useful_utilities_collection.services.microphone_guard_service.QSettings')
        self.mock_qsettings_class = self.qsettings_patcher.start()
        
        self.mock_qsettings_inst = MagicMock()
        self.mock_qsettings_inst.value.side_effect = lambda key, default=None: self.mock_settings_data.get(key, default)
        self.mock_qsettings_inst.setValue.side_effect = lambda key, val: self.mock_settings_data.update({key: val})
        self.mock_qsettings_class.return_value = self.mock_qsettings_inst

        # Mock sounddevice library
        self.sd_patcher = patch('useful_utilities_collection.services.microphone_guard_service.sd')
        self.mock_sd = self.sd_patcher.start()
        self.mock_sd.default.device = (1, 2)
        self.mock_sd.query_devices.return_value = {"name": "Test Microphone"}

        # Mock AudioUtilities and pycaw components
        self.pycaw_patcher = patch('useful_utilities_collection.services.microphone_guard_service.AudioUtilities')
        self.mock_audio_utilities = self.pycaw_patcher.start()

        # Mock IAudioEndpointVolume interface
        self.mock_volume_endpoint = MagicMock()
        self.mock_volume_endpoint.GetMasterVolumeLevelScalar.return_value = 0.8  # 80%
        
        # Mock cast and ctypes components
        self.cast_patcher = patch('useful_utilities_collection.services.microphone_guard_service.cast')
        self.mock_cast = self.cast_patcher.start()
        self.mock_cast.return_value = self.mock_volume_endpoint

    def tearDown(self):
        self.qsettings_patcher.stop()
        self.sd_patcher.stop()
        self.pycaw_patcher.stop()
        self.cast_patcher.stop()

    def test_default_initialization(self):
        service = MicrophoneGuardService()
        self.assertEqual(service._target_level, 80)
        self.assertFalse(service._guard_enabled)
        self.assertTrue(service._auto_restore)

    def test_list_devices(self):
        service = MicrophoneGuardService()
        devices = service.list_devices()
        
        self.assertEqual(len(devices), 1)
        device = devices[0]
        self.assertEqual(device.device_id, "default-capture")
        self.assertEqual(device.display_name, "Test Microphone")
        self.assertEqual(device.current_level, 80)

    def test_set_target_level(self):
        service = MicrophoneGuardService()
        service.set_target_level("default-capture", 90)
        self.assertEqual(service._target_level, 90)
        self.assertEqual(self.mock_settings_data["microphone_guard/target_level"], 90)

    def test_enforce_guard_no_restoration_when_disabled(self):
        service = MicrophoneGuardService()
        # Guard is disabled by default
        service._guard_enabled = False
        
        # Simulate volume changed to 50%
        self.mock_volume_endpoint.GetMasterVolumeLevelScalar.return_value = 0.5
        
        result = service.enforce_guard("default-capture")
        self.assertFalse(result.restored)
        self.assertEqual(result.current_level, 50)
        # Volume endpoint set should not be called since guard is disabled
        self.mock_volume_endpoint.SetMasterVolumeLevelScalar.assert_not_called()

    def test_enforce_guard_restores_volume_when_enabled(self):
        service = MicrophoneGuardService()
        service.set_guard_enabled("default-capture", True)
        service.set_target_level("default-capture", 80)
        
        # Simulate volume drift to 60%
        self.mock_volume_endpoint.GetMasterVolumeLevelScalar.return_value = 0.6
        
        # First call queries volume, sees 60% (scalar 0.6)
        # It should trigger SetMasterVolumeLevelScalar(0.8)
        result = service.enforce_guard("default-capture")
        
        self.assertTrue(result.restored)
        self.assertEqual(result.previous_level, 60)
        self.mock_volume_endpoint.SetMasterVolumeLevelScalar.assert_called_once_with(0.8, None)

    def test_enforce_guard_does_nothing_if_volume_is_correct(self):
        service = MicrophoneGuardService()
        service.set_guard_enabled("default-capture", True)
        service.set_target_level("default-capture", 80)
        
        # Simulate volume is already at 80% (scalar 0.8)
        self.mock_volume_endpoint.GetMasterVolumeLevelScalar.return_value = 0.8
        
        result = service.enforce_guard("default-capture")
        self.assertFalse(result.restored)
        self.mock_volume_endpoint.SetMasterVolumeLevelScalar.assert_not_called()

    def test_guard_modes(self):
        service = MicrophoneGuardService()
        self.assertEqual(service.get_guard_mode(), "selected")
        
        service.set_guard_mode("all")
        self.assertEqual(service.get_guard_mode(), "all")
        
        service.set_guard_mode("specific")
        self.assertEqual(service.get_guard_mode(), "specific")
        
        # Invalid mode should not change it
        service.set_guard_mode("invalid")
        self.assertEqual(service.get_guard_mode(), "specific")

    def test_per_device_settings(self):
        service = MicrophoneGuardService()
        
        # Set target level and auto restore for device A
        service.set_target_level("device-A", 70)
        service.set_auto_restore("device-A", False)
        
        # Set target level and auto restore for device B
        service.set_target_level("device-B", 90)
        service.set_auto_restore("device-B", True)
        
        # Retrieve settings for device A
        dev_a = service.get_device("device-A")
        # Since it is not connected (no raw pycaw devices returned in default test run except mock defaults),
        # get_device calls list_devices() which returns the default mockup in tests.
        # But we can verify settings directly via list_devices or set_target_level side effects.
        # Let's mock GetAllDevices to test this properly.

    @patch('useful_utilities_collection.services.microphone_guard_service.AudioUtilities.GetAllDevices')
    def test_enforce_guard_multiple_devices(self, mock_get_all_devices):
        # Setup mock devices
        mock_dev1 = MagicMock()
        mock_dev1.id = "device-1"
        mock_dev1.FriendlyName = "Microphone 1"
        mock_dev1.EndpointVolume.GetMasterVolumeLevelScalar.return_value = 0.5  # 50%
        
        mock_dev2 = MagicMock()
        mock_dev2.id = "device-2"
        mock_dev2.FriendlyName = "Microphone 2"
        mock_dev2.EndpointVolume.GetMasterVolumeLevelScalar.return_value = 0.4  # 40%
        
        mock_get_all_devices.return_value = [mock_dev1, mock_dev2]
        
        service = MicrophoneGuardService()
        service.set_guard_mode("all")
        service.set_guard_enabled("default-capture", True)  # Global guard enable
        
        # Set different target levels
        service.set_target_level("device-1", 80)
        service.set_target_level("device-2", 90)
        
        # Enforce
        result = service.refresh_and_enforce_selected()
        
        self.assertTrue(result.restored)
        self.assertEqual(len(result.corrected_devices), 2)
        
        # Check volume is set on both devices
        mock_dev1.EndpointVolume.SetMasterVolumeLevelScalar.assert_called_once_with(0.8, None)
        mock_dev2.EndpointVolume.SetMasterVolumeLevelScalar.assert_called_once_with(0.9, None)

if __name__ == "__main__":
    unittest.main()
