from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from ui.python.ui_main_screen import Ui_MainScreen
from PyQt5 import QtCore, QtGui
from target import Target

class MainScreen(QMainWindow):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.uic = Ui_MainScreen()
        self.uic.setupUi(self)

        self.targets = [
            Target(40, 0, 0, 0.0),
            Target(40, 30, 0, 0.2),
            Target(40, 60, 240, 0.1),
            Target(40, 90, 180, 0.2),
            Target(40, 135, 0, 0),
            Target(40, 180, 0, 0.4),
            Target(40, 270, 0, 0.1),
            Target(40, 320, 0, 0.1),
        ]

        timer = QtCore.QTimer(self)
        timer.setInterval(20)
        timer.timeout.connect(self.tick)
        timer.start()

    def tick(self):
        self.uic.radar.tick()