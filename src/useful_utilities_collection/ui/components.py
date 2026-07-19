from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtCore import QTimer, QEvent, Qt

class ToastLabel(QLabel):
    """
    A self-contained animated/auto-hiding toast notification label that
    repositions itself automatically to the top-right of its parent window
    whenever the parent is resized.
    """
    def __init__(self, parent):
        super().__init__("", parent)
        self.setObjectName("ToastMessage")
        self.setWordWrap(True)
        self.hide()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # Install event filter to automatically reposition on parent resize
        if parent:
            parent.installEventFilter(self)

    def show_message(self, message: str, duration_ms: int = 2200) -> None:
        self.setText(message)
        self.adjustSize()
        self.position_toast()
        self.show()
        self.raise_()
        self.timer.start(duration_ms)

    def position_toast(self) -> None:
        parent = self.parentWidget()
        if not parent:
            return
        margin = 20
        # Position at the top right of the parent with safety margins
        x = max(margin, parent.width() - self.width() - margin)
        y = margin
        self.move(x, y)

    def eventFilter(self, watched, event) -> bool:
        if watched == self.parentWidget() and event.type() == QEvent.Resize:
            self.position_toast()
        return super().eventFilter(watched, event)


class BasePage(QWidget):
    """
    Common base class for all application pages.
    Provides helper methods like show_toast and repolish to avoid duplication.
    """
    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.context = context
        self.toast = None

    def show_toast(self, message: str, duration_ms: int = 2200) -> None:
        if self.toast is None:
            self.toast = ToastLabel(self)
        self.toast.show_message(message, duration_ms)

    def repolish(self, *widgets) -> None:
        """Force Qt to reapply stylesheet rules to widgets after property changes."""
        for widget in widgets:
            self.style().unpolish(widget)
            self.style().polish(widget)
            widget.update()

