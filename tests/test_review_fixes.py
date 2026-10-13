from measurements import Measurement, MeasurementType, flip_points, summary_path


def test_flip_points_horizontal():
    assert flip_points([(10, 20)], "h", 100, 50) == [(90, 20)]


def test_flip_points_vertical():
    assert flip_points([(10, 20)], "v", 100, 50) == [(10, 30)]


def test_summary_path_only_last_extension():
    assert summary_path(r"C:\data.csv\out.csv") == r"C:\data.csv\out_summary.csv"


def test_clear_all_resets_ids(qapp):
    from canvas import ImageCanvas
    c = ImageCanvas()
    c._register(Measurement(id=1, mtype=MeasurementType.DISTANCE, points=[(0, 0), (1, 1)]))
    c._next_id = 5
    c.clear_all()
    assert c._next_id == 1
