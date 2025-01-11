from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QMainWindow
from PyQt6.uic import loadUi

from src.uart import Uart

class BackgroundTask(QThread):

    def __init__(self, buffer, *args, **kwargs):
        super(BackgroundTask, self).__init__(*args, **kwargs)
        self.buffer = buffer

    def run(self):
        uart = Uart()
        while True:
            self.buffer = uart.read_data()
            print(f'read data: {self.buffer}')


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        buffer = b''

        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 800, 600)

        loadUi("./qt.ui", self)



        self.background_task = BackgroundTask(buffer)
        self.background_task.start()


