from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QCloseEvent, QGuiApplication, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.core.translation import t
from useful_utilities_collection.modules.about.module import create_module as create_about_module
from useful_utilities_collection.modules.dashboard.module import create_module as create_dashboard_module
from useful_utilities_collection.modules.input_lock.module import create_module as create_input_lock_module
from useful_utilities_collection.modules.microphone_guard.module import create_module as create_microphone_guard_module
from useful_utilities_collection.modules.settings.module import create_module as create_settings_module
from useful_utilities_collection.ui.guard_exit_dialog import GuardExitDialog
from useful_utilities_collection.ui.tray_manager import TrayManager


class MainWindow(QMainWindow):
    _ICON_MAP = {
        "dashboard": "📊",
        "input_lock": "🔒",
        "microphone_guard": "🎙",
        "settings": "⚙",
        "about": "ℹ",
    }

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
        self.pages: list[QWidget] = []
        self.about_index = None
        self.settings_index = None

        self.setWindowTitle("Useful Utilities Collection")
        self.resize(1200, 820)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self._build_ui()
        self._setup_events()

    # ── UI Construction ────────────────────────────────────────────────
    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(0)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        sidebar = self._build_sidebar()
        self.stack = QStackedWidget()
        self.stack.setObjectName("ContentStack")

        self._build_pages(sidebar.layout())

        layout.addWidget(sidebar, 0)
        layout.addWidget(self.stack, 1)
        root_layout.addLayout(layout)

    def _build_sidebar(self) -> QWidget:
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
        return sidebar

    def _build_pages(self, sidebar_layout: QVBoxLayout) -> None:
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

            icon_text = self._ICON_MAP.get(module.module_id, "")
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

    # ── Event Setup & Wiring ──────────────────────────────────────────
    def _setup_events(self) -> None:
        self.tray_manager = TrayManager(self, self.app_icon)
        self.tray_icon = self.tray_manager.tray_icon

        self.context.state_changed.connect(self.tray_manager.update_actions)
        self.context.input_lock_service.state.changed.connect(self.tray_manager.update_actions)
        self.context.state_changed.connect(self.retranslate_ui)
        self.context.state_changed.connect(self._update_guard_indicator)
        self.context.notification_requested.connect(self.show_tray_message)

        QGuiApplication.instance().commitDataRequest.connect(self.on_commit_data)

        self._alt_f4_shortcut = QShortcut(QKeySequence("Alt+F4"), self)
        self._alt_f4_shortcut.activated.connect(self._alt_f4_activated)

        self.retranslate_ui()
        self._update_guard_indicator()
        self.switch_page(0)

    # ── Navigation & Actions ──────────────────────────────────────────
    def switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        for button_index, button in enumerate(self.nav_buttons):
            button.setChecked(button_index == index)

        page = self.pages[index] if index < len(self.pages) else None
        if page is not None:
            if hasattr(page, "refresh"):
                page.refresh()
            if hasattr(page, "fade_in"):
                page.fade_in()

    def refresh_current_page(self) -> None:
        index = self.stack.currentIndex()
        page = self.pages[index] if index < len(self.pages) else None
        if page is not None and hasattr(page, "refresh"):
            page.refresh()

    def open_settings(self) -> None:
        if self.settings_index is not None:
            self.switch_page(self.settings_index)
        self.show_and_activate()

    def show_and_activate(self) -> None:
        self.show()
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def exit_app(self) -> None:
        self._allow_exit = True
        self.context.input_lock_service.unlock()
        self.tray_manager.hide()
        QApplication.quit()

    def _alt_f4_activated(self) -> None:
        if self.tray_manager.is_visible():
            self.tray_manager.show_message(
                t("app.alt_f4_terminated_title"),
                t("app.alt_f4_terminated_body"),
            )
        self._allow_exit = True
        self.close()

    def on_commit_data(self, manager) -> None:
        self._allow_exit = True

    def show_tray_message(self, title: str, message: str) -> None:
        if self.isHidden() or self.isMinimized():
            self.tray_manager.show_message(title, message)

    def _update_guard_indicator(self) -> None:
        guard_active = self.context.microphone_guard_service._guard_enabled
        if guard_active:
            self.guard_dot.setProperty("active", "true")
            self.guard_status_text.setText(t("microphone_guard.status_title_active"))
        else:
            self.guard_dot.setProperty("active", "false")
            self.guard_status_text.setText(t("microphone_guard.status_title_inactive"))
        self.style().unpolish(self.guard_dot)
        self.style().polish(self.guard_dot)

    def retranslate_ui(self) -> None:
        self.setWindowTitle(t("app.title"))
        if hasattr(self, "sidebar_title"):
            self.sidebar_title.setText(t("app.sidebar_title"))
        if hasattr(self, "tray_manager"):
            self.tray_manager.retranslate_ui()

        for index, module in enumerate(self.modules):
            if index < len(self.nav_buttons):
                btn = self.nav_buttons[index]
                label = getattr(btn, "_sidebar_text_label", None)
                if label is not None:
                    label.setText(t(f"{module.module_id}.title"))
                else:
                    btn.setText(t(f"{module.module_id}.title"))

        self._update_guard_indicator()

    # ── Window Lifecycle Events ───────────────────────────────────────
    def closeEvent(self, event: QCloseEvent) -> None:
        if self._allow_exit:
            self.context.input_lock_service.unlock()
            self.tray_manager.hide()
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
                if self.tray_manager.is_visible() and self.context.settings_service.get_notify_on_minimize():
                    self.tray_manager.show_message(
                        t("app.tray_message_title"),
                        t("app.tray_message_body"),
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

                    if self.tray_manager.is_visible() and self.context.settings_service.get_notify_on_minimize():
                        self.tray_manager.show_message(
                            t("app.tray_message_title"),
                            t("app.tray_message_body"),
                        )
        super().changeEvent(event)
