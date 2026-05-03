import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from PySide6.QtWidgets import QApplication
from database.db import init_db
from ui.main_window import MainWindow

def main():
    init_db()
    app = QApplication(sys.argv)

    qss_path = os.path.join(os.path.dirname(__file__), "style", "style.qss")
    with open(qss_path, "r") as f:
        app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
