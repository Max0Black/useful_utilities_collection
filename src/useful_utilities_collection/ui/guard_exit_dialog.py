from PySide6.QtCore import Qt
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from useful_utilities_collection.core.translation import t
from useful_utilities_collection.ui.theme import COLOR_PALETTE

COLOR_SUCCESS = COLOR_PALETTE["COLOR_SUCCESS"]
COLOR_DANGER = COLOR_PALETTE["COLOR_DANGER"]


class GuardExitDialog(QDialog):
    """Themed exit confirmation dialog shown when the guard is active."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setModal(True)
        self.setObjectName("GuardExitDialog")

        self._setup_ui()

    def _setup_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(18)

        self.title_label = QLabel()
        self.title_label.setObjectName("PageTitle")
        self.title_label.setText(t("app.confirm_exit_title"))

        self.body_label = QLabel()
        self.body_label.setObjectName("MutedText")
        self.body_label.setWordWrap(True)
        self.body_label.setText(t("app.confirm_exit_body"))

        buttons = QHBoxLayout()
        buttons.setSpacing(12)

        self.cancel_button = QPushButton()
        self.cancel_button.setObjectName("ExitCancelButton")
        self.cancel_button.clicked.connect(self.reject)

        self.quit_button = QPushButton()
        self.quit_button.setObjectName("ExitQuitButton")
        self.quit_button.clicked.connect(self.accept)

        buttons.addWidget(self.cancel_button)
        buttons.addWidget(self.quit_button)


        root.addWidget(self.title_label)
        root.addWidget(self.body_label)
        root.addLayout(buttons)

        self._apply_texts()
        self._equalize_button_widths()

    def _apply_texts(self) -> None:
        self.cancel_button.setText(t("app.confirm_exit_cancel"))
        self.quit_button.setText(t("app.confirm_exit_quit"))

    def _equalize_button_widths(self) -> None:
        """Ensure both buttons have the same width (based on the wider size hint)."""
        self.cancel_button.adjustSize()
        self.quit_button.adjustSize()
        width = max(self.cancel_button.sizeHint().width(),
                    self.quit_button.sizeHint().width())

        width += 20
        self.cancel_button.setFixedWidth(width)
        self.quit_button.setFixedWidth(width)
        
        self.cancel_button.setStyleSheet(
            f"QPushButton {{ background-color: {COLOR_SUCCESS}; color: white; border: none; border-radius: 8px; padding: 6px 12px; }} "
            f"QPushButton:hover {{ background-color: {self._lighten_color(COLOR_SUCCESS, 0.2)}; }}"
        )
        self.quit_button.setStyleSheet(
            f"QPushButton {{ background-color: {COLOR_DANGER}; color: white; border: none; border-radius: 8px; padding: 6px 12px; }} "
            f"QPushButton:hover {{ background-color: {self._lighten_color(COLOR_DANGER, 0.2)}; }}"
        )

    @staticmethod
    def _lighten_color(hex_color: str, factor: float) -> str:
        """Lighten a hex color by a factor (0-1). Returns hex string."""
        # Remove '#'
        hex_color = hex_color.lstrip('#')
        # Convert to RGB
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        # Lighten: move towards white
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        return f'#{r:02x}{g:02x}{b:02x}'
