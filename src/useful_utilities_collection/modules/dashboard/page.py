from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

class DashboardPage(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(12)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel("A clean starting point for desktop utilities.")
        subtitle.setObjectName("MutedText")

        status_card = QLabel(
            f"Keyboard status: {self.context.state.keyboard_mode}"
        )
        status_card.setObjectName("StatusCard")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(status_card)
        layout.addStretch()