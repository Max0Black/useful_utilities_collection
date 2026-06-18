from dataclasses import dataclass


@dataclass
class AppState:
    keyboard_locked: bool = False
    keyboard_mode: str = "Unlocked"
    selected_microphone_id: str | None = None
    microphone_guard_active: bool = False