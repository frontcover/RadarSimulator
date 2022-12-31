from PyQt5.QtWidgets import QMainWindow, QErrorMessage
from ui.python.ui_main_screen import Ui_MainScreen
from PyQt5 import QtCore, QtGui
from target import Target
import numpy as np

class MainScreen(QMainWindow):
    def __init__(self, navigator):
        super().__init__()
        self.navigator = navigator
        self.uic = Ui_MainScreen()
        self.uic.setupUi(self)

        self.targets = []
        for i in range(5):
            r = np.random.randint(0, 250)
            a = np.random.randint(0, 360)
            v = np.random.rand() * 0.01
            dir = np.random.randint(0, 360)
            self.targets.append(Target(r, a, dir, v))

        timer = QtCore.QTimer(self)
        timer.setInterval(1)
        timer.timeout.connect(self.tick)
        timer.start()

    def tick(self):
        self.uic.radar.tick()
