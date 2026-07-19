import sys
from pathlib import Path

from PySide6.QtCore import QTimer, Qt, QRectF
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPen, QColor, QFont, QBrush

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.ui.main_window import MainWindow
from useful_utilities_collection.ui.theme import APP_STYLE

_INSTANCE_KEY = "UUC_SingleInstance_7f3a2b"


class AnimatedSplashScreen(QSplashScreen):
    def __init__(self, fallback_icon_path: Path, message: str = ""):
        # Create an empty translucent pixmap of size 280x320
        pixmap = QPixmap(280, 320)
        pixmap.fill(Qt.transparent)
        super().__init__(pixmap)

        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.message = message
        self.angle = 0

        # Load and scale the logo
        self.logo_pixmap = QPixmap(str(fallback_icon_path))
        if not self.logo_pixmap.isNull():
            self.logo_pixmap = self.logo_pixmap.scaled(
                140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        # Start timer for spinner animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update)
        self.animation_timer.start(40)  # 25 FPS

    def hideEvent(self, event) -> None:
        self.animation_timer.stop()
        super().hideEvent(event)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1. Draw rounded background card (Background: #161b22, Border: #2d333b)
        card_rect = QRectF(1, 1, 278, 318)
        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#2d333b"), 1.5))
        painter.drawRoundedRect(card_rect, 18, 18)

        # 2. Draw logo (centered at top)
        if not self.logo_pixmap.isNull():
            lx = (280 - 140) // 2
            ly = 35
            painter.drawPixmap(lx, ly, self.logo_pixmap)

        # 3. Draw spinner
        cx = 280 // 2
        cy = 215

        self.angle = (self.angle + 8) % 360
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle)

        pen = QPen()
        pen.setWidth(3)
        pen.setCapStyle(Qt.RoundCap)

        for i in range(8):
            alpha = int(255 * (i + 1) / 8)
            # Vibrant light blue accent color
            pen.setColor(QColor(88, 166, 255, alpha))
            painter.setPen(pen)
            painter.drawLine(0, -9, 0, -5)
            painter.rotate(45)
        painter.restore()

        # 4. Draw loading message
        if self.message:
            painter.setPen(QColor("#e6edf3"))
            font = QFont("Segoe UI", 10)
            font.setBold(True)
            painter.setFont(font)

            text_rect = QRectF(10, cy + 25, 260, 40)
            painter.drawText(text_rect, Qt.AlignHCenter | Qt.AlignTop, self.message)


def _set_windows_app_id() -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes
        app_id = "UsefulUtilitiesCollection"
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

    is_autostart = "--minimized" in sys.argv

    # --- Loading/Splash Screen ---
    splash = None
    if not is_autostart:
        from PySide6.QtCore import QSettings
        from useful_utilities_collection.core.translation import set_language, t

        # Load language settings early
        settings = QSettings("UsefulUtilitiesCollection", "UsefulUtilitiesCollection")
        lang = str(settings.value("general/language", "en"))
        set_language(lang)

        assets_dir = Path(__file__).resolve().parent / "assets"
        fallback_icon_path = assets_dir / "icon.png"
        
        splash = AnimatedSplashScreen(fallback_icon_path, t("app.starting"))
        splash.show()
        app.processEvents()

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

    if not is_autostart:
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
    if is_autostart:
        def show_startup_notification():
            if context.microphone_guard_service._guard_enabled:
                from useful_utilities_collection.core.translation import t
                window.tray_icon.showMessage(
                    t("app.guard_active_startup_title"),
                    t("app.guard_active_startup_body"),
                    QIcon(str(icon_path)),
                    4000,
                )
        QTimer.singleShot(30000, show_startup_notification)

    return app.exec()