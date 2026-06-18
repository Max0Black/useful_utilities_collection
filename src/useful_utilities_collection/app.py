import sys

from PySide6.QtWidgets import QApplication

from useful_utilities_collection.core.app_context import AppContext
from useful_utilities_collection.ui.main_window import MainWindow
from useful_utilities_collection.ui.theme import APP_STYLE


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Useful Utilities Collection")
    app.setStyleSheet(APP_STYLE)

    context = AppContext()
    window = MainWindow(context)
    window.show()

    return app.exec()