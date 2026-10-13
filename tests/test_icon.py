import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

SIZES = {(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)}


def test_ico_has_all_sizes(tmp_path):
    from make_icon import build_ico
    dst = tmp_path / "x.ico"
    build_ico(os.path.join(ROOT, "logo.png"), str(dst))
    assert Image.open(dst).ico.sizes() == SIZES


def test_repo_logo_ico_has_all_sizes():
    assert Image.open(os.path.join(ROOT, "logo.ico")).ico.sizes() == SIZES
