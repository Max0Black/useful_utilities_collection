# ── Central Color Palette ───────────────────────────────────────────
COLOR_PALETTE = {
    # Main app backgrounds
    "COLOR_BG_WINDOW": "#0d1117",
    "COLOR_BG_ROOT_STACK": "#11161d",
    "COLOR_BG_PANEL_SIDEBAR_BTN": "#161b22",
    "COLOR_BG_INPUT_CONTROL": "#1a2030",
    "COLOR_BG_PROGRESS": "#0f141a",
    "COLOR_BG_GUARD_BADGE": "#0f2038",
    "COLOR_BG_TOAST": "#1f3a6e",

    # Borders
    "COLOR_BORDER_STACK": "#212834",
    "COLOR_BORDER_PANEL_SIDEBAR_CTRL": "#2d333b",

    # Core theme colors
    "COLOR_PRIMARY": "#1f6feb",
    "COLOR_BG_PRIMARY_HOVER": "#388bfd",
    "COLOR_ACCENT": "#58a6ff",
    "COLOR_SUCCESS": "#2ea043",
    "COLOR_DANGER": "#f85149",
    
    # Text colors
    "COLOR_TEXT_MAIN": "#e6edf3",
    "COLOR_TEXT_WHITE": "#ffffff",
    "COLOR_TEXT_MUTED_LIGHT": "#9da7b3",
    "COLOR_TEXT_MUTED_DARK": "#555e6a",

    # Mic Tags Specific Colors
    "COLOR_BG_MIC_TAG_ACTIVE": "#1a2a1a",
    "COLOR_BORDER_MIC_TAG_ACTIVE": "#2ea043",
    "COLOR_BG_MIC_TAG_ACTIVE_HOVER": "#22382a",
    "COLOR_BORDER_MIC_TAG_ACTIVE_HOVER": "#3fb950",
    "COLOR_BG_MIC_TAG_ACTIVE_SELECTED": "#1e3020",
    "COLOR_BORDER_MIC_TAG_ACTIVE_SELECTED": "#3fb950",
    "COLOR_BG_MIC_TAG_ACTIVE_SELECTED_HOVER": "#254030",
    "COLOR_BORDER_MIC_TAG_ACTIVE_SELECTED_HOVER": "#56d364",
    "COLOR_BG_MIC_TAG_SELECTED": "#1a2038",
    "COLOR_BORDER_MIC_TAG_SELECTED": "#58a6ff",
    "COLOR_BG_MIC_TAG_SELECTED_HOVER": "#202a4a",
    "COLOR_BORDER_MIC_TAG_SELECTED_HOVER": "#79c0ff",
    "COLOR_BG_MIC_TAG_INACTIVE": "#1e2028",
    "COLOR_BORDER_MIC_TAG_INACTIVE": "#3a4552",
    "COLOR_BG_MIC_TAG_INACTIVE_HOVER": "#252b36",

    # Buttons Hover & Alert Variants
    "COLOR_BG_BTN_HOVER": "#1f2630",
    "COLOR_BORDER_BTN_HOVER": "#3a4552",
    "COLOR_BG_DANGER": "#6e1a1a",
    "COLOR_BG_DANGER_HOVER": "#8b2020",
    "COLOR_BG_SMALL_SEC_BTN": "#1e2630",
    "COLOR_BG_SMALL_SEC_BTN_HOVER": "#253040",
}

# ── Dynamic Stylesheet Template ───────────────────────────────────────
_RAW_STYLE = """
QMainWindow {
    background: COLOR_BG_WINDOW;
}

QWidget {
    color: COLOR_TEXT_MAIN;
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 10pt;
}

QWidget#AppRoot {
    background: COLOR_BG_ROOT_STACK;
    border-radius: 0px;
}

QStackedWidget#ContentStack {
    background: COLOR_BG_ROOT_STACK;
    border: 1px solid COLOR_BORDER_STACK;
    border-radius: 18px;
}

/* ── Scrollable pages (prevent clipping on small windows) ── */
QScrollArea#PageScroll {
    background: transparent;
    border: none;
}

QScrollArea#PageScroll > QWidget > QWidget {
    background: transparent;
}

QScrollArea#PageScroll QScrollBar:vertical {
    background: COLOR_BG_ROOT_STACK;
    width: 10px;
    border-radius: 5px;
}

QScrollArea#PageScroll QScrollBar::handle:vertical {
    background: COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 5px;
    min-height: 24px;
}

QScrollArea#PageScroll QScrollBar::handle:vertical:hover {
    background: COLOR_BORDER_BTN_HOVER;
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
    background: COLOR_BG_PANEL_SIDEBAR_BTN;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 18px;
    min-width: 220px;
    max-width: 240px;
}

QLabel#SidebarTitle {
    color: COLOR_TEXT_WHITE;
    font-size: 16pt;
    font-weight: 700;
    background: transparent;
}

/* ── Guard status indicator in sidebar ─────────────────────── */
QFrame#GuardStatusIndicator {
    background: COLOR_BG_INPUT_CONTROL;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 10px;
}

QLabel#GuardDot {
    font-size: 10pt;
    background: transparent;
    color: COLOR_TEXT_MUTED_DARK;
}

QLabel#GuardDot[active="true"] {
    color: COLOR_SUCCESS;
}

QLabel#GuardDot[active="false"] {
    color: COLOR_TEXT_MUTED_DARK;
}

QLabel#GuardStatusText {
    font-size: 9pt;
    color: COLOR_TEXT_MUTED_LIGHT;
    background: transparent;
}

/* ── Page titles ───────────────────────────────────────────── */
QLabel#PageTitle {
    color: COLOR_TEXT_WHITE;
    font-size: 21pt;
    font-weight: 700;
    background: transparent;
}

QLabel#SectionTitle {
    color: COLOR_TEXT_WHITE;
    font-size: 11pt;
    font-weight: 600;
    background: transparent;
}

QLabel#MutedText {
    color: COLOR_TEXT_MUTED_LIGHT;
    font-size: 10pt;
    background: transparent;
}

/* ── Card values ───────────────────────────────────────────── */
QLabel#CardValue {
    color: COLOR_TEXT_MAIN;
    font-size: 18pt;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="success"] {
    color: COLOR_SUCCESS;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="danger"] {
    color: COLOR_DANGER;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="accent"] {
    color: COLOR_ACCENT;
    font-weight: 700;
    background: transparent;
}

QLabel#CardValue[role="neutral"] {
    color: COLOR_TEXT_MAIN;
    font-weight: 700;
    background: transparent;
}

/* ── Panels ────────────────────────────────────────────────── */
QFrame#Panel {
    background: COLOR_BG_PANEL_SIDEBAR_BTN;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 16px;
}

/* ── Guard Mode panel – more prominent ─────────────────────── */
QFrame#GuardModePanel {
    background: COLOR_BG_PANEL_SIDEBAR_BTN;
    border: 1px solid COLOR_PRIMARY;
    border-radius: 14px;
}

QLabel#GuardModeTitle {
    color: COLOR_ACCENT;
    font-size: 10pt;
    font-weight: 700;
    background: transparent;
}

/* ── Clickable mic tag frames ──────────────────────────────── */

/* Active mic (guard ON) – green */
QFrame#MicTagActive {
    background: COLOR_BG_MIC_TAG_ACTIVE;
    border: 1px solid COLOR_BORDER_MIC_TAG_ACTIVE;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagActive:hover {
    background: COLOR_BG_MIC_TAG_ACTIVE_HOVER;
    border-color: COLOR_BORDER_MIC_TAG_ACTIVE_HOVER;
}

/* Active + currently selected – green with thicker border */
QFrame#MicTagActiveSelected {
    background: COLOR_BG_MIC_TAG_ACTIVE_SELECTED;
    border: 2px solid COLOR_BORDER_MIC_TAG_ACTIVE_SELECTED;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagActiveSelected:hover {
    background: COLOR_BG_MIC_TAG_ACTIVE_SELECTED_HOVER;
    border-color: COLOR_BORDER_MIC_TAG_ACTIVE_SELECTED_HOVER;
}

/* Inactive but currently selected – blue outline */
QFrame#MicTagSelected {
    background: COLOR_BG_MIC_TAG_SELECTED;
    border: 2px solid COLOR_BORDER_MIC_TAG_SELECTED;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagSelected:hover {
    background: COLOR_BG_MIC_TAG_SELECTED_HOVER;
    border-color: COLOR_BORDER_MIC_TAG_SELECTED_HOVER;
}

/* Inactive, not selected */
QFrame#MicTagInactive {
    background: COLOR_BG_MIC_TAG_INACTIVE;
    border: 1px solid COLOR_BORDER_MIC_TAG_INACTIVE;
    border-radius: 8px;
    padding: 2px 0px;
}

QFrame#MicTagInactive:hover {
    background: COLOR_BG_MIC_TAG_INACTIVE_HOVER;
    border-color: COLOR_ACCENT;
}

QLabel#MicTagDot {
    color: COLOR_SUCCESS;
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
    color: COLOR_SUCCESS;
}

QFrame#MicTagSelected QLabel {
    color: COLOR_BORDER_MIC_TAG_SELECTED_HOVER;
}

QFrame#MicTagInactive QLabel {
    color: COLOR_TEXT_MUTED_LIGHT;
}

/* ── Buttons ───────────────────────────────────────────────── */
QPushButton {
    background: COLOR_BG_PANEL_SIDEBAR_BTN;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 12px;
    padding: 12px 14px;
    text-align: left;
    color: COLOR_TEXT_MAIN;
}

QPushButton:hover {
    background: COLOR_BG_BTN_HOVER;
    border-color: COLOR_BORDER_BTN_HOVER;
}

QPushButton:checked {
    background: COLOR_PRIMARY;
    border-color: COLOR_PRIMARY;
    color: COLOR_TEXT_WHITE;
}

QPushButton#PrimaryButton {
    background: COLOR_PRIMARY;
    border: none;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    font-weight: 600;
    color: COLOR_TEXT_WHITE;
}

QPushButton#PrimaryButton:hover {
    background: COLOR_BG_PRIMARY_HOVER;
}

QPushButton#DangerButton {
    background: COLOR_BG_DANGER;
    border: 1px solid COLOR_DANGER;
    border-radius: 12px;
    padding: 14px 18px;
    text-align: center;
    font-weight: 600;
    color: COLOR_TEXT_WHITE;
}

QPushButton#DangerButton:hover {
    background: COLOR_BG_DANGER_HOVER;
}

/* ── Small action buttons (for mic panel header) ───────────── */
QPushButton#SmallPrimaryButton {
    background: COLOR_PRIMARY;
    border: none;
    border-radius: 8px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 9pt;
    color: COLOR_TEXT_WHITE;
}

QPushButton#SmallPrimaryButton:hover {
    background: COLOR_BG_PRIMARY_HOVER;
}

QPushButton#SmallDangerButton {
    background: COLOR_BG_DANGER;
    border: 1px solid COLOR_DANGER;
    border-radius: 8px;
    padding: 5px 12px;
    font-weight: 600;
    font-size: 9pt;
    color: COLOR_TEXT_WHITE;
}

QPushButton#SmallDangerButton:hover {
    background: COLOR_BG_DANGER_HOVER;
}

QPushButton#SmallSecondaryButton {
    background: COLOR_BG_SMALL_SEC_BTN;
    border: 1px solid COLOR_BORDER_BTN_HOVER;
    border-radius: 8px;
    padding: 5px 12px;
    font-size: 9pt;
    color: COLOR_TEXT_MUTED_LIGHT;
}

QPushButton#SmallSecondaryButton:hover {
    background: COLOR_BG_SMALL_SEC_BTN_HOVER;
    border-color: COLOR_ACCENT;
    color: COLOR_TEXT_MAIN;
}

/* ── Form controls ─────────────────────────────────────────── */
QComboBox, QDoubleSpinBox, QCheckBox, QProgressBar, QSlider {
    font-size: 10pt;
}

QComboBox, QDoubleSpinBox {
    background: COLOR_BG_INPUT_CONTROL;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 8px;
    padding: 6px 10px;
    color: COLOR_TEXT_MAIN;
    min-width: 160px;
}

QComboBox:hover, QDoubleSpinBox:hover {
    border-color: COLOR_BORDER_BTN_HOVER;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background: COLOR_BG_INPUT_CONTROL;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 8px;
    color: COLOR_TEXT_MAIN;
    selection-background-color: COLOR_PRIMARY;
}

QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: transparent;
    border: none;
    width: 20px;
}

QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background: COLOR_BG_MIC_TAG_INACTIVE_HOVER;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    background: COLOR_BG_INPUT_CONTROL;
}

QCheckBox::indicator:checked {
    background: COLOR_PRIMARY;
    border-color: COLOR_PRIMARY;
}

QProgressBar {
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 8px;
    background: COLOR_BG_PROGRESS;
    text-align: center;
    min-height: 18px;
}

QProgressBar::chunk {
    background: COLOR_PRIMARY;
    border-radius: 7px;
}

/* ── Toast notifications ───────────────────────────────────── */
QLabel#ToastMessage {
    background-color: COLOR_BG_TOAST;
    border: 1px solid COLOR_PRIMARY;
    color: white;
    border-radius: 10px;
    padding: 10px 14px;
    font-weight: 600;
}

/* ── Status badge (active guard mode) ─────────────────────── */
QFrame#ActiveGuardBadge {
    background: COLOR_BG_GUARD_BADGE;
    border: 2px solid COLOR_PRIMARY;
    border-radius: 12px;
}

QLabel#ActiveGuardLabel {
    color: COLOR_ACCENT;
    font-weight: 700;
    font-size: 10pt;
    background: transparent;
}

/* ── About page ──────────────────────────────────────── */
QLabel#AboutVersionBadge {
    background: COLOR_BG_INPUT_CONTROL;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    color: COLOR_TEXT_MUTED_LIGHT;
    font-weight: 600;
    font-size: 9pt;
    padding: 3px 10px;
    border-radius: 8px;
}

QFrame#AboutOssCard {
    background: COLOR_BG_GUARD_BADGE;
    border: 1px solid COLOR_BORDER_MIC_TAG_ACTIVE;
    border-radius: 14px;
}

QLabel#AboutOssTitle {
    color: COLOR_SUCCESS;
    font-size: 12pt;
    font-weight: 700;
    background: transparent;
}

QLabel#AboutOssIcon {
    font-size: 13pt;
    background: transparent;
}

QLabel#AboutFieldLabel {
    color: COLOR_TEXT_MUTED_LIGHT;
    font-size: 10pt;
    background: transparent;
}

QLabel#AboutFieldValue {
    color: COLOR_TEXT_MAIN;
    font-size: 10pt;
    font-weight: 600;
    background: transparent;
}

QLabel#AboutCopyright {
    color: COLOR_TEXT_MUTED_LIGHT;
    font-size: 8pt;
    background: transparent;
}

/* ── Sidebar bottom group (Settings / About) ─────────── */
QFrame#SidebarGroupSeparator {
    background: COLOR_BORDER_STACK;
    max-height: 1px;
    margin: 6px 8px;
}

QFrame#SidebarInnerSeparator {
    background: COLOR_BORDER_STACK;
    max-height: 1px;
    margin: 2px 12px;
}

QPushButton#SidebarIconButton {
    background: COLOR_BG_PANEL_SIDEBAR_BTN;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 12px;
    padding: 12px 16px;
    text-align: left;
    color: COLOR_TEXT_MAIN;
    font-size: 10pt;
}

QPushButton#SidebarIconButton:hover {
    background: COLOR_BG_INPUT_CONTROL;
}

QPushButton#SidebarIconButton:checked {
    background: COLOR_PRIMARY;
    color: COLOR_TEXT_WHITE;
}

/* ── App footer ──────────────────────────────────────── */
QFrame#AppFooter {
    background: transparent;
    border: none;
    border-top: 1px solid COLOR_BORDER_STACK;
}

/* ── Guard exit confirmation dialog ────────────────────── */
QDialog#GuardExitDialog {
    background: COLOR_BG_PANEL_SIDEBAR_BTN;
    border: 1px solid COLOR_BORDER_PANEL_SIDEBAR_CTRL;
    border-radius: 16px;
}

"""

def generate_style() -> str:
    """Replaces color constants in the raw style sheet and returns the resolved stylesheet string."""
    resolved_style = _RAW_STYLE
    # Sort keys by length in descending order to avoid prefix replacement conflicts
    for key in sorted(COLOR_PALETTE.keys(), key=len, reverse=True):
        val = COLOR_PALETTE[key]
        resolved_style = resolved_style.replace(key, val)
    return resolved_style

# Expose the resolved style string for compatibility
APP_STYLE = generate_style()