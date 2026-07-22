# 💡 Ideas & Future Plans for UUC (Useful Utilities Collection)

Here is a collection of thoughts and features that we could gradually build into the application. Feel free to add any new ideas whenever inspiration strikes!

---

## 1. Microphone Guard Enhancements

### 1.1 Volume History & Live Graph
- A mini live graph on the dashboard showing how microphone volume levels have changed over the past few minutes.
- Display automatic volume corrections directly with timestamps on the graph so you can easily spot when Guard adjusted your levels.

### 1.2 Microphone Test & Quick Calibration
- A quick audio test built right into Microphone Guard: speak into your mic and see immediate visual level feedback.
- Helps when setting up your device to quickly dial in the perfect target volume.

---

## 2. Input Lock Features

### 2.1 Laptop Touchpad Lock
- In addition to keyboard and mouse locking, add the ability to temporarily block the touchpad.
- Super handy when wiping down your laptop keyboard without accidentally triggering touchpad gestures.

---

## 3. Dashboard & System Overview

### 3.1 System Info Cards
- Neat status cards showing CPU usage, RAM, and battery levels (e.g. via `psutil`).
- Quick check for network connection status (Online / Offline).

### 3.2 Live Volume Sparkline on Dashboard
- A compact live microphone level curve right on the main dashboard page so you can verify at a glance that everything is regulating smoothly.

---

## 4. UI & UX Refinements

### 4.1 Light Mode & System Theme Auto-Detection
- Currently, the application is locked to dark mode. Adding a light theme option and automatic Windows accent/theme detection would be awesome.

### 4.2 Flexible Sidebar Placement
- An option to position the sidebar on the right side for users who prefer that layout.

### 4.3 Enhanced Tray Icon Interactions
- Double-clicking the system tray icon immediately opens the most recently used page (instead of just toggling show/hide).
- Expand the tray right-click context menu with quick toggles for "Guard On/Off" or "Lock Mouse".

### 4.4 Smooth Animations & Polish
- After fixing toast notifications, fine-tune page transition animations and hover micro-interactions to feel silky smooth.

---

## 5. Performance & Power Efficiency

### 5.1 Smart Battery Polling Rate
- When unplugged (running on battery power), automatically loosen the polling interval slightly to conserve laptop battery life.

### 5.2 CPU Usage Throttling
- Automatically throttle background checking frequency if system load spikes, ensuring the app remains ultra-lightweight.

### 5.3 Resilient Audio Driver Fallbacks
- If the default Windows Audio API (`pycaw`) stumbles, gracefully fall back to alternative audio backends instead of throwing errors.

---

## 6. Privacy & Transparency

### 6.1 Local Activity Log
- Simple local stats: How many times did the app adjust volume today? Which microphones were guarded?
- Everything remains 100% stored locally on your machine — zero cloud sync or data transmission.

---

## 7. Settings & Backup

### 7.1 Export & Import Settings
- Easily export your configuration to a file and import it on another PC or after a fresh Windows installation.

### 7.2 Automatic Settings Backup
- Automatic local backups saved to `%APPDATA%` so your settings are never lost in case of a system crash.

### 7.3 Silent Autostart to System Tray
- Option to launch directly minimized to the system tray on Windows startup without opening the main window.

---

## 8. Extras for Power Users & Developers

### 8.1 Plugin System (Future Goal)
- Architect modular extensions so third-party developers can easily plug in custom pages (e.g., Clipboard Manager or Memory Monitor).

### 8.2 Command Line Interface (CLI)
- Handy CLI flags like `uuc --toggle-guard` or `uuc --lock-keyboard` for scripting and automation.

---

## 9. Accessibility (a11y)

### 9.1 Screen Reader Optimization
- Improve `accessibleName` and `accessibleDescription` attributes across all widgets for full NVDA / Windows Narrator support.

### 9.2 High Contrast Mode & Font Scaling
- High-contrast theme preset and customizable font sizes in settings.

### 9.3 Full Keyboard Navigation
- Ensure every single page and control can be effortlessly navigated using only the Tab key.

---

## 10. Languages & Localization (i18n)

### 10.1 Complete Translations
- Fully translate language dropdown entries (e.g., French, Spanish, Japanese) with complete locale files.

### 10.2 Regional Date & Number Formats
- Adapt date and time formatting dynamically based on selected locale/region.
