APP_STYLE = """
QMainWindow {
    background: #0f1115;
}

QWidget {
    color: #e8ecf1;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 14px;
}

QWidget#Sidebar {
    background: #171a21;
    border: 1px solid #232833;
    border-radius: 18px;
    min-width: 220px;
    max-width: 240px;
}

QLabel#SidebarTitle {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#PageTitle {
    font-size: 26px;
    font-weight: 700;
    color: #ffffff;
}

QLabel#MutedText {
    color: #9aa4b2;
    font-size: 14px;
}

QLabel#StatusCard {
    background: #171a21;
    border: 1px solid #232833;
    border-radius: 16px;
    padding: 18px;
    font-size: 16px;
    color: #d9e2ec;
}

QPushButton {
    background: #171a21;
    border: 1px solid #2c3340;
    border-radius: 12px;
    padding: 12px 14px;
    text-align: left;
}

QPushButton:hover {
    background: #1d2330;
    border-color: #3a4354;
}

QPushButton#PrimaryButton {
    background: #3b82f6;
    color: white;
    border: none;
    text-align: center;
    font-weight: 600;
    padding: 14px 18px;
}

QPushButton#PrimaryButton:hover {
    background: #2563eb;
}
"""