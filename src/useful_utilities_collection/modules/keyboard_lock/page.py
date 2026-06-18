from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from useful_utilities_collection.modules.keyboard_lock.controller import KeyboardLockController

class KeyboardLockPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.controller = KeyboardLockController(context)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        title = QLabel("Keyboard Lock")
        title.setObjectName("PageTitle")

        subtitle = QLabel("Lock the keyboard while keeping the mouse active.")
        subtitle.setObjectName("MutedText")

        self.status_label = QLabel()
        self.status_label.setObjectName("StatusCard")

        self.toggle_button = QPushButton()
        self.toggle_button.setObjectName("PrimaryButton")
        self.toggle_button.clicked.connect(self.on_toggle)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.status_label)
        layout.addWidget(self.toggle_button)
        layout.addStretch()

        self.refresh()

    def on_toggle(self) -> None:
        self.controller.toggle()
        self.refresh()

    def refresh(self) -> None:
        self.status_label.setText(
            f"Status: {self.context.state.keyboard_mode}"
        )

        if self.context.state.keyboard_locked:
            self.toggle_button.setText("Unlock Keyboard")
        else:
            self.toggle_button.setText("Lock Keyboard")