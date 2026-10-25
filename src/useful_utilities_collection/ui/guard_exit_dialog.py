from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from useful_utilities_collection.core.translation import t


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
        """Ensure both buttons have the same width."""
        self.cancel_button.adjustSize()
        self.quit_button.adjustSize()
        width = max(self.cancel_button.sizeHint().width(),
                    self.quit_button.sizeHint().width()) + 20
        self.cancel_button.setFixedWidth(width)
        self.quit_button.setFixedWidth(width)
