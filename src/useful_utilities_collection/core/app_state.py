from dataclasses import dataclass

@dataclass
class AppState:
    keyboard_locked: bool = False
    keyboard_mode: str = "Unlocked"