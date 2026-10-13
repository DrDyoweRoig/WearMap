"""Design tokens (light / dark) and the application stylesheet built from them."""
from string import Template

LIGHT = {
    "bg": "#F2F6F3", "surface": "#FFFFFF", "surface_alt": "#EAF3EC",
    "border": "#D3E2D8", "text": "#15301F", "text_muted": "#5B7A66",
    "accent": "#16A34A", "accent_hover": "#15803D", "accent_soft": "#DCFCE7",
    "accent_text": "#FFFFFF", "danger": "#DC2626", "canvas_bg": "#1E2030",
}

DARK = {
    "bg": "#12161A", "surface": "#1A2025", "surface_alt": "#222A30",
    "border": "#2E383F", "text": "#E3EDE7", "text_muted": "#8DA89A",
    "accent": "#22C55E", "accent_hover": "#4ADE80", "accent_soft": "#1E3A2A",
    "accent_text": "#052E16", "danger": "#F87171", "canvas_bg": "#0C0F12",
}

THEMES = {"light": LIGHT, "dark": DARK}

_QSS = Template("""
* {
    font-family: 'Segoe UI Variable', 'Segoe UI', system-ui, sans-serif;
    font-size: 13px;
    color: $text;
}
QMainWindow, QDialog { background: $bg; }
QToolTip {
    background: $surface; color: $text; border: 1px solid $border;
    border-radius: 6px; padding: 4px 8px;
}

/* menu bar + menus */
QMenuBar { background: $surface; border-bottom: 1px solid $border; padding: 2px 6px; }
QMenuBar::item { background: transparent; padding: 5px 12px; border-radius: 6px; }
QMenuBar::item:selected { background: $accent_soft; }
QMenu {
    background: $surface; border: 1px solid $border; border-radius: 10px; padding: 6px;
}
QMenu::item { padding: 7px 24px 7px 14px; border-radius: 6px; }
QMenu::item:selected { background: $accent_soft; }
QMenu::item:disabled { color: $text_muted; }
QMenu::separator { height: 1px; background: $border; margin: 5px 10px; }

/* toolbar */
QToolBar {
    background: $surface; border: none; border-bottom: 1px solid $border;
    spacing: 4px; padding: 6px 10px;
}
QToolBar::separator { width: 1px; background: $border; margin: 6px 8px; }
QToolButton {
    background: transparent; border: 1px solid transparent; border-radius: 8px;
    padding: 4px 6px; font-size: 11px; font-weight: 500;
}
QToolButton:hover { background: $surface_alt; }
QToolButton:pressed { background: $accent_soft; }
QToolButton:checked {
    background: $accent; color: $accent_text; border-color: $accent;
}
QToolButton:disabled { color: $text_muted; }
QToolButton::menu-button { border: none; width: 14px; }

/* panels */
QScrollArea { background: transparent; border: none; }
QScrollArea > QWidget > QWidget { background: transparent; }
QWidget#sidePanel { background: $bg; }
QTabWidget::pane {
    border: 1px solid $border; border-radius: 10px; background: $surface; top: -1px;
}
QTabBar::tab {
    background: transparent; padding: 8px 16px; margin-right: 2px;
    border-top-left-radius: 8px; border-top-right-radius: 8px; color: $text_muted;
    font-weight: 600;
}
QTabBar::tab:selected { background: $surface; color: $accent; }
QTabBar::tab:hover:!selected { background: $surface_alt; }
QLabel { background: transparent; }
QLabel#panelTitle {
    font-weight: 700; font-size: 11px; color: $text_muted; padding-top: 4px;
}
QLabel#muted { color: $text_muted; font-size: 12px; }
QLabel#heading { font-weight: 700; font-size: 13px; }
QLabel#navLabel { color: $text_muted; padding: 0 6px; font-size: 12px; font-weight: 600; }
QFrame#sep { background: $border; max-height: 1px; border: none; }
QGroupBox {
    font-weight: 700; border: 1px solid $border; border-radius: 10px;
    margin-top: 10px; padding: 10px 8px 8px 8px; background: $surface_alt;
}
QGroupBox::title {
    subcontrol-origin: margin; left: 10px; padding: 0 5px; color: $text_muted;
    background: transparent;
}

/* buttons */
QPushButton {
    background: $accent; color: $accent_text; border: none; border-radius: 8px;
    padding: 7px 16px; font-weight: 600;
}
QPushButton:hover { background: $accent_hover; }
QPushButton:pressed { background: $accent_hover; padding-top: 8px; }
QPushButton:disabled { background: $surface_alt; color: $text_muted; }
QPushButton#deleteBtn {
    background: transparent; color: $danger; border: 1px solid $danger;
}
QPushButton#deleteBtn:hover { background: $danger; color: #FFFFFF; }
QDialogButtonBox QPushButton { min-width: 88px; }

/* inputs */
QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox {
    background: $surface; border: 1px solid $border; border-radius: 8px;
    padding: 5px 9px; selection-background-color: $accent; selection-color: $accent_text;
}
QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {
    border: 1px solid $accent;
}
QComboBox:hover { border-color: $accent; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background: $surface; border: 1px solid $border; border-radius: 8px;
    selection-background-color: $accent_soft; selection-color: $text; outline: none;
}

/* lists + table */
QListWidget {
    background: $surface; border: 1px solid $border; border-radius: 8px; outline: none;
}
QListWidget::item { padding: 4px 6px; }
QListWidget::item:selected { background: $accent_soft; color: $text; }
QTableWidget {
    background: $surface; alternate-background-color: $surface_alt;
    border: 1px solid $border; border-radius: 8px; gridline-color: transparent;
    selection-background-color: $accent_soft; selection-color: $text;
}
QTableWidget::item { padding: 3px 4px; border: none; }
QTableWidget::item:selected { background: $accent_soft; }
QHeaderView { background: transparent; }
QHeaderView::section {
    background: $surface_alt; color: $text_muted; border: none;
    border-bottom: 1px solid $border; padding: 6px 8px; font-weight: 700; font-size: 11px;
}

/* scrollbars */
QScrollBar:vertical { background: transparent; width: 10px; margin: 2px; }
QScrollBar::handle:vertical { background: $border; border-radius: 4px; min-height: 28px; }
QScrollBar::handle:vertical:hover { background: $accent; }
QScrollBar:horizontal { background: transparent; height: 10px; margin: 2px; }
QScrollBar::handle:horizontal { background: $border; border-radius: 4px; min-width: 28px; }
QScrollBar::handle:horizontal:hover { background: $accent; }
QScrollBar::add-line, QScrollBar::sub-line { width: 0; height: 0; }

/* status bar */
QStatusBar { background: $surface; border-top: 1px solid $border; }
QStatusBar::item { border: none; }
QLabel#pill {
    background: $surface_alt; border-radius: 9px; padding: 2px 10px;
    color: $text_muted; font-size: 12px;
}
QLabel#hint { color: $accent; font-style: italic; padding: 0 8px; }

QSplitter::handle { background: $border; }
QSplitter::handle:hover { background: $accent; }
QSplitter::handle:horizontal { width: 2px; }

/* sliders + checkboxes */
QSlider::groove:horizontal { height: 4px; background: $border; border-radius: 2px; }
QSlider::sub-page:horizontal { background: $accent; border-radius: 2px; }
QSlider::handle:horizontal {
    width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; background: $accent;
}
QSlider::handle:horizontal:hover { background: $accent_hover; }
QCheckBox { spacing: 8px; }
QCheckBox::indicator {
    width: 16px; height: 16px; border-radius: 5px;
    border: 1px solid $border; background: $surface;
}
QCheckBox::indicator:hover { border-color: $accent; }
QCheckBox::indicator:checked { background: $accent; border-color: $accent; }
""")


def build_qss(tokens: dict) -> str:
    return _QSS.substitute(tokens)


def get_tokens(name: str) -> dict:
    return THEMES.get(name, LIGHT)


def current_theme() -> str:
    try:
        from PyQt6.QtCore import QSettings
        name = QSettings("Wearmap Project", "Wearmap").value("theme", "light")
        return name if name in THEMES else "light"
    except Exception:
        return "light"


def set_theme(name: str) -> None:
    try:
        from PyQt6.QtCore import QSettings
        QSettings("Wearmap Project", "Wearmap").setValue("theme", name)
    except Exception:
        pass
