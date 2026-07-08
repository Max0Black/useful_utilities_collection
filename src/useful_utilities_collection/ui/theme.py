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
    font-size: 16pt;
    font-weight: 700;
    background: transparent;
}

/* ── Guard status indicator in sidebar ─────────────────────── */
QFrame#GuardStatusIndicator {
    background: #1a2030;
    border: 1px solid #2d333b;
    border-radius: 10px;
}

QLabel#GuardDot {
    font-size: 10pt;
    background: transparent;
    color: #555e6a;
}

QLabel#GuardDot[active="true"] {
    color: #2ea043;
}

QLabel#GuardDot[active="false"] {
    color: #555e6a;
}

QLabel#GuardStatusText {
    font-size: 9pt;
    color: #9da7b3;
    background: transparent;
}

/* ── Page titles ───────────────────────────────────────────── */
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

/* ── Card values ───────────────────────────────────────────── */
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

/* ── Panels ────────────────────────────────────────────────── */
QFrame#Panel {
    background: #161b22;
    border: 1px solid #2d333b;
    border-radius: 16px;
}

/* ── Guard Mode panel – more prominent ─────────────────────── */
QFrame#GuardModePanel {
    background: #0f2038;
    border: 1px solid #1f6feb;
    border-radius: 14px;
}

QLabel#GuardModeTitle {
    color: #58a6ff;
    font-size: 10pt;
    font-weight: 700;
    background: transparent;
}

/* ── Active microphone tags ────────────────────────────────── */
QLabel#MicTag {
    background: #1a2a1a;
    border: 1px solid #2ea043;
    border-radius: 8px;
    color: #2ea043;
    font-size: 9pt;
    font-weight: 600;
    padding: 3px 8px;
}

QLabel#MicTagInactive {
    background: #1e2028;
    border: 1px solid #3a4552;
    border-radius: 8px;
    color: #9da7b3;
    font-size: 9pt;
    padding: 3px 8px;
}

/* ── Buttons ───────────────────────────────────────────────── */
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

QPushButton#DangerButton {
    background: #6e1a1a;
    border: 1px solid #f85149;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    font-weight: 600;
    color: #ffffff;
}

QPushButton#DangerButton:hover {
    background: #8b2020;
}

/* ── Form controls ─────────────────────────────────────────── */
QComboBox, QCheckBox, QProgressBar, QSlider {
    font-size: 10pt;
}

QComboBox {
    background: #1a2030;
    border: 1px solid #2d333b;
    border-radius: 8px;
    padding: 6px 10px;
    color: #e6edf3;
    min-width: 160px;
}

QComboBox:hover {
    border-color: #3a4552;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background: #1a2030;
    border: 1px solid #2d333b;
    border-radius: 8px;
    color: #e6edf3;
    selection-background-color: #1f6feb;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid #2d333b;
    background: #1a2030;
}

QCheckBox::indicator:checked {
    background: #1f6feb;
    border-color: #1f6feb;
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

/* ── Toast notifications ───────────────────────────────────── */
QLabel#ToastMessage {
    background-color: #1f3a6e;
    border: 1px solid #1f6feb;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}

/* ── Status badge (active guard mode) ─────────────────────── */
QFrame#ActiveGuardBadge {
    background: #0f2038;
    border: 2px solid #1f6feb;
    border-radius: 12px;
}

QLabel#ActiveGuardLabel {
    color: #58a6ff;
    font-weight: 700;
    font-size: 10pt;
    background: transparent;
}
"""