import sys

from PyQt6.QtWidgets import QApplication

from my_logger import init_logger
from window import MainWindow


def main():
    init_logger()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == '__main__':
    main()
