import keyboard


class KeyboardLockService:
    EMERGENCY_HOTKEY = "shift+alt+m"

    def __init__(self, settings_service=None, on_emergency_unlock=None):
        self._settings_service = settings_service
        self._on_emergency_unlock = on_emergency_unlock
        self._locked = False
        self._hook = None
        self._pressed_scan_codes: set[int] = set()
        self._pressed_names: set[str] = set()
        self._hotkey_combinations: list[tuple[int, ...]] = []
        self._hotkey_names: set[str] = set()
        self._setup_hotkey()

    def _convert_portable_hotkey_to_keyboard(self, portable_hotkey: str) -> str:
        if not portable_hotkey:
            return self.EMERGENCY_HOTKEY

        first_part = portable_hotkey.split(",")[0].strip()

        key_map = {
            "ctrl": "ctrl",
            "alt": "alt",
            "shift": "shift",
            "meta": "win",
            "ins": "insert",
            "del": "delete",
            "pgup": "page up",
            "pgdn": "page down",
            "backspace": "backspace",
            "esc": "esc",
            "enter": "enter",
            "return": "enter",
            "tab": "tab",
            "space": "space",
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right",
        }

        parts = first_part.split("+")
        new_parts = []
        for part in parts:
            p = part.strip().lower()
            if p in key_map:
                new_parts.append(key_map[p])
            else:
                new_parts.append(p)

        return "+".join(new_parts)

    def _setup_hotkey(self) -> None:
        try:
            hotkey_str = self.EMERGENCY_HOTKEY
            if self._settings_service:
                portable_hotkey = self._settings_service.get_mouse_lock_hotkey()
                hotkey_str = self._convert_portable_hotkey_to_keyboard(portable_hotkey)

            parsed = keyboard.parse_hotkey_combinations(hotkey_str)
            if parsed and len(parsed) > 0:
                self._hotkey_combinations = list(parsed[0])
            else:
                self._hotkey_combinations = []

            self._hotkey_names = {p.strip().lower() for p in hotkey_str.split("+")}
        except Exception:
            self._hotkey_combinations = []
            self._hotkey_names = {"shift", "alt", "m"}

    def update_hotkey(self) -> None:
        self._setup_hotkey()

    def lock(self, allowed_keys: set[int] | None = None) -> bool:
        if self._locked:
            return True

        self._pressed_scan_codes.clear()
        self._pressed_names.clear()
        self._setup_hotkey()
        self._hook = keyboard.hook(self._on_key_event, suppress=True)
        self._locked = True
        return True

    def unlock(self) -> bool:
        if not self._locked:
            return True

        if self._hook is not None:
            try:
                keyboard.unhook(self._hook)
            except Exception:
                pass
            self._hook = None

        self._pressed_scan_codes.clear()
        self._pressed_names.clear()
        self._locked = False
        return True

    def is_locked(self) -> bool:
        return self._locked

    def shutdown(self) -> None:
        self.unlock()

    @staticmethod
    def _normalize_key_name(name: str | None) -> str:
        if not name:
            return ""
        n = str(name).lower()
        if n in ("left alt", "right alt", "alt gr"):
            return "alt"
        if n in ("left shift", "right shift"):
            return "shift"
        if n in ("left ctrl", "right ctrl", "control"):
            return "ctrl"
        if n in ("left windows", "right windows", "win"):
            return "win"
        return n

    def _on_key_event(self, event) -> bool:
        """
        Windows keyboard hook callback.
        Return True to allow the event to pass through to other apps.
        Return False to block (suppress) all keys unconditionally,
        while checking for the emergency unlock hotkey.
        """
        if not self._locked:
            return True

        norm_name = self._normalize_key_name(getattr(event, "name", None))
        scan_code = getattr(event, "scan_code", None)
        event_type = getattr(event, "event_type", None)

        if event_type == "down":
            if scan_code is not None:
                self._pressed_scan_codes.add(scan_code)
            if norm_name:
                self._pressed_names.add(norm_name)

            matched = False
            if self._hotkey_combinations:
                matched = any(
                    set(combo).issubset(self._pressed_scan_codes)
                    for combo in self._hotkey_combinations
                )

            if not matched and self._hotkey_names:
                matched = self._hotkey_names.issubset(self._pressed_names)

            if matched:
                if self._on_emergency_unlock:
                    try:
                        self._on_emergency_unlock()
                    except Exception:
                        pass
        elif event_type == "up":
            if scan_code is not None:
                self._pressed_scan_codes.discard(scan_code)
            if norm_name:
                self._pressed_names.discard(norm_name)

        # Block all keys from passing through to other apps
        return False