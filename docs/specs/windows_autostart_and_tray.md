# Spec: Windows Autostart & Tray Menu

## Purpose
Provide a reliable Windows autostart mechanism and a polished system-tray context menu.

## AutostartService
- File: `src/useful_utilities_collection/services/autostart_service.py`
- Class: `AutostartService` with `enable() -> bool`, `disable() -> bool`, `is_enabled() -> bool`
- Registry key: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`, value name `UsefulUtilitiesCollection`
- Dev mode (`python.exe` in `sys.executable`): registers `"<python>" "<main.py>" --minimized`
- Frozen mode: registers `"<exe>" --minimized`
- Also creates/removes `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\UsefulUtilitiesCollection.lnk`
- `SettingsService` delegates `is_startup_enabled()` / `set_startup_enabled()` to this service

## Start-Minimized Setting
- QSettings key: `general/start_minimized` (bool, default False)
- API: `SettingsService.is_start_minimized() -> bool`, `set_start_minimized(bool) -> None`
- At startup: `is_minimized = ("--minimized" in sys.argv) or settings_service.is_start_minimized()`
- When `is_minimized`: skip splash screen, do not call `window.show()`, tray icon visible

## Tray Menu
Menu order (top to bottom):
1. **Show Window** — `show_and_activate()`
2. --- separator ---
3. **Microphone Guard** (checkable) — reflects `microphone_guard_service._guard_enabled`; toggle via `set_guard_enabled(device_id, not current)`
4. **Lock Mouse** (checkable) — reflects `input_lock_service.mouse_locked()`; toggle via `InputLockController.toggle_mouse_lock()`
5. **Lock Keyboard** (checkable) — reflects `input_lock_service.keyboard_locked()`; toggle via `InputLockController.toggle_keyboard_lock()`
6. --- separator ---
7. **Settings** — `open_settings()` → `switch_page(settings_index)` + `show_and_activate()`
8. --- separator ---
9. **Exit** — `exit_app()`

State updates: `_update_tray_actions()` called on tray setup and on `context.state_changed`.

## Translation Keys Added
Both `en.json` and `de.json` under `app`:
- `tray_menu_microphone_guard`
- `tray_menu_lock_mouse`
- `tray_menu_lock_keyboard`
- `tray_menu_settings`
