from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui
from utils.helper import rphi_to_xy

class Radar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.current_a = 0
        self.SPEED_A = 0.1
        self.R_MAX = 250
        self.width = 500
        self.height = 500
        self.center = (250, 250)
        self.signals = []

    def tick(self):
        self.old_w = self.current_a
        self.current_a = (self.current_a + self.SPEED_A) % 360
        
        # Remove old weak signal
        self.signals = list(filter(lambda signal: signal.alpha > 0.01, self.signals))

        # Scan for signals
        for target in self.parent().targets:
            if self.old_w <= target.a <= self.current_a:
                signal = Signal(target.x, target.y)
                self.signals.append(signal)
            target.update()

            for noise in target.noises:
                if self.old_w <= noise.a <= self.current_a:
                    signal = Signal(noise.x, noise.y)
                    self.signals.append(signal)
                noise.update()
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Get painter
        painter = QtGui.QPainter(self)

        # Draw background
        painter.setBrush(QtGui.QColor(0, 0, 0))
        painter.drawEllipse(QtCore.QPointF(*self.center), self.R_MAX, self.R_MAX)

        # Draw landmark
        painter.setPen(QtGui.QColor(127, 127, 127))

        for phi in [0, 45, 90, 135, 180, 225, 270, 315]:
            p2 = rphi_to_xy(self.R_MAX, phi)
            painter.drawLine(self.center[0], self.center[1], self.center[0] + p2[0], self.center[0] + p2[1])

        painter.setBrush(QtCore.Qt.NoBrush)
        for r in [50, 100, 150, 200]:
            painter.drawEllipse(QtCore.QPointF(*self.center), r, r)

        # Draw rotating line
        p2 = rphi_to_xy(self.R_MAX, self.current_a)
        painter.setPen(QtGui.QColor(0, 255, 0))
        painter.drawLine(self.center[0], self.center[1], self.center[0] + p2[0], self.center[0] + p2[1])

        # Draw signals
        for signal in self.signals:
            painter.setPen(QtGui.QColor(0, 255, 0, 255 * signal.alpha))
            painter.drawRect(self.center[0] + signal.x, self.center[1] + signal.y, 1, 1)
            signal.update()

        return super().paintEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        print(a0.pos())
        return super().mousePressEvent(a0)

class Signal():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.alpha = 1
        self.FADING_RATE = 0.999

    def update(self):
        self.alpha *= self.FADING_RATE