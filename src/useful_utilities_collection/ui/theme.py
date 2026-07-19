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

/* ── Scroll areas – must be fully transparent so dark theme shows ── */
QScrollArea#MicGuardScroll {
    background: transparent;
    border: none;
}

QScrollArea#MicGuardScroll > QWidget > QWidget {
    background: transparent;
}

QWidget#MicGuardInner {
    background: transparent;
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
    background: transparent;
}

QLabel#CardValue[role="danger"] {
    color: #f85149;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="accent"] {
    color: #58a6ff;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="neutral"] {
    color: #e6edf3;
    font-weight: 700;
    background: transparent;
}

/* ── Panels ────────────────────────────────────────────────── */
QFrame#Panel {
    background: #161b22;
    border: 1px solid #2d333b;
    border-radius: 16px;
}

/* ── Guard Mode panel – more prominent ─────────────────────── */
QFrame#GuardModePanel {
    background: #161b22;
    border: 1px solid #1f6feb;
    border-radius: 14px;
}

QLabel#GuardModeTitle {
    color: #58a6ff;
    font-size: 10pt;
    font-weight: 700;
    background: transparent;
}

/* ── Clickable mic tag frames ──────────────────────────────── */

/* Active mic (guard ON) – green */
QFrame#MicTagActive {
    background: #1a2a1a;
    border: 1px solid #2ea043;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagActive:hover {
    background: #22382a;
    border-color: #3fb950;
}

/* Active + currently selected – green with thicker border */
QFrame#MicTagActiveSelected {
    background: #1e3020;
    border: 2px solid #3fb950;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagActiveSelected:hover {
    background: #254030;
    border-color: #56d364;
}

/* Inactive but currently selected – blue outline */
QFrame#MicTagSelected {
    background: #1a2038;
    border: 2px solid #58a6ff;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagSelected:hover {
    background: #202a4a;
    border-color: #79c0ff;
}

/* Inactive, not selected */
QFrame#MicTagInactive {
    background: #1e2028;
    border: 1px solid #3a4552;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagInactive:hover {
    background: #252b36;
    border-color: #58a6ff;
}

QLabel#MicTagDot {
    color: #2ea043;
    font-size: 8pt;
    background: transparent;
}

QLabel#MicTagIcon {
    background: transparent;
    font-size: 11pt;
}

QLabel#MicTagText {
    background: transparent;
    font-size: 9pt;
    font-weight: 600;
    color: inherit;
}

QFrame#MicTagActive QLabel,
QFrame#MicTagActiveSelected QLabel {
    color: #2ea043;
}

QFrame#MicTagSelected QLabel {
    color: #79c0ff;
}

QFrame#MicTagInactive QLabel {
    color: #9da7b3;
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

/* ── Small action buttons (for mic panel header) ───────────── */
QPushButton#SmallPrimaryButton {
    background: #1f6feb;
    border: none;
    border-radius: 8px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 9pt;
    color: #ffffff;
}

QPushButton#SmallPrimaryButton:hover {
    background: #388bfd;
}

QPushButton#SmallDangerButton {
    background: #6e1a1a;
    border: 1px solid #f85149;
    border-radius: 8px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 9pt;
    color: #ffffff;
}

QPushButton#SmallDangerButton:hover {
    background: #8b2020;
}

QPushButton#SmallSecondaryButton {
    background: #1e2630;
    border: 1px solid #3a4552;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 9pt;
    color: #9da7b3;
}

QPushButton#SmallSecondaryButton:hover {
    background: #253040;
    border-color: #58a6ff;
    color: #e6edf3;
}

/* ── Form controls ─────────────────────────────────────────── */
QComboBox, QDoubleSpinBox, QCheckBox, QProgressBar, QSlider {
    font-size: 10pt;
}

QComboBox, QDoubleSpinBox {
    background: #1a2030;
    border: 1px solid #2d333b;
    border-radius: 8px;
    padding: 6px 10px;
    color: #e6edf3;
    min-width: 160px;
}

QComboBox:hover, QDoubleSpinBox:hover {
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

QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: transparent;
    border: none;
    width: 20px;
}

QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background: #252b36;
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