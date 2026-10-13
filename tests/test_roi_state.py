import pytest
from PIL import Image
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtTest import QTest

from measurements import AnalysisROI


@pytest.fixture
def canvas(qapp, tmp_path):
    from canvas import ImageCanvas
    p = tmp_path / "a.png"
    Image.new("RGB", (200, 100), "gray").save(p)
    c = ImageCanvas()
    c.resize(800, 400)
    c.show()
    assert c.load_image(str(p))
    c.resetTransform()
    return c


def test_roi_roundtrip_state(canvas, tmp_path):
    canvas.set_roi(AnalysisROI(10, 10, 50, 40))
    st = canvas.get_state()
    p2 = tmp_path / "b.png"
    Image.new("RGB", (50, 50), "gray").save(p2)
    canvas.load_image(str(p2))
    assert canvas.get_roi() is None
    canvas.load_image(str(tmp_path / "a.png"))
    canvas.restore_state(st)
    assert canvas.get_roi() == AnalysisROI(10, 10, 50, 40)


def test_restore_state_without_roi_key(canvas):
    st = canvas.get_state()
    st.pop("roi", None)
    canvas.restore_state(st)
    assert canvas.get_roi() is None


def test_set_roi_clamps_to_image(canvas):
    canvas.set_roi(AnalysisROI(-20, -20, 900, 900))
    assert canvas.get_roi() == AnalysisROI(0, 0, 200, 100)


def test_remove_roi_emits_none(canvas):
    got = []
    canvas.roi_changed.connect(got.append)
    canvas.set_roi(AnalysisROI(10, 10, 50, 40))
    canvas.set_roi(None)
    assert got[-1] is None and canvas.get_roi() is None


def test_flip_moves_roi(canvas):
    canvas.set_roi(AnalysisROI(10, 5, 20, 10))
    canvas.flip_image("h")
    assert canvas.get_roi() == AnalysisROI(170, 5, 20, 10)


def test_drag_roi_moves_it_without_panning(canvas):
    canvas.set_roi(AnalysisROI(50, 20, 60, 40))
    vp = canvas.viewport()
    start = canvas.mapFromScene(80, 40)
    end = start + QPoint(30, 10)
    QTest.mousePress(vp, Qt.MouseButton.LeftButton, pos=start)
    QTest.mouseMove(vp, end)
    QTest.mouseRelease(vp, Qt.MouseButton.LeftButton, pos=end)
    r = canvas.get_roi()
    assert r.w == 60 and r.h == 40
    assert r.x > 50 and r.y > 20


def test_resize_handle_changes_size(canvas):
    canvas.set_roi(AnalysisROI(50, 20, 60, 40))
    vp = canvas.viewport()
    start = canvas.mapFromScene(110, 60)      # bottom-right corner
    end = start + QPoint(20, 10)
    QTest.mousePress(vp, Qt.MouseButton.LeftButton, pos=start)
    QTest.mouseMove(vp, end)
    QTest.mouseRelease(vp, Qt.MouseButton.LeftButton, pos=end)
    r = canvas.get_roi()
    assert r.x == 50 and r.y == 20 and r.w > 60 and r.h > 40
