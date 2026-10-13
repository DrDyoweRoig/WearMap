from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout,
    QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
)

from measurements import Calibration


class CalibrationDialog(QDialog):
    def __init__(self, pixel_length: float, parent=None):
        super().__init__(parent)
        self.pixel_length = pixel_length
        self.setWindowTitle("Set Scale — Calibration")
        self.setMinimumWidth(380)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        info = QLabel(
            f"You drew a reference line of <b>{self.pixel_length:.1f} px</b>.<br>"
            "Enter its real-world length to calibrate the scale."
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.length_edit = QLineEdit("1.0")
        self.length_edit.setValidator(QDoubleValidator(0.0001, 1e12, 8))
        form.addRow("Known length:", self.length_edit)

        self.unit_combo = QComboBox()
        self.unit_combo.addItems([
            "pm",           # picometres
            "nm",           # nanometres
            "\u00c5",       # Ångström
            "\u03bcm",      # micròmetres (micres)
            "mm",           # mil·límetres
            "cm",           # centímetres
            "m",            # metres
            "km",           # quilòmetres
            "in",           # polzades
            "ft",           # peus
            "px",           # píxels (sense calibrar)
        ])
        form.addRow("Unit:", self.unit_combo)
        layout.addLayout(form)

        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet(
            "color: #166534; background: #DCFCE7; border-radius: 4px; padding: 6px;"
        )
        layout.addWidget(self.preview)
        self._refresh_preview()

        self.length_edit.textChanged.connect(self._refresh_preview)
        self.unit_combo.currentTextChanged.connect(self._refresh_preview)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _refresh_preview(self):
        try:
            length = float(self.length_edit.text())
            unit = self.unit_combo.currentText()
            scale = length / self.pixel_length if self.pixel_length > 0 else 0
            self.preview.setText(f"Scale: 1 px \u2192 {scale:.6g} {unit}")
        except (ValueError, ZeroDivisionError):
            self.preview.setText("Enter a valid length above")

    def get_calibration(self) -> Calibration:
        try:
            real_len = float(self.length_edit.text())
        except ValueError:
            real_len = 1.0
        unit = self.unit_combo.currentText()
        return Calibration(
            pixel_length=self.pixel_length,
            real_length=real_len,
            unit=unit,
            is_calibrated=(unit != "px"),
        )


class ScaleBarDialog(QDialog):
    """Dialog to configure the scale bar overlaid on the image."""

    def __init__(self, calibration: "Calibration", parent=None):
        super().__init__(parent)
        self._cal = calibration
        self.setWindowTitle("Scale Bar")
        self.setMinimumWidth(340)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)

        if not self._cal.is_calibrated:
            warn = QLabel(
                "⚠  The image is not calibrated.\n"
                "Use the Calibrate tool (K) first to set the real-world scale."
            )
            warn.setWordWrap(True)
            warn.setStyleSheet("color:#DC2626; background:#FEF2F2; "
                               "border-radius:6px; padding:10px;")
            layout.addWidget(warn)
            bb = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
            bb.accepted.connect(self.reject)
            layout.addWidget(bb)
            return

        info = QLabel(
            f"Calibration: <b>1 px = {self._cal.scale:.4g} {self._cal.unit}</b>"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("color:#166534; background:#DCFCE7; "
                           "border-radius:6px; padding:8px;")
        layout.addWidget(info)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self._spin = QDoubleSpinBox()
        self._spin.setRange(0.001, 1_000_000)
        self._spin.setDecimals(3)
        self._spin.setValue(100.0)
        self._spin.setSuffix(f"  {self._cal.unit}")
        form.addRow(f"Scale bar length ({self._cal.unit}):", self._spin)

        layout.addLayout(form)

        self._preview = QLabel()
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview.setObjectName("muted")
        layout.addWidget(self._preview)
        self._spin.valueChanged.connect(self._update_preview)
        self._update_preview()

        bb = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        bb.accepted.connect(self.accept)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

    def _update_preview(self):
        val = self._spin.value()
        px  = val / self._cal.scale if self._cal.scale > 0 else 0
        self._preview.setText(f"Bar width: {px:.0f} px on the image")

    @property
    def value(self) -> float:
        return self._spin.value()

    @property
    def unit(self) -> str:
        return self._cal.unit


class StriationTypeNamesDialog(QDialog):
    """Dialog to rename, add and remove striation types."""

    def __init__(self, names: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rename / Add Striation Types")
        self.setMinimumWidth(360)
        self.setModal(True)
        # Work with a sorted copy; keys are consecutive ints starting at 1
        self._names = {k: v for k, v in sorted(names.items())}
        self._edits: dict[int, QLineEdit] = {}
        self._form_widget = QWidget()
        self._form = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 16, 20, 16)

        info = QLabel(
            "Name each striation type. Use keyboard shortcuts 1 / 2 / 3 … "
            "to assign types to selected measurements."
        )
        info.setWordWrap(True)
        info.setObjectName("muted")
        layout.addWidget(info)

        layout.addWidget(self._form_widget)
        self._rebuild_form()

        btn_row = QHBoxLayout()
        add_btn = QPushButton("+ Add type")
        add_btn.clicked.connect(self._add_type)
        rem_btn = QPushButton("− Remove last")
        rem_btn.clicked.connect(self._remove_last)
        btn_row.addWidget(add_btn)
        btn_row.addWidget(rem_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        layout.addWidget(btns)

    def _rebuild_form(self):
        # Clear old widgets
        old_layout = self._form_widget.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            QWidget().setLayout(old_layout)  # detach

        from PyQt6.QtWidgets import QFormLayout
        form = QFormLayout(self._form_widget)
        form.setSpacing(6)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        self._edits = {}
        for k in sorted(self._names):
            edit = QLineEdit(self._names[k])
            edit.setPlaceholderText(f"Type {k} name…")
            form.addRow(f"Type {k}  [{k}]:", edit)
            self._edits[k] = edit

    def _add_type(self):
        self._flush_current()
        next_k = max(self._names.keys(), default=0) + 1
        self._names[next_k] = f"Type {next_k}"
        self._rebuild_form()

    def _remove_last(self):
        if not self._names:
            return
        self._flush_current()
        last_k = max(self._names.keys())
        if last_k <= 1:
            return   # keep at least one type
        del self._names[last_k]
        self._edits.pop(last_k, None)
        self._rebuild_form()

    def _flush_current(self):
        for k, edit in self._edits.items():
            self._names[k] = edit.text().strip() or f"Type {k}"

    def get_names(self) -> dict:
        self._flush_current()
        return dict(self._names)


class ROIDialog(QDialog):
    """Ask the size of the analysis area in calibrated units (px if uncalibrated)."""

    def __init__(self, unit: str, scale: float, img_w: int, img_h: int, parent=None):
        super().__init__(parent)
        self._scale = scale if scale > 0 else 1.0
        self._img_w, self._img_h = img_w, img_h
        self.setWindowTitle("Analysis Area")
        self.setMinimumWidth(340)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(QLabel(
            "Set the size of the rectangular analysis area.<br>"
            "Afterwards drag it into place on the image and resize it with its handles."
        ))
        form = QFormLayout()
        self.w_spin = QDoubleSpinBox()
        self.h_spin = QDoubleSpinBox()
        for sp, full in ((self.w_spin, img_w), (self.h_spin, img_h)):
            sp.setDecimals(4)
            sp.setRange(0.0001, 1e12)
            sp.setSuffix(f" {unit}")
            sp.setValue(full * self._scale / 3)
            sp.valueChanged.connect(self._validate)
        form.addRow("Width:", self.w_spin)
        form.addRow("Height:", self.h_spin)
        layout.addLayout(form)
        self.hint = QLabel(
            f"Image size: {img_w * self._scale:.4g} \u00d7 {img_h * self._scale:.4g} {unit}"
        )
        layout.addWidget(self.hint)
        self.btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.btns.accepted.connect(self.accept)
        self.btns.rejected.connect(self.reject)
        layout.addWidget(self.btns)
        self._validate()

    def get_size_px(self):
        return self.w_spin.value() / self._scale, self.h_spin.value() / self._scale

    def _validate(self):
        w, h = self.get_size_px()
        ok = 0 < w <= self._img_w and 0 < h <= self._img_h
        self.btns.button(QDialogButtonBox.StandardButton.Ok).setEnabled(ok)
        self.hint.setStyleSheet("" if ok else "color: #DC2626;")


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Wearmap")
        self.setMinimumWidth(400)
        self.setModal(True)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("<h2 style='color:#14532D;'>Wearmap</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        body = QLabel(
            "<b>Version 1.0.0</b><br><br>"
            "Image analysis tool for dental wear research.<br><br>"
            "<b>Features:</b><br>"
            "\u2022 Distance, area and angle measurements<br>"
            "\u2022 Object counting &amp; pit marking<br>"
            "\u2022 Puech wear classification<br>"
            "\u2022 Scale calibration<br>"
            "\u2022 Excel / CSV export<br><br>"
            "Keyboard shortcuts: <b>S</b>=Select &nbsp; <b>D</b>=Distance<br>"
            "<b>A</b>=Area &nbsp; <b>G</b>=Angle &nbsp; <b>C</b>=Count &nbsp; <b>P</b>=Pits<br>"
            "<b>K</b>=Calibrate &nbsp; <b>L</b>=Labels"
        )
        body.setAlignment(Qt.AlignmentFlag.AlignCenter)
        body.setWordWrap(True)
        layout.addWidget(body)

        btn = QPushButton("Close")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
