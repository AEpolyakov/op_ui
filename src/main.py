import sys
import time
import logging

from PyQt6.QtWidgets import QApplication

from my_logger import init_logger
from uart import init_uart
from window import MainWindow




def main():
    init_logger()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

    # uart = init_uart()
    # while True:
    #     logging.info('start')
    #     uart.write(b'Hello World')
    #     time.sleep(.2)
    #     data = uart.readline().decode('utf-8')
    #     logging.info(f'read data {data}')


if __name__ == '__main__':
    main()
