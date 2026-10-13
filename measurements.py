import math
import os
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum


def compute_puech(angle_deg: float, jaw: str, side: str) -> int:
    """
    Puech (1983) toothwear directionality from the SPSS script.
    angle_deg : slope_angle() value — signed, in [-90, 90].
    jaw       : 'Upper' or 'Lower'
    side      : 'Right' or 'Left'
    Returns   : 1=horizontal, 2=vertical, 3=mesial, 4=distal
    """
    # Normalise angle to [0, 180] exactly as the SPSS script does
    angle = 180 + angle_deg if angle_deg < 0 else angle_deg
    # SPSS variables: mdx 2=maxilla(Upper) 1=mandible(Lower)
    #                 costat 1=Right  2=Left
    mdx    = 2 if jaw  == "Upper" else 1
    costat = 1 if side == "Right" else 2

    if angle >= 157.5 or angle <= 22.5:
        return 1                          # horizontal
    if 67.5 < angle < 112.5:
        return 2                          # vertical
    if 22.5 < angle <= 67.5:
        # \ diagonal: P3 Mesiodistal when mdx≠costat (Lower-Left OR Upper-Right)
        #             P4 Distomesial when mdx=costat  (Lower-Right OR Upper-Left)
        return 3 if mdx != costat else 4
    if 112.5 <= angle < 157.5:
        # / diagonal: P3 Mesiodistal when mdx=costat  (Lower-Right OR Upper-Left)
        #             P4 Distomesial when mdx≠costat (Lower-Left OR Upper-Right)
        return 3 if mdx == costat else 4
    return 0


def flip_points(points, axis: str, width: float, height: float):
    """Mirror points inside a width x height image. axis: 'h' or 'v'."""
    if axis == "h":
        return [(width - x, y) for x, y in points]
    return [(x, height - y) for x, y in points]


def summary_path(base: str) -> str:
    """Insert '_summary' before the final extension only."""
    root, ext = os.path.splitext(base)
    return f"{root}_summary{ext}"


class MeasurementType(Enum):
    DISTANCE = "Distance"
    AREA = "Area"
    ANGLE = "Angle"
    COUNT = "Count"
    PITS = "Pits"


@dataclass
class Calibration:
    pixel_length: float = 1.0
    real_length: float = 1.0
    unit: str = "px"
    is_calibrated: bool = False

    @property
    def scale(self) -> float:
        return self.real_length / self.pixel_length if self.pixel_length > 0 else 1.0

    def to_real(self, pixels: float) -> float:
        return pixels * self.scale if self.is_calibrated else pixels

    def to_real_area(self, px_area: float) -> float:
        return px_area * (self.scale ** 2) if self.is_calibrated else px_area

    def unit_str(self, is_area: bool = False) -> str:
        u = self.unit if self.is_calibrated else "px"
        return f"{u}\u00b2" if is_area else u


@dataclass
class Measurement:
    id: int
    mtype: MeasurementType
    points: List[Tuple[float, float]] = field(default_factory=list)
    label: str = ""
    color: str = "#22C55E"
    visible: bool = True
    striation_type: int = 0  # 0=unset, 1/2/3 = user-defined types

    def pixel_value(self) -> float:
        if self.mtype == MeasurementType.DISTANCE:
            return self._distance()
        if self.mtype == MeasurementType.AREA:
            return self._area()
        if self.mtype == MeasurementType.ANGLE:
            return self._angle()
        if self.mtype in (MeasurementType.COUNT, MeasurementType.PITS):
            return float(len(self.points))
        return 0.0

    def display_value(self, cal: "Calibration") -> str:
        if self.mtype == MeasurementType.COUNT:
            return f"{len(self.points)} objects"
        if self.mtype == MeasurementType.PITS:
            return f"{len(self.points)} pits"
        pv = self.pixel_value()
        if self.mtype == MeasurementType.ANGLE:
            return f"{pv:.2f}\u00b0"
        if self.mtype == MeasurementType.AREA:
            return f"{cal.to_real_area(pv):.2f} {cal.unit_str(is_area=True)}"
        return f"{cal.to_real(pv):.2f} {cal.unit_str()}"

    def slope_angle(self) -> Optional[float]:
        """Signed angle from horizontal [-90, 90]. Positive = descending right (image Y↓).
        None if not a DISTANCE measurement."""
        if self.mtype != MeasurementType.DISTANCE or len(self.points) < 2:
            return None
        dx = self.points[1][0] - self.points[0][0]
        dy = self.points[1][1] - self.points[0][1]
        if dx == 0 and dy == 0:
            return 0.0
        # Normalise so we always read left→right
        if dx < 0:
            dx, dy = -dx, -dy
        return math.degrees(math.atan2(dy, dx))

    def direction_arrow(self) -> Optional[str]:
        """Unicode arrow that shows the slope direction."""
        angle = self.slope_angle()
        if angle is None:
            return None
        if abs(angle) < 5:
            return "\u2192"    # → horizontal
        if abs(angle) > 85:
            return "\u2193" if angle > 0 else "\u2191"  # ↓ ↑
        return "\u2198" if angle > 0 else "\u2197"      # ↘ ↗

    def slope_display(self) -> Optional[str]:
        """Combined display: arrow + abs angle, e.g. '↘ 45.0°'"""
        angle = self.slope_angle()
        arrow = self.direction_arrow()
        if angle is None or arrow is None:
            return None
        return f"{arrow} {abs(angle):.1f}\u00b0"

    def _distance(self) -> float:
        if len(self.points) < 2:
            return 0.0
        dx = self.points[1][0] - self.points[0][0]
        dy = self.points[1][1] - self.points[0][1]
        return math.sqrt(dx * dx + dy * dy)

    def _area(self) -> float:
        if len(self.points) < 3:
            return 0.0
        pts = self.points
        n = len(pts)
        s = sum(
            pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1]
            for i in range(n)
        )
        return abs(s) / 2.0

    def puech(self, jaw: str, side: str) -> int:
        """Puech wear classification (1–4) based on slope + jaw + side.
        Replicates the SPSS script logic.
        jaw:  'Upper'|'Lower'   side: 'Right'|'Left'
        Returns: 1=horizontal, 2=vertical, 3=mesial, 4=distal, 0=n/a
        """
        a = self.slope_angle()
        if a is None:
            return 0
        return compute_puech(a, jaw, side)

    def _angle(self) -> float:
        if len(self.points) < 3:
            return 0.0
        p1, v, p2 = self.points[0], self.points[1], self.points[2]
        a = (p1[0] - v[0], p1[1] - v[1])
        b = (p2[0] - v[0], p2[1] - v[1])
        dot = a[0] * b[0] + a[1] * b[1]
        ma = math.sqrt(a[0] ** 2 + a[1] ** 2)
        mb = math.sqrt(b[0] ** 2 + b[1] ** 2)
        if ma == 0 or mb == 0:
            return 0.0
        return math.degrees(math.acos(max(-1.0, min(1.0, dot / (ma * mb)))))


# ── Analysis area (ROI) ──────────────────────────────────────────────────

UNIT_TO_MM = {
    "pm": 1e-9, "nm": 1e-6, "Å": 1e-7, "μm": 1e-3, "mm": 1.0,
    "cm": 10.0, "m": 1000.0, "km": 1e6, "in": 25.4, "ft": 304.8,
}


@dataclass
class AnalysisROI:
    """Axis-aligned rectangle in image pixels."""
    x: float
    y: float
    w: float
    h: float

    def contains(self, pt: Tuple[float, float]) -> bool:
        return self.x <= pt[0] <= self.x + self.w and self.y <= pt[1] <= self.y + self.h

    def area_px(self) -> float:
        return self.w * self.h

    def clamped(self, img_w: float, img_h: float, min_size: float = 5.0) -> "AnalysisROI":
        w = min(max(self.w, min_size), img_w)
        h = min(max(self.h, min_size), img_h)
        x = min(max(self.x, 0.0), img_w - w)
        y = min(max(self.y, 0.0), img_h - h)
        return AnalysisROI(x, y, w, h)


def flip_roi(roi: AnalysisROI, axis: str, width: float, height: float) -> AnalysisROI:
    if axis == "h":
        return AnalysisROI(width - roi.x - roi.w, roi.y, roi.w, roi.h)
    return AnalysisROI(roi.x, height - roi.y - roi.h, roi.w, roi.h)


@dataclass
class ROIStats:
    n_striations: int
    per_puech: dict
    mean_len: Optional[float]
    sd_len: Optional[float]
    area: float
    area_unit: str
    density_per_mm2: Optional[float]
    n_points: int


def compute_roi_stats(roi: AnalysisROI, measurements, cal: Calibration,
                      jaw: str, side: str) -> ROIStats:
    lengths = []
    per_puech = {1: 0, 2: 0, 3: 0, 4: 0}
    n_points = 0
    for m in measurements:
        if m.mtype == MeasurementType.DISTANCE and len(m.points) >= 2:
            mid = ((m.points[0][0] + m.points[1][0]) / 2,
                   (m.points[0][1] + m.points[1][1]) / 2)
            if roi.contains(mid):
                lengths.append(cal.to_real(m.pixel_value()))
                p = m.puech(jaw, side)
                if p in per_puech:
                    per_puech[p] += 1
        elif m.mtype in (MeasurementType.COUNT, MeasurementType.PITS):
            n_points += sum(1 for p in m.points if roi.contains(p))
    n = len(lengths)
    mean = sum(lengths) / n if n else None
    if n == 0:
        sd = None
    elif n == 1:
        sd = 0.0
    else:
        sd = math.sqrt(sum((v - mean) ** 2 for v in lengths) / (n - 1))
    area_px = roi.area_px()
    area = cal.to_real_area(area_px)
    density = None
    if cal.is_calibrated and cal.unit in UNIT_TO_MM:
        mm_per_px = cal.scale * UNIT_TO_MM[cal.unit]
        area_mm2 = area_px * mm_per_px ** 2
        density = n / area_mm2 if area_mm2 > 0 else None
    return ROIStats(n, per_puech, mean, sd, area, cal.unit_str(is_area=True),
                    density, n_points)


ROI_HEADERS = ["Image", "Width", "Height", "Unit", "Area", "Striations",
               "P1", "P2", "P3", "P4", "Mean length", "SD length",
               "Density (/mm²)", "Points"]


def roi_export_row(image_name: str, roi: AnalysisROI, stats: ROIStats,
                   cal: Calibration) -> list:
    def f(v, nd=4):
        return "-" if v is None else f"{v:.{nd}f}"
    return [image_name, f(cal.to_real(roi.w)), f(cal.to_real(roi.h)), cal.unit_str(),
            f(stats.area), stats.n_striations,
            stats.per_puech[1], stats.per_puech[2], stats.per_puech[3], stats.per_puech[4],
            f(stats.mean_len), f(stats.sd_len), f(stats.density_per_mm2, 2), stats.n_points]
