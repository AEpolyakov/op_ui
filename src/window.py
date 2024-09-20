from PyQt6.QtWidgets import QMainWindow, QPushButton, QTabWidget
from PyQt6.uic import loadUi


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setGeometry(100, 100, 800, 600)

        loadUi("./qt.ui", self)

        # self.tabs = QTabWidget(self)
        # self.tabs.setFixedSize(500, 500)
        # self.tabs.setTabText(1, 'tab1')
        # self.move(10, 10)
        #
        # self.button1 = QPushButton(self)
        # self.button1.setText('b1')
        # self.button1.setCheckable(True)
        # self.button1.clicked.connect(self.the_button_was_clicked)
        # self.button1.setFixedSize(50, 50)
        # self.button1.move(50, 50)
        #
        #
        # self.button2 = QPushButton(self)
        # self.button2.setText('b2')
        # self.button2.setCheckable(True)
        # self.button2.clicked.connect(self.the_button2_was_clicked)
        # self.button2.setFixedSize(50, 50)
        # self.button2.move(50, 150)


    def the_button_was_clicked(self):
        print("Clicked!")

    def the_button2_was_clicked(self):
        print("Clicked2!")