import sys
from pathlib import Path

from PySide6.QtCore import QSharedMemory
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.ui.main_window import MainWindow
from useful_utilities_collection.ui.theme import APP_STYLE

_INSTANCE_KEY = "UUC_SingleInstance_7f3a2b"


def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        app_id = "usefulutilitiescollection.desktop.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


def _try_focus_existing() -> bool:
    """Try to signal an existing instance to show itself. Returns True if one was found."""
    socket = QLocalSocket()
    socket.connectToServer(_INSTANCE_KEY)
    if socket.waitForConnected(500):
        socket.write(b"SHOW")
        socket.flush()
        socket.waitForBytesWritten(300)
        socket.disconnectFromServer()
        return True
    return False


def run() -> int:
    _set_windows_app_id()

    # --- Single Instance Check ---
    app = QApplication(sys.argv)
    app.setApplicationName("Useful Utilities Collection")
    app.setStyleSheet(APP_STYLE)

    if _try_focus_existing():
        # Another instance is running — signal it and exit
        return 0

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

    is_autostart = "--minimized" in sys.argv
    if not is_autostart:
        window.show()

    # --- Start local server so other instances can signal us ---
    local_server = QLocalServer()
    QLocalServer.removeServer(_INSTANCE_KEY)  # Remove stale socket if exists
    local_server.listen(_INSTANCE_KEY)

    def on_new_connection():
        client = local_server.nextPendingConnection()
        if client:
            client.waitForReadyRead(300)
            # Any message means: bring window to front
            window.show_and_activate()
            client.disconnectFromServer()

    local_server.newConnection.connect(on_new_connection)

    # Autostart: show tray notification if guard is active
    if is_autostart and context.microphone_guard_service._guard_enabled:
        from useful_utilities_collection.core.translation import t
        window.tray_icon.showMessage(
            t("app.guard_active_startup_title"),
            t("app.guard_active_startup_body"),
            QIcon(str(icon_path)),
            4000,
        )

    return app.exec()