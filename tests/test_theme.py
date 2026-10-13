import re

from icons import icon
from theme import DARK, LIGHT, build_qss


def test_light_dark_same_keys():
    assert set(LIGHT) == set(DARK)


def test_build_qss_has_no_unresolved_tokens():
    for tokens in (LIGHT, DARK):
        qss = build_qss(tokens)
        assert "$" not in qss
        assert tokens["accent"] in qss
    assert not re.search(r"\$\w+", build_qss(LIGHT))


def test_icon_missing_returns_null(qapp):
    assert icon("nope", "#000000").isNull()


def test_icon_renders_nonempty(qapp):
    pm = icon("open", "#15301F").pixmap(24, 24)
    assert not pm.isNull()
    img = pm.toImage()
    assert any(img.pixelColor(x, y).alpha() > 0
               for x in range(img.width()) for y in range(img.height()))


def test_all_toolbar_icons_exist(qapp):
    for name in ("open", "pan", "distance", "area", "angle", "count", "pits",
                 "calibrate", "zoom-in", "zoom-out", "fit", "labels", "palette",
                 "roi", "export", "image", "prev", "next", "theme"):
        assert not icon(name, "#000000").isNull(), name
