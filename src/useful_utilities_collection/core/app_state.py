from dataclasses import dataclass


@dataclass
class AppState:
    selected_microphone_id: str | None = None
    microphone_guard_active: bool = False