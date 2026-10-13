"""Backward-compatible entry point; styles live in theme.py."""
from theme import LIGHT, build_qss

MAIN_STYLE = build_qss(LIGHT)
