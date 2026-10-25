import math
import sys
from pathlib import Path

from PySide6.QtCore import QTimer, Qt, QRectF
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import QApplication, QSplashScreen, QSystemTrayIcon
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QFont, QBrush

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.ui.main_window import MainWindow
from useful_utilities_collection.ui.theme import APP_STYLE

_INSTANCE_KEY = "UUC_SingleInstance_7f3a2b"


def _to_bool_setting(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "on"}
    return bool(value)


class AnimatedSplashScreen(QSplashScreen):
    def __init__(self, fallback_icon_path: Path, message: str = ""):
        pixmap = QPixmap(280, 320)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap)

        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.message = message
        self.frame = 0

        # Load and scale the logo
        self.logo_pixmap = QPixmap(str(fallback_icon_path))
        if not self.logo_pixmap.isNull():
            self.logo_pixmap = self.logo_pixmap.scaled(
                140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        # Pre-render static background card and logo into base pixmap
        self.base_pixmap = QPixmap(280, 320)
        self.base_pixmap.fill(Qt.transparent)
        p = QPainter(self.base_pixmap)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QBrush(QColor("#161b22")))
        p.setPen(QPen(QColor("#2d333b"), 1.5))
        p.drawRoundedRect(QRectF(1, 1, 278, 318), 18, 18)
        if not self.logo_pixmap.isNull():
            lx = (280 - 140) // 2
            ly = 35
            p.drawPixmap(lx, ly, self.logo_pixmap)
        if self.message:
            p.setPen(QColor("#e6edf3"))
            font = QFont("Segoe UI", 10)
            font.setBold(True)
            p.setFont(font)
            text_rect = QRectF(10, 240, 260, 40)
            p.drawText(text_rect, Qt.AlignHCenter | Qt.AlignTop, self.message)
        p.end()

        # Start light timer for the three-dot loading animation (refresh only dot rect)
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self._animate_tick)
        self.animation_timer.start(120)

    def _animate_tick(self) -> None:
        self.frame = (self.frame + 1) % 60
        # Only repaint the small dots area (cx=140, cy=215, height=30)
        self.update(80, 200, 120, 35)

    def hideEvent(self, event) -> None:
        self.animation_timer.stop()
        super().hideEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw pre-rendered static base
        painter.drawPixmap(0, 0, self.base_pixmap)

        # Draw smooth pulsing dots
        cx = 280 // 2
        cy = 215
        dot_radius = 4
        spacing = 20

        for i in range(3):
            phase = (self.frame / 10.0 - i * 0.8) % (2 * math.pi)
            lift = -math.sin(phase) * 5 if math.sin(phase) > 0 else 0
            alpha = int(140 + 115 * max(0.0, math.sin(phase)))

            dot_color = QColor(88, 166, 255, alpha)
            painter.setBrush(QBrush(dot_color))
            painter.setPen(Qt.NoPen)
            dx = cx + (i - 1) * spacing
            painter.drawEllipse(QRectF(dx - dot_radius, cy + lift - dot_radius,
                                       dot_radius * 2, dot_radius * 2))


WINDOWS_APP_ID = "UsefulUtilitiesCollection.DesktopApp.1.0"


def _register_toast_compat_id() -> None:
    if sys.platform != "win32":
        return
    try:
        import winreg
        key_path = f"Software\\Classes\\AppUserModelId\\{WINDOWS_APP_ID}"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "Useful Utilities Collection")
            winreg.SetValueEx(key, "ShowInSettings", 0, winreg.REG_DWORD, 1)
    except Exception:
        pass


def _resolve_asset(name: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", str(Path(__file__).resolve().parent)))
    candidate = Path(base) / "assets" / name
    if candidate.exists():
        return candidate
    # Fallback to the source tree location (running as a script).
    return Path(__file__).resolve().parent / "assets" / name


def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOWS_APP_ID)
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
    # --- Single Instance Check ---
    app = QApplication(sys.argv)
    app.setApplicationName("Useful Utilities Collection")
    app.setStyleSheet(APP_STYLE)

    _set_windows_app_id()
    _register_toast_compat_id()

    if _try_focus_existing():
        # Another instance is running — signal it and exit
        return 0

    from PySide6.QtCore import QSettings

    # --- Determine startup mode ---
    _qs = QSettings("UsefulUtilitiesCollection", "UsefulUtilitiesCollection")
    _persisted_minimized = _to_bool_setting(_qs.value("general/start_minimized", False))
    is_minimized = ("--minimized" in sys.argv) or _persisted_minimized

    # --- Loading/Splash Screen (skip if minimized) ---
    splash = None
    if not is_minimized:
        from useful_utilities_collection.core.translation import set_language, t

        # Load language settings early
        settings = QSettings("UsefulUtilitiesCollection", "UsefulUtilitiesCollection")
        lang = str(settings.value("general/language", "en"))
        set_language(lang)

        fallback_icon_path = _resolve_asset("icon.png")

        splash = AnimatedSplashScreen(fallback_icon_path, t("app.starting"))
        splash.show()
        app.processEvents()

    windows_icon_path = _resolve_asset("icon.ico")
    fallback_icon_path = _resolve_asset("icon.png")

    icon_path = windows_icon_path if windows_icon_path.exists() else fallback_icon_path
    app_icon = QIcon(str(icon_path))

    app.setWindowIcon(app_icon)
    app.setQuitOnLastWindowClosed(False)

    context = AppContext()
    window = MainWindow(context, app_icon)
    window.setWindowIcon(app_icon)

    if not is_minimized:
        window.show()
        if splash:
            splash.finish(window)

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

    # Autostart: show tray notification 30 seconds after starting if guard is active
    if is_minimized:
        def show_startup_notification():
            if context.microphone_guard_service._guard_enabled:
                from useful_utilities_collection.core.translation import t
                window.tray_icon.showMessage(
                    t("app.guard_active_startup_title"),
                    t("app.guard_active_startup_body"),
                    QSystemTrayIcon.Information,
                    4000,
                )
        QTimer.singleShot(30000, show_startup_notification)

    exit_code = 0
    try:
        exit_code = app.exec()
    finally:
        context.input_lock_service.shutdown()

    return exit_code