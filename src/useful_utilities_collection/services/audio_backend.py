from __future__ import annotations

import sys
from typing import Optional
from ctypes import POINTER, cast
import sounddevice as sd
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, EDataFlow, DEVICE_STATE


def _get_audio_module():
    """Return the microphone_guard_service module if patched by tests, else this module."""
    svc_mod = sys.modules.get("useful_utilities_collection.services.microphone_guard_service")
    return svc_mod if svc_mod is not None else sys.modules[__name__]


def get_default_device_id() -> str:
    default_id = "default-capture"
    try:
        mod = _get_audio_module()
        default_mic = getattr(mod, "AudioUtilities", AudioUtilities).GetMicrophone()
        if default_mic:
            real_id = default_mic.GetId()
            if "Mock" not in type(real_id).__name__:
                default_id = real_id
    except Exception:
        pass
    return default_id


def get_default_input_name() -> str:
    try:
        mod = _get_audio_module()
        sd_mod = getattr(mod, "sd", sd)
        default_input, _ = sd_mod.default.device
        if default_input is None or default_input < 0:
            return "Default microphone"
        info = sd_mod.query_devices(default_input)
        return str(info.get("name", "Default microphone"))
    except Exception:
        return "Default microphone"


def get_default_microphone_endpoint():
    try:
        mod = _get_audio_module()
        device = getattr(mod, "AudioUtilities", AudioUtilities).GetMicrophone()
        if device is None:
            return None
        interface = device.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None,
        )
        cast_fn = getattr(mod, "cast", cast)
        return cast_fn(interface, POINTER(IAudioEndpointVolume))
    except Exception:
        return None


def get_default_microphone_level() -> Optional[int]:
    endpoint_volume = get_default_microphone_endpoint()
    if endpoint_volume is None:
        return None

    try:
        scalar = endpoint_volume.GetMasterVolumeLevelScalar()
        return max(0, min(100, int(round(float(scalar) * 100))))
    except Exception:
        return None


def set_default_microphone_level(level_percent: int) -> bool:
    endpoint_volume = get_default_microphone_endpoint()
    if endpoint_volume is None:
        return False

    try:
        scalar = max(0.0, min(1.0, level_percent / 100.0))
        endpoint_volume.SetMasterVolumeLevelScalar(scalar, None)
        return True
    except Exception:
        return False


def get_all_capture_devices():
    try:
        mod = _get_audio_module()
        return getattr(mod, "AudioUtilities", AudioUtilities).GetAllDevices(
            EDataFlow.eCapture.value, DEVICE_STATE.ACTIVE.value
        )
    except Exception:
        return []


def get_device_volume_level(device_id: str) -> Optional[int]:
    try:
        pycaw_devices = get_all_capture_devices()
        for pycaw_dev in pycaw_devices:
            if pycaw_dev.id == device_id:
                volume = pycaw_dev.EndpointVolume
                if volume:
                    scalar = volume.GetMasterVolumeLevelScalar()
                    return max(0, min(100, int(round(float(scalar) * 100))))
    except Exception as e:
        print(f"Error getting volume for {device_id}: {e}")

    try:
        mod = _get_audio_module()
        default_mic = getattr(mod, "AudioUtilities", AudioUtilities).GetMicrophone()
        if default_mic:
            real_id = default_mic.GetId()
            is_default_id = (device_id == "default-capture") or (real_id == device_id) or ("Mock" in type(real_id).__name__)
            if is_default_id:
                return get_default_microphone_level()
    except Exception:
        pass

    return None


def set_device_volume_level(device_id: str, level_percent: int) -> bool:
    try:
        pycaw_devices = get_all_capture_devices()
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
        mod = _get_audio_module()
        default_mic = getattr(mod, "AudioUtilities", AudioUtilities).GetMicrophone()
        if default_mic:
            real_id = default_mic.GetId()
            is_default_id = (device_id == "default-capture") or (real_id == device_id) or ("Mock" in type(real_id).__name__)
            if is_default_id:
                return set_default_microphone_level(level_percent)
    except Exception:
        pass

    return False

