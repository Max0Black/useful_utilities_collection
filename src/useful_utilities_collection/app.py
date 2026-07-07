import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.ui.main_window import MainWindow
from useful_utilities_collection.ui.theme import APP_STYLE

def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return

    try:
        import ctypes
        app_id = "usefulutilitiescollection.desktop.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

def run() -> int:
    _set_windows_app_id()

    app = QApplication(sys.argv)
    app.setApplicationName("Useful Utilities Collection")
    app.setStyleSheet(APP_STYLE)

    assets_dir = Path(__file__).resolve().parent / "assets"
    windows_icon_path = assets_dir / "icon.ico"
    fallback_icon_path = assets_dir / "icon.png"

    icon_path = windows_icon_path if windows_icon_path.exists() else fallback_icon_path
    app_icon = QIcon(str(icon_path))

    app.setWindowIcon(app_icon)
    app.setQuitOnLastWindowClosed(False)

    context = AppContext()
    window = MainWindow(context, app_icon)
    window.setWindowIcon(app_icon)
    if "--minimized" not in sys.argv:
        window.show()

    return app.exec()