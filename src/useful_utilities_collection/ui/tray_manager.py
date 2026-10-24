from PySide6.QtCore import QObject
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from useful_utilities_collection.core.translation import t


class TrayManager(QObject):
    """Manages the system tray icon, its context menu and status updates.

    Encapsulates tray actions, status synchronization with services,
    and user interactions (single/double clicks).
    """

    def __init__(self, main_window, app_icon: QIcon):
        super().__init__(main_window)
        self.window = main_window
        self.context = main_window.context
        self.app_icon = app_icon

        self.tray_icon = QSystemTrayIcon(self.app_icon, self.window)
        self.tray_icon.setToolTip(t("app.tray_tooltip"))
        self._setup_menu()
        self.tray_icon.activated.connect(self._on_activated)
        self.tray_icon.show()
        self.update_actions()

    def _setup_menu(self) -> None:
        self.menu = QMenu(self.window)
        self.menu.aboutToShow.connect(self.update_actions)

        # Show action
        self.show_action = QAction(t("app.tray_menu_show"), self.window)
        self.show_action.triggered.connect(self.window.show_and_activate)
        self.menu.addAction(self.show_action)
        self.menu.addSeparator()

        # Microphone Guard
        self.mg_action = QAction(t("app.tray_menu_microphone_guard"), self.window)
        self.mg_action.setCheckable(True)
        self.mg_action.triggered.connect(lambda checked: self._toggle_microphone_guard())
        self.menu.addAction(self.mg_action)

        # Mouse lock
        self.mouse_action = QAction(t("app.tray_menu_lock_mouse"), self.window)
        self.mouse_action.setCheckable(True)
        self.mouse_action.triggered.connect(lambda checked: self._toggle_mouse_lock())
        self.menu.addAction(self.mouse_action)

        # Keyboard lock
        self.keyboard_action = QAction(t("app.tray_menu_lock_keyboard"), self.window)
        self.keyboard_action.setCheckable(True)
        self.keyboard_action.triggered.connect(lambda checked: self._toggle_keyboard_lock())
        self.menu.addAction(self.keyboard_action)

        self.menu.addSeparator()

        # Settings
        self.settings_action = QAction(t("app.tray_menu_settings"), self.window)
        self.settings_action.triggered.connect(self.window.open_settings)
        self.menu.addAction(self.settings_action)

        self.menu.addSeparator()

        # Exit action
        self.exit_action = QAction(t("app.tray_menu_exit"), self.window)
        self.exit_action.triggered.connect(self.window.exit_app)
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)

    def _on_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.Trigger:
            if self.window.isVisible():
                self.window.hide()
            else:
                self.window.show_and_activate()
        elif reason == QSystemTrayIcon.DoubleClick:
            self.window.show_and_activate()

    def update_actions(self) -> None:
        if not hasattr(self, "mg_action"):
            return
        svc = self.context.microphone_guard_service
        self.mg_action.setChecked(svc._guard_enabled)
        self.mouse_action.setChecked(self.context.input_lock_service.mouse_locked())
        self.keyboard_action.setChecked(self.context.input_lock_service.keyboard_locked())

    def retranslate_ui(self) -> None:
        self.tray_icon.setToolTip(t("app.tray_tooltip"))
        self.show_action.setText(t("app.tray_menu_show"))
        self.exit_action.setText(t("app.tray_menu_exit"))
        self.mg_action.setText(t("app.tray_menu_microphone_guard"))
        self.mouse_action.setText(t("app.tray_menu_lock_mouse"))
        self.keyboard_action.setText(t("app.tray_menu_lock_keyboard"))
        self.settings_action.setText(t("app.tray_menu_settings"))

    def show_message(self, title: str, message: str, icon=QSystemTrayIcon.Information, timeout_ms: int = 3000) -> None:
        if self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon, timeout_ms)

    def is_visible(self) -> bool:
        return self.tray_icon.isVisible()

    def hide(self) -> None:
        self.tray_icon.hide()

    def _toggle_microphone_guard(self) -> None:
        svc = self.context.microphone_guard_service
        device_id = svc.get_selected_device_id()
        if device_id:
            current = svc.is_device_guard_enabled(device_id)
            svc.set_guard_enabled(device_id, not current)
            self.context.notify_state_changed()

    def _toggle_mouse_lock(self) -> None:
        from useful_utilities_collection.modules.input_lock.controller import InputLockController
        InputLockController(self.context).toggle_mouse_lock()
        self.context.notify_state_changed()

    def _toggle_keyboard_lock(self) -> None:
        from useful_utilities_collection.modules.input_lock.controller import InputLockController
        InputLockController(self.context).toggle_keyboard_lock()
        self.context.notify_state_changed()
