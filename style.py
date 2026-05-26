MAIN_STYLE = """

/* ─── Global ──────────────────────────────────────────────────────────── */
* {
    font-family: 'Segoe UI Variable', 'Segoe UI', system-ui, sans-serif;
    font-size: 13px;
    color: #14532D;
}

QMainWindow {
    background: #E4F0E8;
}

/* ─── Menu bar ────────────────────────────────────────────────────────── */
QMenuBar {
    background: #ffffff;
    border-bottom: 1px solid #C9E8D3;
    padding: 2px 6px;
    spacing: 2px;
}
QMenuBar::item {
    background: transparent;
    padding: 5px 12px;
    border-radius: 6px;
    color: #14532D;
    font-weight: 500;
}
QMenuBar::item:selected { background: #DCFCE7; }
QMenuBar::item:pressed  { background: #BBF7D0; }

QMenu {
    background: #ffffff;
    border: 1px solid #C9E8D3;
    border-radius: 10px;
    padding: 5px;
    color: #14532D;
}
QMenu::item {
    padding: 7px 22px 7px 12px;
    border-radius: 6px;
    color: #14532D;
}
QMenu::item:selected { background: #DCFCE7; color: #14532D; }
QMenu::separator { height: 1px; background: #C9E8D3; margin: 4px 10px; }

/* ─── Toolbar ─────────────────────────────────────────────────────────── */
QToolBar {
    background: #ffffff;
    border-bottom: 1px solid #C9E8D3;
    spacing: 3px;
    padding: 6px 12px;
}
QToolBar::separator {
    width: 1px;
    background: #C9E8D3;
    margin: 6px 6px;
}

QToolButton {
    background: #F0FBF4;
    border: 1px solid #C9E8D3;
    border-radius: 8px;
    padding: 5px 13px;
    color: #166534;
    font-size: 13px;
    font-weight: 500;
    min-height: 30px;
}
QToolButton:hover {
    background: #DCFCE7;
    border-color: #86EFAC;
    color: #14532D;
}
QToolButton:pressed {
    background: #BBF7D0;
    border-color: #4ADE80;
}
QToolButton:checked {
    background: #16A34A;
    border-color: #15803D;
    color: #ffffff;
    font-weight: 700;
}

/* ─── Side panel ──────────────────────────────────────────────────────── */
QWidget#sidePanel {
    background: #ffffff;
    border-left: 1px solid #C9E8D3;
}

/* ─── Push buttons ────────────────────────────────────────────────────── */
QPushButton {
    background: #16A34A;
    color: #ffffff;
    border: none;
    border-bottom: 2px solid #15803D;
    border-radius: 8px;
    padding: 7px 18px;
    font-weight: 600;
    min-height: 30px;
}
QPushButton:hover   { background: #15803D; border-bottom-color: #166534; }
QPushButton:pressed { background: #166534; border-bottom-width: 0; padding-top: 9px; }
QPushButton:disabled {
    background: #D1FAE5;
    border-bottom-color: #A7F3D0;
    color: #6EE7B7;
}

QPushButton#deleteBtn {
    background: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
    border-bottom: 2px solid #FCA5A5;
}
QPushButton#deleteBtn:hover   { background: #EF4444; color: #ffffff; border-color: #DC2626; }
QPushButton#deleteBtn:pressed { background: #DC2626; color: #ffffff; border-bottom-width: 0; }

/* ─── Table ───────────────────────────────────────────────────────────── */
QTableWidget {
    background: #ffffff;
    alternate-background-color: #F4FCF7;
    border: 1px solid #C9E8D3;
    border-radius: 10px;
    gridline-color: transparent;
    selection-background-color: #DCFCE7;
    selection-color: #14532D;
    outline: none;
}
QTableWidget::item {
    padding: 5px 10px;
    border-bottom: 1px solid #ECFDF5;
}
QTableWidget::item:selected {
    background: #DCFCE7;
    color: #14532D;
}

QHeaderView::section {
    background: #E9F7EE;
    color: #14532D;
    border: none;
    border-bottom: 2px solid #4ADE80;
    padding: 6px 10px;
    font-weight: 700;
    font-size: 12px;
    letter-spacing: 0.3px;
    text-transform: uppercase;
}
QHeaderView {
    background: #E9F7EE;
    border-radius: 0;
}

/* ─── Scrollbars ──────────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 10px;
    border-radius: 5px;
    margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #86EFAC;
    border-radius: 5px;
    min-height: 28px;
}
QScrollBar::handle:vertical:hover { background: #22C55E; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QScrollBar:horizontal {
    background: transparent;
    height: 10px;
    border-radius: 5px;
    margin: 2px 4px;
}
QScrollBar::handle:horizontal {
    background: #86EFAC;
    border-radius: 5px;
    min-width: 28px;
}
QScrollBar::handle:horizontal:hover { background: #22C55E; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ─── Status bar ──────────────────────────────────────────────────────── */
QStatusBar {
    background: #ffffff;
    color: #166534;
    border-top: 1px solid #C9E8D3;
    padding: 3px 6px;
    font-size: 12px;
}

/* ─── Splitter ────────────────────────────────────────────────────────── */
QSplitter::handle           { background: #C9E8D3; }
QSplitter::handle:hover     { background: #4ADE80; }
QSplitter::handle:horizontal { width: 2px; }

/* ─── Labels ──────────────────────────────────────────────────────────── */
QLabel { color: #14532D; background: transparent; }
QLabel#panelTitle {
    font-size: 11px;
    font-weight: 700;
    color: #166534;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    padding: 6px 0 3px 0;
}

/* ─── Dialogs ─────────────────────────────────────────────────────────── */
QDialog {
    background: #ffffff;
}
QDialogButtonBox QPushButton { min-width: 86px; }

/* ─── Inputs ──────────────────────────────────────────────────────────── */
QLineEdit, QDoubleSpinBox {
    background: #F4FCF7;
    border: 1.5px solid #86EFAC;
    border-radius: 8px;
    padding: 6px 10px;
    color: #14532D;
    selection-background-color: #4ADE80;
}
QLineEdit:focus, QDoubleSpinBox:focus {
    border-color: #16A34A;
    background: #ffffff;
}

/* ─── ComboBox ────────────────────────────────────────────────────────── */
QComboBox {
    background: #F4FCF7;
    border: 1.5px solid #86EFAC;
    border-radius: 8px;
    padding: 5px 30px 5px 10px;
    color: #14532D;
    font-weight: 500;
    min-height: 26px;
    selection-background-color: #4ADE80;
}
QComboBox:hover  { border-color: #22C55E; background: #ffffff; }
QComboBox:focus  { border-color: #16A34A; background: #ffffff; }
QComboBox::drop-down {
    border: none;
    width: 24px;
    subcontrol-position: right center;
}
QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}
QComboBox QAbstractItemView {
    background: #ffffff;
    border: 1px solid #86EFAC;
    border-radius: 8px;
    color: #14532D;
    outline: none;
    padding: 4px;
}
QComboBox QAbstractItemView::item {
    padding: 6px 12px;
    color: #14532D;
    background: #ffffff;
    min-height: 26px;
    border-radius: 5px;
}
QComboBox QAbstractItemView::item:selected,
QComboBox QAbstractItemView::item:hover {
    background: #DCFCE7;
    color: #14532D;
}

/* ─── GroupBox ────────────────────────────────────────────────────────── */
QGroupBox {
    background: #F4FCF7;
    border: 1.5px solid #C9E8D3;
    border-radius: 10px;
    margin-top: 14px;
    padding: 10px 8px 8px 8px;
    font-weight: 700;
    color: #166534;
    font-size: 11px;
    letter-spacing: 0.5px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    top: -1px;
    padding: 0 6px;
    background: #F4FCF7;
    color: #166534;
}

/* ─── Tabs ────────────────────────────────────────────────────────────── */
QTabWidget::pane {
    border: 1px solid #C9E8D3;
    border-radius: 0 10px 10px 10px;
    background: #ffffff;
    top: -1px;
}
QTabBar {
    background: transparent;
}
QTabBar::tab {
    background: #E4F0E8;
    color: #166534;
    border: 1px solid #C9E8D3;
    border-bottom: none;
    border-radius: 8px 8px 0 0;
    padding: 7px 18px;
    margin-right: 3px;
    font-size: 12px;
    font-weight: 500;
    min-width: 80px;
}
QTabBar::tab:selected {
    background: #ffffff;
    color: #14532D;
    font-weight: 700;
    border-color: #C9E8D3;
    border-bottom: none;
}
QTabBar::tab:hover:!selected {
    background: #DCFCE7;
    color: #14532D;
}

/* ─── Sliders ─────────────────────────────────────────────────────────── */
QSlider::groove:horizontal {
    height: 4px;
    background: #C9E8D3;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #16A34A;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
    border: 2px solid #ffffff;
}
QSlider::handle:horizontal:hover { background: #15803D; }
QSlider::sub-page:horizontal { background: #22C55E; border-radius: 2px; }

/* ─── Checkboxes ──────────────────────────────────────────────────────── */
QCheckBox {
    color: #14532D;
    spacing: 8px;
    font-weight: 500;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1.5px solid #86EFAC;
    border-radius: 4px;
    background: #F4FCF7;
}
QCheckBox::indicator:hover   { border-color: #16A34A; background: #ffffff; }
QCheckBox::indicator:checked {
    background: #16A34A;
    border-color: #15803D;
    image: none;
}

/* ─── Separator frames ────────────────────────────────────────────────── */
QFrame[frameShape="4"] {
    background: #C9E8D3;
    max-height: 1px;
    border: none;
}

"""
