import time
from PySide6.QtCore import QObject, QTimer, Signal

from useful_utilities_collection.core.translation import t


class CountdownLockManager(QObject):
    """Manages timed locking sessions with ticker updates and event notifications."""

    tick = Signal(int)  # remaining seconds
    started = Signal(int, str)  # duration seconds, localized duration text
    completed = Signal()
    stopped = Signal()

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)
        self._end_timestamp: float | None = None
        self._current_duration: int = 0

    @property
    def is_active(self) -> bool:
        return self._timer.isActive()

    def start(self, duration_seconds: int) -> None:
        if duration_seconds <= 0:
            return
        self._current_duration = duration_seconds
        self._end_timestamp = time.time() + duration_seconds
        self.controller.lock_both()
        self._timer.start(1000)
        duration_text = self.format_duration(duration_seconds)
        self.started.emit(duration_seconds, duration_text)
        self._on_tick()

    def stop(self) -> None:
        if self._timer.isActive():
            self._timer.stop()
            self._end_timestamp = None
            self.controller.unlock_both()
            self.stopped.emit()

    def _on_tick(self) -> None:
        if self._end_timestamp is None:
            return
        remaining = max(0, int(self._end_timestamp - time.time()))
        if remaining <= 0:
            self._timer.stop()
            self._end_timestamp = None
            self.controller.unlock_both()
            self.completed.emit()
            return
        self.tick.emit(remaining)

    @staticmethod
    def format_clock(seconds: int) -> str:
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            return f"{hours:d}:{minutes:02d}:{sec:02d}"
        return f"{minutes:d}:{sec:02d}"

    @staticmethod
    def format_duration(seconds: int) -> str:
        if seconds >= 3600:
            hours = seconds / 3600
            if seconds % 3600 == 0:
                value = int(hours)
                unit = t("input_lock.countdown_unit_hour") if value == 1 else t("input_lock.countdown_unit_hours")
                return f"{value} {unit}"
            unit = t("input_lock.countdown_unit_hours")
            return f"{hours:.1f} {unit}"
        if seconds >= 60:
            minutes = seconds / 60
            if seconds % 60 == 0:
                value = int(minutes)
                unit = t("input_lock.countdown_unit_minute") if value == 1 else t("input_lock.countdown_unit_minutes")
                return f"{value} {unit}"
            unit = t("input_lock.countdown_unit_minutes")
            return f"{minutes:.1f} {unit}"
        value = seconds
        unit = t("input_lock.countdown_unit_second") if value == 1 else t("input_lock.countdown_unit_seconds")
        return f"{value} {unit}"
