# Useful Utilities Collection

A clean, modular desktop utility app built with **Python** and **PySide6 (Qt)**.

The current first feature is a **Keyboard Lock** module for Windows that can temporarily block keyboard input while keeping the mouse active. The project is designed as a modular desktop app so additional utility modules can be added later without rewriting the whole application.

## Features

- Modern desktop UI with PySide6/Qt.
- Modular application structure.
- Keyboard lock module for Windows.
- Mouse remains usable while the keyboard is locked.
- Automatic unlock on normal application exit.
- Ready for future modules such as screen-clean mode, timers, window tools, or other private utilities.

## Project Goals

This repository is meant to be:

- A practical private-use utility app.
- A clean PySide6 desktop starter project.
- A modular foundation for adding more desktop tools over time.
- A cross-platform-friendly structure, even if some modules are platform-specific.

## Current Status

Implemented:

- Application shell
- Sidebar navigation
- Dashboard page
- Keyboard Lock module
- Shared application context
- Shared service layer
- Module-based page registration

Planned:

- Better dashboard live status refresh
- Additional utility modules
- Packaging for Windows
- Optional Linux/macOS-compatible modules where possible

## Tech Stack

- Python
- PySide6 / Qt for Python
- keyboard

## Project Structure

```text
src/
└─ useful_utilities_collection/
   ├─ app.py
   ├─ main.py
   ├─ core/
   │  ├─ app_context.py
   │  ├─ app_state.py
   │  └─ module_registry.py
   ├─ modules/
   │  ├─ dashboard/
   │  └─ keyboard_lock/
   ├─ services/
   │  └─ keyboard_lock_service.py
   └─ ui/
      ├─ main_window.py
      └─ theme.py
```

## Setup

### 1. Create and activate a virtual environment

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

```powershell
$env:PYTHONPATH="src"
python -m useful_utilities_collection.main
```

## Requirements

- Python 3.11+
- Windows for the current keyboard lock functionality

## Notes

The current keyboard lock feature is Windows-focused. The overall application structure is intentionally modular so future utilities can support Linux and macOS with minimal structural changes.
