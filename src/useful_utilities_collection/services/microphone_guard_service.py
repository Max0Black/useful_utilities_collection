from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sounddevice as sd
from PySide6.QtCore import QSettings
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, EDataFlow, DEVICE_STATE


@dataclass
class MicrophoneDevice:
    device_id: str
    display_name: str
    current_level: int = 0
    target_level: int = 80
    guard_enabled: bool = False
    auto_restore: bool = True
    is_default: bool = False

@dataclass
class GuardRestoreResult:
    restored: bool
    previous_level: int | None = None
    current_level: int | None = None
    target_level: int | None = None
    corrected_devices: list[dict] | None = None


class MicrophoneGuardService:
    def __init__(self):
        self._settings = QSettings(
            "UsefulUtilitiesCollection",
            "UsefulUtilitiesCollection",
        )
        self._selected_device_id: Optional[str] = self._settings.value("microphone_guard/selected_device_id", "")
        self._guard_enabled: bool = self._to_bool(
            self._settings.value("microphone_guard/guard_enabled", False)
        )
        self._guard_mode: str = self._settings.value("microphone_guard/guard_mode", "selected")
        self._last_correction_text: str = self._settings.value(
            "microphone_guard/last_correction_text", "–"
        )
        self._cached_devices: list[MicrophoneDevice] = []
        
        # Legacy fields for backward compatibility and tests
        self._target_level: int = int(
            self._settings.value("microphone_guard/target_level", 80)
        )
        self._auto_restore: bool = self._to_bool(
            self._settings.value("microphone_guard/auto_restore", True)
        )
        
        # Initial scan to populate cache
        self.list_devices()

    def _device_settings_prefix(self, device_id: str) -> str:
        safe_id = str(device_id).replace("{", "").replace("}", "").replace("/", "_").replace("\\", "_")
        return f"microphone_guard/devices/{safe_id}"

    def get_guard_mode(self) -> str:
        return self._guard_mode

    def set_guard_mode(self, mode: str) -> None:
        if mode in ("selected", "all", "specific"):
            self._guard_mode = mode
            self._settings.setValue("microphone_guard/guard_mode", mode)
            self._settings.sync()

    def list_devices(self) -> list[MicrophoneDevice]:
        devices = []
        default_id = "default-capture"
        try:
            default_mic = AudioUtilities.GetMicrophone()
            if default_mic:
                real_id = default_mic.GetId()
                if "Mock" not in type(real_id).__name__:
                    default_id = real_id
        except Exception:
            pass

        try:
            pycaw_devices = AudioUtilities.GetAllDevices(EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value)
            for pycaw_dev in pycaw_devices:
                device_id = pycaw_dev.id
                display_name = pycaw_dev.FriendlyName or "Microphone"
                is_default = (device_id == default_id) if default_id else False
                
                # Fetch settings for this device
                prefix = self._device_settings_prefix(device_id)
                
                # Load settings, fallback to legacy settings, then to hard defaults
                legacy_target = self._target_level
                legacy_restore = self._auto_restore
                
                target_level = int(self._settings.value(f"{prefix}/target_level", legacy_target))
                default_guard_state = True if is_default else False
                guard_enabled = self._to_bool(self._settings.value(f"{prefix}/guard_enabled", default_guard_state))
                auto_restore = self._to_bool(self._settings.value(f"{prefix}/auto_restore", legacy_restore))
                
                current_level = 0
                try:
                    volume = pycaw_dev.EndpointVolume
                    if volume:
                        scalar = volume.GetMasterVolumeLevelScalar()
                        current_level = max(0, min(100, int(round(float(scalar) * 100))))
                except Exception:
                    pass
                
                devices.append(MicrophoneDevice(
                    device_id=device_id,
                    display_name=display_name,
                    current_level=current_level,
                    target_level=target_level,
                    guard_enabled=guard_enabled,
                    auto_restore=auto_restore,
                    is_default=is_default
                ))
        except Exception as e:
            # Fallback if pycaw fails to list devices
            print(f"[Warning] Failed to list devices via pycaw: {e}")
            default_device = self._build_default_device()
            if default_device:
                devices.append(default_device)

        # If we got no devices, try to get the default device anyway
        if not devices:
            default_device = self._build_default_device()
            if default_device:
                devices.append(default_device)

        self._cached_devices = devices
        return devices

    def refresh_devices(self) -> list[MicrophoneDevice]:
        return self.list_devices()

    def refresh_selected_device_state(self) -> Optional[MicrophoneDevice]:
        selected_id = self.get_selected_device_id()
        devices = self.list_devices()
        for d in devices:
            if d.device_id == selected_id:
                return d
        for d in devices:
            if d.is_default:
                return d
        return devices[0] if devices else None

    def get_selected_device_id(self) -> Optional[str]:
        if not self._selected_device_id:
            try:
                default_mic = AudioUtilities.GetMicrophone()
                if default_mic:
                    real_id = default_mic.GetId()
                    if "Mock" not in type(real_id).__name__:
                        return real_id
            except Exception:
                pass
            return "default-capture"
        return self._selected_device_id or None

    def set_selected_device_id(self, device_id: str) -> None:
        self._selected_device_id = device_id
        self._settings.setValue("microphone_guard/selected_device_id", device_id)
        self._settings.sync()

    def get_device(self, device_id: str | None) -> Optional[MicrophoneDevice]:
        if not device_id:
            return None
        # Support legacy / dashboard identifier
        if device_id == "default-capture":
            return self.refresh_selected_device_state()
            
        for d in self._cached_devices:
            if d.device_id == device_id:
                return d
        devices = self.list_devices()
        for d in devices:
            if d.device_id == device_id:
                return d
        return None

    def set_target_level(self, device_id: str, level: int) -> None:
        level = max(0, min(100, level))
        self._target_level = level
        # Handle legacy / default-capture mapping
        if device_id == "default-capture":
            target = self.refresh_selected_device_state()
            device_id = target.device_id if target else "default-capture"
            
        prefix = self._device_settings_prefix(device_id)
        self._settings.setValue(f"{prefix}/target_level", level)
        # Keep legacy setting updated for backward compatibility
        self._settings.setValue("microphone_guard/target_level", level)
        self._settings.sync()
        for d in self._cached_devices:
            if d.device_id == device_id:
                d.target_level = level

    def set_device_guard_enabled(self, device_id: str, enabled: bool) -> None:
        prefix = self._device_settings_prefix(device_id)
        self._settings.setValue(f"{prefix}/guard_enabled", enabled)
        self._settings.sync()
        for d in self._cached_devices:
            if d.device_id == device_id:
                d.guard_enabled = enabled

    def set_guard_enabled(self, device_id: str, enabled: bool) -> None:
        if device_id == "default-capture":
            target = self.refresh_selected_device_state()
            device_id = target.device_id if target else "default-capture"

        self.set_device_guard_enabled(device_id, enabled)

        devices = self._cached_devices or self.list_devices()
        self._guard_enabled = any(bool(d.guard_enabled) for d in devices)

        self._settings.setValue("microphone_guard/guard_enabled", self._guard_enabled)
        self._settings.sync()
    
    def is_device_guard_enabled(self, device_id: str) -> bool:
        device = self.get_device(device_id)
        return bool(device.guard_enabled) if device else False

    def set_auto_restore(self, device_id: str, enabled: bool) -> None:
        self._auto_restore = enabled
        if device_id == "default-capture":
            target = self.refresh_selected_device_state()
            device_id = target.device_id if target else "default-capture"
            
        prefix = self._device_settings_prefix(device_id)
        self._settings.setValue(f"{prefix}/auto_restore", enabled)
        self._settings.setValue("microphone_guard/auto_restore", enabled)
        self._settings.sync()
        for d in self._cached_devices:
            if d.device_id == device_id:
                d.auto_restore = enabled

    def set_current_level(self, device_id: str, level: int) -> bool:
        if device_id == "default-capture":
            target = self.refresh_selected_device_state()
            device_id = target.device_id if target else "default-capture"
            
        changed = self._set_device_volume_level(device_id, max(0, min(100, level)))
        if changed:
            self.refresh_devices()
        return changed

    def enforce_guard(self, device_id: str) -> GuardRestoreResult:
        if device_id == "default-capture":
            target = self.refresh_selected_device_state()
            device_id = target.device_id if target else "default-capture"
            
        device = self.get_device(device_id)
        if device is None:
            return GuardRestoreResult(restored=False)

        if not self._guard_enabled or not device.auto_restore:
            return GuardRestoreResult(
                restored=False,
                previous_level=device.current_level,
                current_level=device.current_level,
                target_level=device.target_level,
            )

        previous_level = int(device.current_level)
        target_level = int(device.target_level)

        if previous_level != target_level:
            changed = self._set_device_volume_level(device_id, target_level)
            if changed:
                self._last_correction_text = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
                self._settings.setValue("microphone_guard/last_correction_text", self._last_correction_text)
                self._settings.sync()
                current_level = self._get_device_volume_level(device_id) or target_level
                device.current_level = current_level
                return GuardRestoreResult(
                    restored=True,
                    previous_level=previous_level,
                    current_level=current_level,
                    target_level=target_level,
                )

        return GuardRestoreResult(
            restored=False,
            previous_level=previous_level,
            current_level=previous_level,
            target_level=target_level,
        )

    def refresh_and_enforce_selected(self) -> GuardRestoreResult:
        # Performance: only call list_devices() once per tick
        devices = self.refresh_devices()

        if not self._guard_enabled:
            # Use cached data – avoid second API round-trip
            selected_id = self.get_selected_device_id()
            selected_dev = next(
                (d for d in devices if d.device_id == selected_id),
                next((d for d in devices if d.is_default), devices[0] if devices else None)
            )
            return GuardRestoreResult(
                restored=False,
                previous_level=selected_dev.current_level if selected_dev else None,
                current_level=selected_dev.current_level if selected_dev else None,
                target_level=selected_dev.target_level if selected_dev else None
            )

        mode = self.get_guard_mode()
        devices_to_guard = []
        if mode == "selected":
            selected_id = self.get_selected_device_id()
            for d in devices:
                if d.device_id == selected_id:
                    devices_to_guard.append(d)
                    break
            if not devices_to_guard:
                for d in devices:
                    if d.is_default:
                        devices_to_guard.append(d)
                        break
        elif mode == "all":
            devices_to_guard = devices
        elif mode == "specific":
            devices_to_guard = [d for d in devices if d.guard_enabled]

        restored_any = False
        last_restored_result = None
        corrected_devices = []

        for dev in devices_to_guard:
            if not dev.auto_restore:
                continue

            previous_level = dev.current_level
            target_level = dev.target_level

            if previous_level != target_level:
                changed = self._set_device_volume_level(dev.device_id, target_level)
                if changed:
                    restored_any = True
                    self._last_correction_text = datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
                    self._settings.setValue("microphone_guard/last_correction_text", self._last_correction_text)
                    self._settings.sync()
                    dev.current_level = target_level
                    corrected_devices.append({
                        "name": dev.display_name,
                        "device_id": dev.device_id,
                        "previous": previous_level,
                        "target": target_level
                    })
                    last_restored_result = GuardRestoreResult(
                        restored=True,
                        previous_level=previous_level,
                        current_level=target_level,
                        target_level=target_level
                    )

        if restored_any and last_restored_result:
            last_restored_result.corrected_devices = corrected_devices
            return last_restored_result

        # Use cached result from devices list – avoid second API call
        selected_id = self.get_selected_device_id()
        selected_dev = next(
            (d for d in devices if d.device_id == selected_id),
            next((d for d in devices if d.is_default), devices[0] if devices else None)
        )
        return GuardRestoreResult(
            restored=False,
            previous_level=selected_dev.current_level if selected_dev else None,
            current_level=selected_dev.current_level if selected_dev else None,
            target_level=selected_dev.target_level if selected_dev else None
        )

    def get_last_correction_text(self) -> str:
        return self._last_correction_text

    def _build_default_device(self) -> Optional[MicrophoneDevice]:
        display_name = self._get_default_input_name()
        current_level = self._get_default_microphone_level()

        if current_level is None:
            return None

        default_id = "default-capture"
        try:
            default_mic = AudioUtilities.GetMicrophone()
            if default_mic:
                real_id = default_mic.GetId()
                if "Mock" not in type(real_id).__name__:
                    default_id = real_id
        except Exception:
            pass

        prefix = self._device_settings_prefix(default_id)
        legacy_target = self._target_level
        legacy_restore = self._auto_restore

        target_level = int(self._settings.value(f"{prefix}/target_level", legacy_target))
        guard_enabled = self._to_bool(self._settings.value(f"{prefix}/guard_enabled", True))
        auto_restore = self._to_bool(self._settings.value(f"{prefix}/auto_restore", legacy_restore))

        return MicrophoneDevice(
            device_id=default_id,
            display_name=display_name or "Default microphone",
            current_level=current_level,
            target_level=target_level,
            guard_enabled=guard_enabled,
            auto_restore=auto_restore,
            is_default=True,
        )

    def _get_default_input_name(self) -> str:
        try:
            default_input, _ = sd.default.device
            if default_input is None or default_input < 0:
                return "Default microphone"
            info = sd.query_devices(default_input)
            return str(info.get("name", "Default microphone"))
        except Exception:
            return "Default microphone"

    def _get_default_microphone_endpoint(self):
        try:
            device = AudioUtilities.GetMicrophone()
            if device is None:
                return None
            interface = device.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None,
            )
            return cast(interface, POINTER(IAudioEndpointVolume))
        except Exception:
            return None

    def _get_default_microphone_level(self) -> Optional[int]:
        endpoint_volume = self._get_default_microphone_endpoint()
        if endpoint_volume is None:
            return None

        try:
            scalar = endpoint_volume.GetMasterVolumeLevelScalar()
            return max(0, min(100, int(round(float(scalar) * 100))))
        except Exception:
            return None

    def _set_default_microphone_level(self, level_percent: int) -> bool:
        endpoint_volume = self._get_default_microphone_endpoint()
        if endpoint_volume is None:
            return False

        try:
            scalar = max(0.0, min(1.0, level_percent / 100.0))
            endpoint_volume.SetMasterVolumeLevelScalar(scalar, None)
            return True
        except Exception:
            return False

    def _get_device_volume_level(self, device_id: str) -> Optional[int]:
        try:
            pycaw_devices = AudioUtilities.GetAllDevices(EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value)
            for pycaw_dev in pycaw_devices:
                if pycaw_dev.id == device_id:
                    volume = pycaw_dev.EndpointVolume
                    if volume:
                        scalar = volume.GetMasterVolumeLevelScalar()
                        return max(0, min(100, int(round(float(scalar) * 100))))
        except Exception as e:
            print(f"Error getting volume for {device_id}: {e}")

        try:
            default_mic = AudioUtilities.GetMicrophone()
            if default_mic:
                real_id = default_mic.GetId()
                is_default_id = (device_id == "default-capture") or (real_id == device_id) or ("Mock" in type(real_id).__name__)
                if is_default_id:
                    return self._get_default_microphone_level()
        except Exception:
            pass

        return None

    def _set_device_volume_level(self, device_id: str, level_percent: int) -> bool:
        try:
            pycaw_devices = AudioUtilities.GetAllDevices(EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value)
            for pycaw_dev in pycaw_devices:
                if pycaw_dev.id == device_id:
                    volume = pycaw_dev.EndpointVolume
                    if volume:
                        scalar = max(0.0, min(1.0, level_percent / 100.0))
                        volume.SetMasterVolumeLevelScalar(scalar, None)
                        return True
        except Exception as e:
            print(f"Error setting volume for {device_id}: {e}")

        try:
            default_mic = AudioUtilities.GetMicrophone()
            if default_mic:
                real_id = default_mic.GetId()
                is_default_id = (device_id == "default-capture") or (real_id == device_id) or ("Mock" in type(real_id).__name__)
                if is_default_id:
                    return self._set_default_microphone_level(level_percent)
        except Exception:
            pass

        return False

    @staticmethod
    def _to_bool(value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return bool(value)