"""Application theme, centralized design system tokens, and stylesheet definition."""

# ── Design Tokens: Colors ─────────────────────────────────────────────
# Core Brand & State
PRIMARY = "#1f6feb"
PRIMARY_HOVER = "#388bfd"
ACCENT = "#58a6ff"
ACCENT_BG = "rgba(88, 166, 255, 0.15)"
SUCCESS = "#2ea043"
SUCCESS_BG = "rgba(46, 160, 67, 0.15)"
DANGER = "#f85149"
DANGER_BG = "rgba(248, 81, 73, 0.15)"

# Surfaces & Backgrounds
BG_BASE = "#0d1117"        # Canvas / window background
BG_SURFACE = "#161b22"     # Elevated surfaces: sidebar, panels, cards, dialogs
BG_INPUT = "#1a2030"       # Inputs, dropdowns, sub-cards
BG_HOVER = "#212836"       # Interactive hover state
BG_PROGRESS = "#0f141a"    # Track backgrounds
BG_TOAST = "#1f3a6e"

# Borders & Dividers
BORDER_SUBTLE = "#212834"   # Dividers, separators, root boundaries
BORDER_DEFAULT = "#2d333b"  # Standard panel, card, and input border
BORDER_HOVER = "#3a4552"    # Focused or hovered borders

# Typography Colors
TEXT_PRIMARY = "#ffffff"    # High contrast: headings, active buttons
TEXT_DEFAULT = "#e6edf3"    # Standard readable text
TEXT_MUTED = "#8b949e"      # Secondary descriptions, hints
TEXT_DISABLED = "#484f58"   # Inactive indicators, disabled states

# ── Design Tokens: Spacing & Radii Scale ──────────────────────────────
RADIUS_SM = "6px"
RADIUS_MD = "8px"
RADIUS_LG = "10px"
RADIUS_XL = "14px"
RADIUS_XXL = "16px"

PAD_BTN_SM = "5px 12px"
PAD_BTN = "10px 14px"
PAD_BTN_LG = "12px 18px"
PAD_INPUT = "6px 10px"
PAD_CARD = "12px"
PAD_TAG = "2px 6px"

# ── Stylesheet Construction ───────────────────────────────────────────
def generate_style() -> str:
    """Builds and returns the global application stylesheet from design tokens."""
    return f"""
QMainWindow {{
    background: {BG_BASE};
}}

QWidget {{
    color: {TEXT_DEFAULT};
    font-family: "Segoe UI", "Inter", -apple-system, sans-serif;
    font-size: 10pt;
}}

QLabel {{
    background: transparent;
}}

QWidget#AppRoot {{
    background: {BG_BASE};
}}

QStackedWidget#ContentStack {{
    background: {BG_BASE};
    border: 1px solid {BORDER_SUBTLE};
    border-radius: {RADIUS_XXL};
}}

/* ── Scroll Areas ───────────────────────────────────────────── */
QScrollArea#PageScroll, QScrollArea#MicGuardScroll,
QScrollArea#PageScroll > QWidget > QWidget,
QScrollArea#MicGuardScroll > QWidget > QWidget,
QWidget#MicGuardInner {{
    background: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background: {BG_BASE};
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background: {BORDER_DEFAULT};
    border-radius: 5px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {BORDER_HOVER};
}}

/* ── Sidebar ────────────────────────────────────────────────── */
QWidget#Sidebar {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_XXL};
    min-width: 220px;
    max-width: 240px;
}}

QLabel#SidebarTitle {{
    color: {TEXT_PRIMARY};
    font-size: 13pt;
    font-weight: 700;
}}

QLabel#SidebarSubtitle {{
    color: {TEXT_MUTED};
    font-size: 8pt;
    font-weight: 600;
    margin-top: -2px;
}}

QLabel#SidebarIconLabel {{
    font-size: 12pt;
}}

QFrame#SidebarGroupSeparator, QFrame#SidebarInnerSeparator {{
    background: {BORDER_SUBTLE};
    max-height: 1px;
    margin: 4px 8px;
}}

QPushButton#SidebarIconButton {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_LG};
    padding: {PAD_BTN};
    text-align: left;
    color: {TEXT_DEFAULT};
}}

QPushButton#SidebarIconButton:hover {{
    background: {BG_HOVER};
}}

QPushButton#SidebarIconButton:checked {{
    background: {PRIMARY};
    border-color: {PRIMARY};
    color: {TEXT_PRIMARY};
}}

/* ── Typographic Scale ──────────────────────────────────────── */
QLabel#PageTitle {{
    color: {TEXT_PRIMARY};
    font-size: 18pt;
    font-weight: 700;
}}

QLabel#SectionTitle, QLabel#ModernSectionHeader {{
    color: {TEXT_PRIMARY};
    font-size: 12pt;
    font-weight: 600;
}}

QLabel#MutedText, QLabel#VolumeMetricCaption, QLabel#AboutFieldLabel, QLabel#AboutCopyright {{
    color: {TEXT_MUTED};
    font-size: 9pt;
}}

QLabel#CardValue, QLabel#VolumeMetricValue {{
    color: {TEXT_DEFAULT};
    font-size: 18pt;
    font-weight: 700;
}}

QLabel#CardValue[role="success"] {{ color: {SUCCESS}; }}
QLabel#CardValue[role="danger"]  {{ color: {DANGER}; }}
QLabel#CardValue[role="accent"], QLabel#VolumeMetricValue[accent="true"] {{ color: {ACCENT}; }}

/* ── Panels & Cards ─────────────────────────────────────────── */
QFrame#Panel, QFrame#ModernPanel, QDialog#GuardExitDialog {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_XL};
}}

QFrame#GuardModePanel {{
    background: {BG_SURFACE};
    border: 1px solid {PRIMARY};
    border-radius: 12px;
}}

QLabel#GuardModeTitle {{
    color: {ACCENT};
    font-size: 10pt;
    font-weight: 700;
}}

QFrame#VolumeMetricCard, QFrame#AboutOssCard {{
    background: {BG_INPUT};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_LG};
    padding: {PAD_CARD};
}}

QFrame#AppFooter {{
    border: none;
    border-top: 1px solid {BORDER_SUBTLE};
}}

/* ── Mic Tag Frames ─────────────────────────────────────────── */
QFrame#MicTagActive, QFrame#MicTagActiveSelected,
QFrame#MicTagSelected, QFrame#MicTagInactive {{
    border-radius: {RADIUS_MD};
    padding: {PAD_TAG};
    border: 1px solid {BORDER_DEFAULT};
    background: {BG_SURFACE};
}}

QFrame#MicTagActive, QFrame#MicTagActiveSelected {{
    background: {SUCCESS_BG};
    border-color: {SUCCESS};
}}

QFrame#MicTagActive QLabel, QFrame#MicTagActiveSelected QLabel {{
    color: {SUCCESS};
}}

QFrame#MicTagSelected {{
    background: {ACCENT_BG};
    border-color: {ACCENT};
}}

QFrame#MicTagSelected QLabel {{
    color: {ACCENT};
}}

QFrame#MicTagInactive QLabel {{
    color: {TEXT_MUTED};
}}

QLabel#MicTagIcon, QLabel#MicTagText, QLabel#MicTagDot {{
    font-size: 9pt;
    font-weight: 600;
}}

/* ── Buttons ────────────────────────────────────────────────── */
QPushButton {{
    background: {BG_SURFACE};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_LG};
    padding: {PAD_BTN};
    text-align: left;
    color: {TEXT_DEFAULT};
}}

QPushButton:hover {{
    background: {BG_HOVER};
    border-color: {BORDER_HOVER};
}}

QPushButton:checked {{
    background: {PRIMARY};
    border-color: {PRIMARY};
    color: {TEXT_PRIMARY};
}}

QPushButton#PrimaryButton, QPushButton#DangerButton,
QPushButton#SmallPrimaryButton, QPushButton#SmallSecondaryButton,
QPushButton#SmallDangerButton, QPushButton#ExitCancelButton,
QPushButton#ExitQuitButton {{
    text-align: center;
    font-weight: 600;
}}

QPushButton#PrimaryButton {{
    background: {PRIMARY};
    border: none;
    padding: {PAD_BTN_LG};
    color: {TEXT_PRIMARY};
}}

QPushButton#PrimaryButton:hover {{
    background: {PRIMARY_HOVER};
}}

QPushButton#DangerButton, QPushButton#ExitQuitButton {{
    background: {DANGER_BG};
    border: 1px solid {DANGER};
    padding: {PAD_BTN_LG};
    color: {TEXT_PRIMARY};
}}

QPushButton#DangerButton:hover, QPushButton#ExitQuitButton:hover {{
    background: {DANGER};
}}

QPushButton#ExitCancelButton {{
    background: {BG_INPUT};
    border: 1px solid {BORDER_DEFAULT};
    padding: {PAD_BTN_LG};
    color: {TEXT_DEFAULT};
}}

QPushButton#ExitCancelButton:hover {{
    background: {BG_HOVER};
    border-color: {BORDER_HOVER};
}}

QPushButton#SmallPrimaryButton, QPushButton#SmallSecondaryButton, QPushButton#SmallDangerButton {{
    border-radius: {RADIUS_MD};
    padding: {PAD_BTN_SM};
    font-size: 9pt;
}}

QPushButton#SmallPrimaryButton {{
    background: {PRIMARY};
    border: none;
    color: {TEXT_PRIMARY};
}}

QPushButton#SmallPrimaryButton:hover {{
    background: {PRIMARY_HOVER};
}}

QPushButton#SmallSecondaryButton {{
    background: {BG_INPUT};
    color: {TEXT_MUTED};
}}

QPushButton#SmallSecondaryButton:hover {{
    background: {BG_HOVER};
    color: {TEXT_DEFAULT};
}}

QPushButton#SmallDangerButton {{
    background: {DANGER_BG};
    border: 1px solid {DANGER};
    color: {TEXT_PRIMARY};
}}

QPushButton#SmallDangerButton:hover {{
    background: {DANGER};
}}

/* ── Form Controls & Inputs ─────────────────────────────────── */
QComboBox, QDoubleSpinBox, QSpinBox {{
    background: {BG_INPUT};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD};
    padding: {PAD_INPUT};
    color: {TEXT_DEFAULT};
    min-width: 160px;
}}

QComboBox:hover, QDoubleSpinBox:hover, QSpinBox:hover {{
    border-color: {BORDER_HOVER};
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox QAbstractItemView {{
    background: {BG_INPUT};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD};
    color: {TEXT_DEFAULT};
    selection-background-color: {PRIMARY};
}}

QDoubleSpinBox::up-button, QDoubleSpinBox::down-button,
QSpinBox::up-button, QSpinBox::down-button {{
    background: transparent;
    border: none;
    width: 20px;
}}

QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover,
QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
    background: {BG_HOVER};
}}

QCheckBox {{
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 5px;
    border: 1px solid {BORDER_DEFAULT};
    background: {BG_INPUT};
}}

QCheckBox::indicator:checked {{
    background: {PRIMARY};
    border-color: {PRIMARY};
}}

QProgressBar {{
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD};
    background: {BG_PROGRESS};
    text-align: center;
    min-height: 18px;
}}

QProgressBar::chunk {{
    background: {PRIMARY};
    border-radius: 7px;
}}

QSlider::groove:horizontal {{
    height: 6px;
    background: {BG_PROGRESS};
    border-radius: 3px;
}}

QSlider::sub-page:horizontal {{
    background: {PRIMARY};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {TEXT_PRIMARY};
    border: 2px solid {PRIMARY};
    width: 16px;
    margin-top: -6px;
    margin-bottom: -6px;
    border-radius: {RADIUS_MD};
}}

QSlider::handle:horizontal:hover {{
    background: {ACCENT};
    border-color: {ACCENT};
}}

/* ── Badges, Indicators & Toasts ────────────────────────────── */
QLabel#ToastMessage {{
    background-color: {BG_TOAST};
    border: 1px solid {PRIMARY};
    color: {TEXT_PRIMARY};
    border-radius: {RADIUS_LG};
    padding: {PAD_BTN};
    font-weight: 600;
}}

QFrame#GuardStatusIndicator {{
    background: {BG_INPUT};
    border: 1px solid {BORDER_DEFAULT};
    border-radius: {RADIUS_MD};
}}

QLabel#GuardDot, QLabel#StatusIndicatorDot {{ font-size: 8pt; }}
QLabel#GuardDot[active="true"], QLabel#StatusIndicatorDot[active="true"]   {{ color: {SUCCESS}; }}
QLabel#GuardDot[active="false"], QLabel#StatusIndicatorDot[active="false"] {{ color: {TEXT_DISABLED}; }}

QLabel#GuardStatusText {{ font-size: 9pt; font-weight: 600; }}
QLabel#GuardStatusText[active="true"]  {{ color: {SUCCESS}; }}
QLabel#GuardStatusText[active="false"] {{ color: {TEXT_MUTED}; }}

QLabel#StatusIndicatorText {{ font-size: 11pt; font-weight: 600; color: {TEXT_PRIMARY}; }}
QLabel#StatusIndicatorHint {{ font-size: 9pt; color: {TEXT_MUTED}; }}

/* ── About Dialog ───────────────────────────────────────────── */
QLabel#AboutOssTitle {{ color: {TEXT_PRIMARY}; font-size: 10pt; font-weight: 600; }}
QLabel#AboutFieldValue {{ color: {TEXT_DEFAULT}; font-size: 9pt; font-weight: 600; }}
QLabel#AboutVersionBadge {{
    background: {PRIMARY};
    color: {TEXT_PRIMARY};
    border-radius: {RADIUS_SM};
    padding: 2px 8px;
    font-size: 8pt;
    font-weight: 700;
}}

/* ── Timer & Countdown Lock ─────────────────────────────────── */
QFrame#TimerWarningBox, QFrame#TimerDisplayPanel, QFrame#TimerDisplayBox {{
    background: {DANGER_BG};
    border: 1.5px solid {DANGER};
    border-radius: 12px;
}}

QLabel#TimerCountdown {{
    color: {DANGER};
    font-size: 24pt;
    font-weight: 800;
    font-family: "Consolas", "Courier New", monospace;
}}

QLabel#TimerWarningTitle, QLabel#TimerInfoText {{
    color: {DANGER};
    font-size: 11pt;
    font-weight: 700;
}}

QLabel#TimerWarningText {{
    color: {TEXT_DEFAULT};
    font-size: 9pt;
}}
"""


# Expose resolved style for application use
APP_STYLE = generate_style()
