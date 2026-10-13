import pytest

from measurements import (
    AnalysisROI, Calibration, Measurement, MeasurementType, ROI_HEADERS,
    compute_roi_stats, flip_roi, roi_export_row,
)

D = MeasurementType.DISTANCE
UM = "μm"


def dist(i, p0, p1):
    return Measurement(id=i, mtype=D, points=[p0, p1])


def cal_um(scale=1.0):
    return Calibration(pixel_length=1.0, real_length=scale, unit=UM, is_calibrated=True)


def test_contains_inclusive_edges():
    r = AnalysisROI(10, 10, 20, 20)
    assert r.contains((10, 10)) and r.contains((30, 30))
    assert not r.contains((30.1, 20))


def test_midpoint_rule():
    r = AnalysisROI(20, 0, 20, 10)
    s = compute_roi_stats(r, [dist(1, (0, 5), (30, 5))], cal_um(), "Upper", "Right")
    assert s.n_striations == 0          # midpoint x=15 is outside
    s = compute_roi_stats(r, [dist(1, (10, 5), (50, 5))], cal_um(), "Upper", "Right")
    assert s.n_striations == 1          # midpoint x=30 inside, endpoints outside


def test_empty_roi_stats():
    s = compute_roi_stats(AnalysisROI(0, 0, 10, 10), [], cal_um(), "Upper", "Right")
    assert s.mean_len is None and s.sd_len is None
    assert s.n_striations == 0 and s.per_puech == {1: 0, 2: 0, 3: 0, 4: 0}


def test_single_striation_sd_zero():
    s = compute_roi_stats(AnalysisROI(0, 0, 100, 100),
                          [dist(1, (0, 0), (10, 0))], cal_um(), "Upper", "Right")
    assert s.sd_len == 0.0 and s.mean_len == pytest.approx(10.0)


def test_mean_sd_calibrated():
    ms = [dist(1, (0, 0), (10, 0)), dist(2, (0, 5), (20, 5))]
    s = compute_roi_stats(AnalysisROI(0, 0, 100, 100), ms, cal_um(2.0), "Upper", "Right")
    assert s.mean_len == pytest.approx(30.0)
    assert s.sd_len == pytest.approx(14.1421, rel=1e-4)


def test_puech_counts_horizontal():
    s = compute_roi_stats(AnalysisROI(0, 0, 100, 100),
                          [dist(1, (0, 0), (10, 0))], cal_um(), "Upper", "Right")
    assert s.per_puech[1] == 1


def test_density_calibrated():
    ms = [dist(i, (10, 10 + i), (20, 10 + i)) for i in range(5)]
    s = compute_roi_stats(AnalysisROI(0, 0, 1000, 1000), ms, cal_um(), "Upper", "Right")
    assert s.area == pytest.approx(1_000_000) and s.area_unit == UM + "²"
    assert s.density_per_mm2 == pytest.approx(5.0)


def test_density_none_when_uncalibrated():
    s = compute_roi_stats(AnalysisROI(0, 0, 10, 10), [], Calibration(), "Upper", "Right")
    assert s.density_per_mm2 is None and s.area_unit == "px²"


def test_pits_and_count_points_inside():
    m = Measurement(id=1, mtype=MeasurementType.PITS, points=[(1, 1), (5, 5), (50, 50)])
    s = compute_roi_stats(AnalysisROI(0, 0, 10, 10), [m], cal_um(), "Upper", "Right")
    assert s.n_points == 2


def test_clamped_inside_image_min_size():
    assert AnalysisROI(-10, -10, 500, 500).clamped(100, 80) == AnalysisROI(0, 0, 100, 80)
    assert AnalysisROI(10, 10, 0, 0).clamped(100, 80).w == 5.0


def test_flip_roi():
    assert flip_roi(AnalysisROI(10, 5, 20, 10), "h", 200, 100) == AnalysisROI(170, 5, 20, 10)
    assert flip_roi(AnalysisROI(10, 5, 20, 10), "v", 200, 100) == AnalysisROI(10, 85, 20, 10)


def test_export_row_matches_headers():
    roi = AnalysisROI(0, 0, 100, 50)
    s = compute_roi_stats(roi, [dist(1, (0, 0), (10, 0))], cal_um(), "Upper", "Right")
    row = roi_export_row("a.png", roi, s, cal_um())
    assert len(row) == len(ROI_HEADERS) and row[0] == "a.png"
