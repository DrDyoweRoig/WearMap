"""Monochrome SVG icons from ./icons, tinted at runtime to match the theme."""
import os

from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer

from paths import resource_path

_cache: dict = {}


def _pixmap(svg: str, size: int) -> QPixmap:
    scale = 2   # render at 2x so icons stay sharp on HiDPI screens
    pm = QPixmap(size * scale, size * scale)
    pm.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pm)
    QSvgRenderer(QByteArray(svg.encode("utf-8"))).render(painter)
    painter.end()
    pm.setDevicePixelRatio(scale)
    return pm


def icon(name: str, color: str, size: int = 24, color_on: str | None = None) -> QIcon:
    """Icon `name` tinted `color`; `color_on` is used for the checked state."""
    key = (name, color, size, color_on)
    if key in _cache:
        return _cache[key]
    path = resource_path(os.path.join("icons", name + ".svg"))
    if not os.path.exists(path):
        return QIcon()
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    ic = QIcon()
    ic.addPixmap(_pixmap(raw.replace("currentColor", color), size),
                 QIcon.Mode.Normal, QIcon.State.Off)
    if color_on:
        ic.addPixmap(_pixmap(raw.replace("currentColor", color_on), size),
                     QIcon.Mode.Normal, QIcon.State.On)
    _cache[key] = ic
    return ic
