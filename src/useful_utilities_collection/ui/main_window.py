from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QCloseEvent, QGuiApplication, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.dashboard.module import create_module as create_dashboard_module
from useful_utilities_collection.modules.input_lock.module import create_module as create_input_lock_module
from useful_utilities_collection.modules.microphone_guard.module import create_module as create_microphone_guard_module
from useful_utilities_collection.modules.settings.module import create_module as create_settings_module
from useful_utilities_collection.modules.about.module import create_module as create_about_module
from useful_utilities_collection.ui.guard_exit_dialog import GuardExitDialog


class MainWindow(QMainWindow):
    def __init__(self, context: AppContext, app_icon: QIcon):
        super().__init__()
        self.context = context
        self.app_icon = app_icon
        self._allow_exit = False
        self.modules = [
            create_dashboard_module(),
            create_input_lock_module(),
            create_microphone_guard_module(),
            create_settings_module(),
            create_about_module(),
        ]
        self.nav_buttons: list[QPushButton] = []

        self.setWindowTitle("Useful Utilities Collection")
        self.resize(1200, 820)
        # Prevent Qt from auto-resizing when child widgets change their size hints.
        # The user's chosen window size must always be respected.
        self.setMinimumSize(760, 540)
        from PySide6.QtWidgets import QSizePolicy as _SP
        self.setSizePolicy(_SP.Ignored, _SP.Ignored)

        root = QWidget()
        root.setObjectName("AppRoot")
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 20, 16, 20)
        sidebar_layout.setSpacing(8)

        self.sidebar_title = QLabel("UUC")
        self.sidebar_title.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(self.sidebar_title)
        sidebar_layout.addSpacing(16)

        # Guard status indicator in sidebar
        self.guard_status_indicator = QFrame()
        self.guard_status_indicator.setObjectName("GuardStatusIndicator")
        guard_indicator_layout = QHBoxLayout(self.guard_status_indicator)
        guard_indicator_layout.setContentsMargins(10, 8, 10, 8)
        guard_indicator_layout.setSpacing(8)

        self.guard_dot = QLabel("●")
        self.guard_dot.setObjectName("GuardDot")
        self.guard_status_text = QLabel()
        self.guard_status_text.setObjectName("GuardStatusText")

        guard_indicator_layout.addWidget(self.guard_dot)
        guard_indicator_layout.addWidget(self.guard_status_text)
        guard_indicator_layout.addStretch()

        sidebar_layout.addWidget(self.guard_status_indicator)
        sidebar_layout.addSpacing(8)

        self.stack = QStackedWidget()
        self.stack.setObjectName("ContentStack")

        self.pages: list = []
        from PySide6.QtWidgets import QApplication, QScrollArea
        self.about_index = None
        self.settings_index = None

        _ICON_MAP = {
            "dashboard": "📊",
            "input_lock": "🔒",
            "microphone_guard": "🎙",
            "settings": "⚙",
            "about": "ℹ",
        }

        main_buttons = []
        bottom_buttons = []
        for index, module in enumerate(self.modules):
            QApplication.processEvents()
            page = module.page_factory(self.context)
            self.pages.append(page)

            scroll = QScrollArea()
            scroll.setObjectName("PageScroll")
            scroll.setWidgetResizable(True)
            scroll.setWidget(page)
            self.stack.addWidget(scroll)

            icon_text = _ICON_MAP.get(module.module_id, "")
            text = t(f"{module.module_id}.title")
            button = self._create_sidebar_icon_button(icon_text, text)
            button.clicked.connect(lambda checked=False, i=index: self.switch_page(i))
            self.nav_buttons.append(button)

            if module.module_id in ("settings", "about"):
                if module.module_id == "about":
                    self.about_index = index
                elif module.module_id == "settings":
                    self.settings_index = index
                bottom_buttons.append(button)
            else:
                main_buttons.append(button)

        for btn in main_buttons:
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        sidebar_sep = QFrame()
        sidebar_sep.setObjectName("SidebarGroupSeparator")
        sidebar_layout.addWidget(sidebar_sep)

        for idx, btn in enumerate(bottom_buttons):
            sidebar_layout.addWidget(btn)
            if idx < len(bottom_buttons) - 1:
                sep = QFrame()
                sep.setObjectName("SidebarInnerSeparator")
                sidebar_layout.addWidget(sep)

        layout.addWidget(sidebar, 0)
        layout.addWidget(self.stack, 1)

        root_layout.addLayout(layout)

        # Setup System Tray
        self._setup_tray_icon()

        # Connect session shutdown handling
        QGuiApplication.instance().commitDataRequest.connect(self.on_commit_data)

        # Connect notification signal
        self.context.notification_requested.connect(self.show_tray_message)

        # Connect state change to retranslate UI
        self.context.state_changed.connect(self.retranslate_ui)
        self.context.state_changed.connect(self._update_guard_indicator)
        self.retranslate_ui()
        self._update_guard_indicator()

        # Alt+F4 shortcut: show notification then exit
        self._alt_f4_forced = False
        self.alt_f4_shortcut = QShortcut(QKeySequence("Alt+F4"), self)
        self.alt_f4_shortcut.activated.connect(self._alt_f4_activated)

        self.switch_page(0)

    def switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

        for button_index, button in enumerate(self.nav_buttons):
            button.setChecked(button_index == index)

        # Performance fix: Only refresh the currently visible page
        page = self.pages[index] if index < len(self.pages) else None
        if page is not None:
            if hasattr(page, "refresh"):
                page.refresh()
            # Smooth, cheap fade-in for the newly shown page (no window relayout).
            if hasattr(page, "fade_in"):
                page.fade_in()

    def refresh_current_page(self) -> None:
        """Refresh only the currently visible page."""
        index = self.stack.currentIndex()
        page = self.pages[index] if index < len(self.pages) else None
        if page is not None and hasattr(page, "refresh"):
            page.refresh()

    def _update_guard_indicator(self) -> None:
        """Update the guard status dot in the sidebar."""
        guard_active = self.context.microphone_guard_service._guard_enabled
        if guard_active:
            self.guard_dot.setProperty("active", "true")
            self.guard_status_text.setText(t("microphone_guard.status_title_active"))
        else:
            self.guard_dot.setProperty("active", "false")
            self.guard_status_text.setText(t("microphone_guard.status_title_inactive"))
        self.style().unpolish(self.guard_dot)
        self.style().polish(self.guard_dot)

    def _create_sidebar_icon_button(self, icon_text: str, text: str) -> QPushButton:
        button = QPushButton()
        button.setCheckable(True)
        button.setObjectName("SidebarIconButton")

        layout = QHBoxLayout(button)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        icon_label = QLabel(icon_text)
        icon_label.setAlignment(Qt.AlignCenter)
        font = icon_label.font()
        font.setPointSize(16)
        icon_label.setFont(font)
        icon_label.setObjectName("SidebarIconLabel")
        icon_label.setFixedWidth(24)

        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        text_label.setObjectName("SectionTitle")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)
        layout.addStretch()

        button._sidebar_text_label = text_label
        return button

    def _is_german(self) -> bool:
        from useful_utilities_collection.core.translation import get_language
        return get_language() == "de"

    def _setup_tray_icon(self) -> None:
        self.tray_icon = QSystemTrayIcon(self.app_icon, self)
        self.tray_icon.setToolTip("Useful Utilities Collection")

        tray_menu = QMenu(self)

        self.show_action = QAction("Show Window", self)
        self.show_action.triggered.connect(self.show_and_activate)
        tray_menu.addAction(self.show_action)

        tray_menu.addSeparator()

        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def show_and_activate(self) -> None:
        self.show()
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def on_tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_and_activate()
        elif reason == QSystemTrayIcon.DoubleClick:
            self.show_and_activate()

    def exit_app(self) -> None:
        self._allow_exit = True
        self.context.input_lock_service.unlock()
        if hasattr(self, "tray_icon"):
            self.tray_icon.hide()
        QApplication.quit()

    def _alt_f4_activated(self):
        if hasattr(self, "tray_icon") and self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                t("app.alt_f4_terminated_title"),
                t("app.alt_f4_terminated_body"),
                QSystemTrayIcon.Information,
                3000,
            )
        self._allow_exit = True
        self.close()

    def on_commit_data(self, manager) -> None:
        self._allow_exit = True

    def show_tray_message(self, title: str, message: str) -> None:
        if self.isHidden() or self.isMinimized():
            if hasattr(self, "tray_icon") and self.tray_icon.isVisible():
                self.tray_icon.showMessage(title, message, QSystemTrayIcon.Information, 3000)

    def retranslate_ui(self) -> None:
        self.setWindowTitle(t("app.title"))
        if hasattr(self, "sidebar_title"):
            self.sidebar_title.setText(t("app.sidebar_title"))
        if hasattr(self, "tray_icon"):
            self.tray_icon.setToolTip(t("app.tray_tooltip"))
            if hasattr(self, "show_action"):
                self.show_action.setText(t("app.tray_menu_show"))
            if hasattr(self, "exit_action"):
                self.exit_action.setText(t("app.tray_menu_exit"))

        for index, module in enumerate(self.modules):
            if index < len(self.nav_buttons):
                btn = self.nav_buttons[index]
                label = getattr(btn, "_sidebar_text_label", None)
                if label is not None:
                    label.setText(t(f"{module.module_id}.title"))
                else:
                    btn.setText(t(f"{module.module_id}.title"))

        self._update_guard_indicator()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._allow_exit:
            self.context.input_lock_service.unlock()
            if hasattr(self, "tray_icon"):
                self.tray_icon.hide()
            event.accept()
            return

        close_to_tray = self.context.settings_service.get_close_to_tray()
        guard_active = self.context.microphone_guard_service._guard_enabled

        if guard_active:
            dlg = GuardExitDialog(self)
            if dlg.exec() == QDialog.Accepted:
                self.exit_app()
                event.accept()
            else:
                event.ignore()
        else:
            if close_to_tray:
                event.ignore()
                self.hide()
                if hasattr(self, "tray_icon") and self.tray_icon.isVisible():
                    if self.context.settings_service.get_notify_on_minimize():
                        self.tray_icon.showMessage(
                            t("app.tray_message_title"),
                            t("app.tray_message_body"),
                            QSystemTrayIcon.Information,
                            3000
                        )
            else:
                self.exit_app()
                event.accept()

    def changeEvent(self, event: QEvent) -> None:
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                if self.context.settings_service.get_close_to_tray():
                    self.hide()

                    if self.context.input_lock_service.keyboard_locked() or self.context.input_lock_service.mouse_locked():
                        self.context.input_lock_service.unlock()

                    if hasattr(self, "tray_icon") and self.tray_icon.isVisible():
                        if self.context.settings_service.get_notify_on_minimize():
                            self.tray_icon.showMessage(
                                t("app.tray_message_title"),
                                t("app.tray_message_body"),
                                QSystemTrayIcon.Information,
                                3000
                            )
        super().changeEvent(event)