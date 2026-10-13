import os
import sys


def resource_path(name: str) -> str:
    """Absolute path of a bundled resource (source tree or PyInstaller bundle)."""
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, name)
