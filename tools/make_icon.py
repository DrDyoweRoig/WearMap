"""Regenerate logo.ico (16-256 px) from logo.png:  python tools/make_icon.py"""
import os

from PIL import Image

SIZES = [16, 24, 32, 48, 64, 128, 256]


def build_ico(src_png: str, dst_ico: str) -> None:
    img = Image.open(src_png).convert("RGBA")
    side = max(img.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    base = canvas.resize((256, 256), Image.LANCZOS)
    base.save(dst_ico, format="ICO", sizes=[(s, s) for s in SIZES])


if __name__ == "__main__":
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    build_ico(os.path.join(root, "logo.png"), os.path.join(root, "logo.ico"))
