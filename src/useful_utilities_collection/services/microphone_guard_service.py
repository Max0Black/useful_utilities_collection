from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sounddevice as sd
from PySide6.QtCore import QSettings
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


@dataclass
class MicrophoneDevice:
    device_id: str
    display_name: str
    current_level: int = 0
    target_level: int = 80
    guard_enabled: bool = False
    auto_restore: bool = True
    is_default: bool = True

@dataclass
class GuardRestoreResult:
    restored: bool
    previous_level: int | None = None
    current_level: int | None = None
    target_level: int | None = None


class MicrophoneGuardService:
    def __init__(self):
        self._settings = QSettings(
            "UsefulUtilitiesCollection",
            "UsefulUtilitiesCollection",
        )
        self._selected_device_id: Optional[str] = "default-capture"
        self._target_level: int = int(
            self._settings.value("microphone_guard/target_level", 80)
        )
        self._guard_enabled: bool = self._to_bool(
            self._settings.value("microphone_guard/guard_enabled", False)
        )
        self._auto_restore: bool = self._to_bool(
            self._settings.value("microphone_guard/auto_restore", True)
        )
        self._last_correction_text: str = "Never"
        self._cached_device: Optional[MicrophoneDevice] = None

    def list_devices(self) -> list[MicrophoneDevice]:
        device = self._build_default_device()
        self._cached_device = device
        return [device] if device else []

    def refresh_devices(self) -> list[MicrophoneDevice]:
        return self.list_devices()

    def refresh_selected_device_state(self) -> Optional[MicrophoneDevice]:
        device = self._build_default_device()
        self._cached_device = device
        return device

    def get_selected_device_id(self) -> Optional[str]:
        return self._selected_device_id

    def set_selected_device_id(self, device_id: str) -> None:
        self._selected_device_id = device_id

    def get_device(self, device_id: str | None) -> Optional[MicrophoneDevice]:
        if not device_id:
            return None
        if self._cached_device and self._cached_device.device_id == device_id:
            return self._cached_device
        return self._build_default_device()

    def set_target_level(self, device_id: str, level: int) -> None:
        self._target_level = max(0, min(100, level))
        self._save_settings()
        if self._cached_device:
            self._cached_device.target_level = self._target_level

    def set_guard_enabled(self, device_id: str, enabled: bool) -> None:
        self._guard_enabled = enabled
        self._save_settings()
        if self._cached_device:
            self._cached_device.guard_enabled = enabled

    def set_auto_restore(self, device_id: str, enabled: bool) -> None:
        self._auto_restore = enabled
        self._save_settings()
        if self._cached_device:
            self._cached_device.auto_restore = enabled

    def set_current_level(self, device_id: str, level: int) -> bool:
        changed = self._set_default_microphone_level(max(0, min(100, level)))
        if changed:
            self.refresh_selected_device_state()
        return changed

    def enforce_guard(self, device_id: str) -> GuardRestoreResult:
        device = self.refresh_selected_device_state()
        if device is None:
            return GuardRestoreResult(restored=False)

        if not self._guard_enabled or not self._auto_restore:
            return GuardRestoreResult(
                restored=False,
                previous_level=device.current_level,
                current_level=device.current_level,
                target_level=device.target_level,
            )

        previous_level = int(device.current_level)
        target_level = int(self._target_level)

        if previous_level != target_level:
            changed = self._set_default_microphone_level(target_level)
            if changed:
                self._last_correction_text = datetime.now().strftime("%H:%M:%S")
                updated = self.refresh_selected_device_state()
                current_level = updated.current_level if updated is not None else target_level
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
        return self.enforce_guard("default-capture")

    def get_last_correction_text(self) -> str:
        return self._last_correction_text

    def _build_default_device(self) -> Optional[MicrophoneDevice]:
        display_name = self._get_default_input_name()
        current_level = self._get_default_microphone_level()

        if current_level is None:
            return None

        return MicrophoneDevice(
            device_id="default-capture",
            display_name=display_name or "Default microphone",
            current_level=current_level,
            target_level=self._target_level,
            guard_enabled=self._guard_enabled,
            auto_restore=self._auto_restore,
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

    def _save_settings(self) -> None:
        self._settings.setValue("microphone_guard/target_level", self._target_level)
        self._settings.setValue("microphone_guard/guard_enabled", self._guard_enabled)
        self._settings.setValue("microphone_guard/auto_restore", self._auto_restore)
        self._settings.sync()

    @staticmethod
    def _to_bool(value) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return bool(value)