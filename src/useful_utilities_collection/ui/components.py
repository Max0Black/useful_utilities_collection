from PySide6.QtWidgets import QLabel, QWidget, QGraphicsOpacityEffect
from PySide6.QtCore import QTimer, QEvent, Qt, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter


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

        # Opacity effect drives a cheap fade that never triggers a relayout.
        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity)

        self._fade = QPropertyAnimation(self._opacity, b"opacity", self)
        self._fade.setDuration(220)
        self._fade.setEasingCurve(QEasingCurve.OutCubic)
        self._fade.finished.connect(self._on_fade_finished)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._start_hide)

        # Install event filter to automatically reposition on parent resize
        if parent:
            parent.installEventFilter(self)

    def show_message(self, message: str, duration_ms: int = 2200) -> None:
        self.setText(message)
        self.adjustSize()
        self.position_toast()
        self.show()
        self.raise_()
        self._fade.stop()
        self._fade.setDirection(QPropertyAnimation.Forward)
        self._fade.setStartValue(self._opacity.opacity())
        self._fade.setEndValue(1.0)
        self._fade.start()
        self.timer.start(duration_ms)

    def _start_hide(self) -> None:
        self._fade.stop()
        self._fade.setDirection(QPropertyAnimation.Backward)
        self._fade.setStartValue(self._opacity.opacity())
        self._fade.setEndValue(0.0)
        self._fade.start()

    def _on_fade_finished(self) -> None:
        if self._opacity.opacity() == 0.0:
            self.hide()

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

    def fade_in(self, duration_ms: int = 180) -> None:
        """Smoothly fade the page in after a page switch (no relayout/repaint storm)."""
        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(0.0)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(duration_ms)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.finished.connect(lambda: self.setGraphicsEffect(None))
        anim.start()

