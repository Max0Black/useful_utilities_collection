from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.modules.dashboard.module import create_module as create_dashboard_module
from useful_utilities_collection.modules.input_lock.module import create_module as create_input_lock_module
from useful_utilities_collection.modules.microphone_guard.module import create_module as create_microphone_guard_module


class MainWindow(QMainWindow):
    def __init__(self, context: AppContext):
        super().__init__()
        self.context = context
        self.modules = [
            create_dashboard_module(),
            create_input_lock_module(),
            create_microphone_guard_module(),
        ]
        self.nav_buttons: list[QPushButton] = []

        self.setWindowTitle("Useful Utilities Collection")
        self.resize(1120, 760)

        root = QWidget()
        root.setObjectName("AppRoot")
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        sidebar = QWidget()
        sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(12)

        title = QLabel("Useful Utilities")
        title.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(title)
        sidebar_layout.addSpacing(12)

        self.stack = QStackedWidget()
        self.stack.setObjectName("ContentStack")

        for index, module in enumerate(self.modules):
            button = QPushButton(module.title)
            button.setCheckable(True)
            button.clicked.connect(lambda checked=False, i=index: self.switch_page(i))
            self.nav_buttons.append(button)
            sidebar_layout.addWidget(button)

            page = module.page_factory(self.context)
            self.stack.addWidget(page)

        sidebar_layout.addStretch()

        layout.addWidget(sidebar, 0)
        layout.addWidget(self.stack, 1)

        self.switch_page(0)

    def switch_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

        for button_index, button in enumerate(self.nav_buttons):
            button.setChecked(button_index == index)

        self.refresh_pages()

    def refresh_pages(self) -> None:
        for index in range(self.stack.count()):
            page = self.stack.widget(index)
            if hasattr(page, "refresh"):
                page.refresh()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.context.input_lock_service.unlock()
        event.accept()