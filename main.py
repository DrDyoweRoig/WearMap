import sys
import os

if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Wearmap")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Wearmap Project")

    _base = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(_base, "logo.ico")
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)

    window = MainWindow()
    if os.path.exists(icon_path):
        window.setWindowIcon(icon)

    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        window._load(sys.argv[1])

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
