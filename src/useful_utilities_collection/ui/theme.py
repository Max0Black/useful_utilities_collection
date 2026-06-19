APP_STYLE = """
QMainWindow {
    background: #0d1117;
}

QWidget {
    color: #e6edf3;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 10pt;
}

QWidget#AppRoot {
    background: #11161d;
    border-radius: 0px;
}

QStackedWidget#ContentStack {
    background: #11161d;
    border: 1px solid #212834;
    border-radius: 18px;
}

QWidget#Sidebar {
    background: #161b22;
    border: 1px solid #2d333b;
    border-radius: 18px;
    min-width: 220px;
    max-width: 240px;
}

QLabel#SidebarTitle {
    color: #ffffff;
    font-size: 15pt;
    font-weight: 700;
    background: transparent;
}

QLabel#PageTitle {
    color: #ffffff;
    font-size: 21pt;
    font-weight: 700;
    background: transparent;
}

QLabel#SectionTitle {
    color: #ffffff;
    font-size: 11pt;
    font-weight: 600;
    background: transparent;
}

QLabel#MutedText {
    color: #9da7b3;
    font-size: 10pt;
    background: transparent;
}

QLabel#CardValue {
    color: #e6edf3;
    font-size: 18pt;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="success"] {
    color: #2ea043;
    font-weight: 700;
}

QLabel#CardValue[role="danger"] {
    color: #f85149;
    font-weight: 700;
}

QLabel#CardValue[role="accent"] {
    color: #58a6ff;
    font-weight: 700;
}

QLabel#CardValue[role="neutral"] {
    color: #e6edf3;
    font-weight: 700;
}

QFrame#Panel {
    background: #161b22;
    border: 1px solid #2d333b;
    border-radius: 16px;
}

QPushButton {
    background: #161b22;
    border: 1px solid #2d333b;
    border-radius: 12px;
    padding: 12px 14px;
    text-align: left;
    color: #e6edf3;
}

QPushButton:hover {
    background: #1f2630;
    border-color: #3a4552;
}

QPushButton:checked {
    background: #1f6feb;
    border-color: #1f6feb;
    color: #ffffff;
}

QPushButton#PrimaryButton {
    background: #1f6feb;
    border: none;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    font-weight: 600;
    color: #ffffff;
}

QPushButton#PrimaryButton:hover {
    background: #388bfd;
}

QComboBox, QCheckBox, QProgressBar, QSlider {
    font-size: 10pt;
}

QProgressBar {
    border: 1px solid #2d333b;
    border-radius: 8px;
    background: #0f141a;
    text-align: center;
    min-height: 18px;
}

QProgressBar::chunk {
    background: #1f6feb;
    border-radius: 7px;
}

QLabel#ToastMessage {
    background-color: #1f6feb;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}

QLabel#ToastMessage {
    background-color: #1f6feb;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}
"""