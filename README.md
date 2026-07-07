# 🛠️ Useful Utilities Collection

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A modern, high-performance, and modular desktop utility suite built with **Python** and **PySide6 (Qt)**. Designed with clean software architecture principles, this app provides essential productivity and system utilities in a single, beautiful desktop dashboard.

---

## ✨ Features

### 1. 📊 Dashboard
A centralized control center showing live system status at a glance:
* **Keyboard Lock status** (Locked / Unlocked)
* **Mouse Lock status** (Locked / Unlocked)
* **Microphone Guard status** (Active with current vs. target volume)

### 2. 🔒 Input Lock (Eingabesperre)
Temporarily lock inputs to clean your desk, clean your keyboard, or protect against kids/pets:
* **Keyboard Lock**: Block all keyboard inputs while keeping the mouse functional.
* **Mouse Lock**: Lock mouse movement and clicks.
* **Emergency Unlock**: Unlock the mouse at any time with a customizable global key shortcut (Default: `Shift+Alt+M`).

### 3. 🎙️ Microphone Guard (Mikrofon-Schutz)
Prevent apps (like MS Teams, Zoom, Discord, etc.) from stealthily changing your microphone level:
* **Constant Monitoring**: Checks your Windows default microphone level at custom intervals.
* **Automatic Restoration**: Instantly resets the volume to your desired target (e.g. 80%) if another program alters it.
* **Activity Logs**: Track exactly when and how much volume was corrected.

### 4. ⚙️ Settings (Einstellungen)
Customize behavior, language, and performance:
* **Multi-Language**: Full English & German support.
* **Minimize to Tray**: Minimize the application into the Windows system tray to keep it running invisibly in the background.
* **Launch on Startup**: Run automatically on Windows login.
* **Scan Interval**: Adjust the Microphone Guard responsiveness (from 1.0s up to Eco mode or custom duration).
* **Custom Shortcut**: Change the emergency mouse unlock hotkey.

### 5. 📥 System Tray & Window Management
* **Smart Minimizing**: When minimizing the window, it hides directly to the system tray, freeing up taskbar space.
* **Auto-Safety Unlock**: Minimizing to the tray automatically unlocks your mouse and keyboard if they were locked.
* **Smart Close Behavior**: Clicking the close `[X]` button will prompt a confirmation dialog if the **Microphone Guard** is active to prevent accidental shutdowns.
* **Alt+F4 Exit**: Standard Alt+F4 closes the app immediately without prompts or going to the tray.

---

## 🚀 Installation & Setup

### Requirements
* **OS**: Windows 10 / 11
* **Python**: Version 3.11 or newer

### 1. Clone & Set Up Environment
Open PowerShell and run:
```powershell
# Clone the repository
git clone https://github.com/Max0Black/useful_utilities_collection.git
cd useful_utilities_collection

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run the App
```powershell
# Run with Python
$env:PYTHONPATH="src"
python -m useful_utilities_collection.main
```

---

## 📦 Simple Deployment (Create standalone `.exe`)

We have simplified the compilation process down to a single command. The included build script checks requirements, updates dependencies, and bundles all resources (icons, language packs, com-hooks) into a single standalone executable.

Run the build script:
```powershell
python build.py
```

Once completed, your standalone executable is ready at:
📂 `dist/UsefulUtilitiesCollection.exe`

---

## 📂 Project Structure

```text
useful_utilities_collection/
├─ src/
│  └─ useful_utilities_collection/
│     ├─ core/              # Translation engine, Application context and state
│     ├─ languages/         # de.json and en.json translations
│     ├─ assets/            # App icons (PNG, ICO)
│     ├─ modules/           # Pages & Module definitions (Dashboard, Input Lock, Mic Guard, Settings)
│     ├─ services/          # Services (Keyboard/Mouse hooks, Sound/Volume APIs, Settings)
│     ├─ ui/                # Main window chassis and stylesheets
│     ├─ main.py            # Entry point
│     └─ app.py             # Qt Application launcher
├─ UsefulUtilitiesCollection.spec  # PyInstaller configuration
├─ requirements.txt         # Package dependencies
└─ build.py                 # Automated packaging script
```

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.
