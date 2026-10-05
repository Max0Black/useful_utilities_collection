# Startup & System Tray

## Windows Autostart

To launch UUC automatically on Windows login:

1. Open the **Settings** page inside UUC.
2. Toggle **Launch on Startup** to ON.

UUC registers a run-on-login entry in the Windows registry
(`HKCU\Software\Microsoft\Windows\CurrentVersion\Run`) and also creates a shortcut in the
Windows Startup folder as a fallback.

When launched via autostart, UUC starts silently — no window appears. The tray icon is
immediately visible in the system notification area.

## Start Minimized

If you want UUC to always start in the tray (even when launched manually):

1. Open the **Settings** page.
2. Toggle **Start minimized** to ON.

From this point on, launching UUC will skip the splash screen and go straight to the tray.
To open the main window, left-click or right-click the tray icon and choose **Show Window**.

## Tray Icon & Context Menu

Right-click the UUC tray icon to access quick actions:

| Menu Item | Action |
|---|---|
| **Show Window** | Open (or bring to front) the main UUC window |
| **Microphone Guard** ✓ | Toggle the Mic Guard on/off (check mark = active) |
| **Lock Mouse** ✓ | Toggle mouse lock on/off |
| **Lock Keyboard** ✓ | Toggle keyboard lock on/off |
| **Settings** | Jump directly to the Settings page |
| **Exit** | Quit UUC completely |

The check mark next to Microphone Guard, Lock Mouse, and Lock Keyboard reflects the current
live state — it updates whenever the state changes through any part of the app.

## Tips

- **Autostart + Start Minimized**: Enable both for a fully silent background launch on every login.
- **Emergency mouse unlock**: The hotkey `Shift+Alt+M` (or your custom shortcut) always unlocks the mouse,
  even without opening the main window.
