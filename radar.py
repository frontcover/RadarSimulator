from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui
from utils.helper import rphi_to_xy

class Radar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.current_a = 0
        self.SPEED_A = 2
        self.R_MAX = 250
        self.width = 500
        self.height = 500
        self.center = (250, 250)

    def tick(self):
        self.old_w = self.current_a
        self.current_a = (self.current_a + self.SPEED_A) % 360

        for target in self.parent().targets:
            if self.old_w <= target.a <= self.current_a:
                target.alpha = 1
            target.update()

            for noise in target.noises:
                if self.old_w <= noise.a <= self.current_a:
                    noise.alpha = 1
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

        # Draw targets and noises
        for target in self.parent().targets:
            # Draw target
            painter.setPen(QtGui.QColor(0, 255, 0, 255 * target.alpha))
            painter.drawRect(self.center[0] + target.x, self.center[1] + target.y, 3, 3)

            # Draw it's noises
            for noise in target.noises:
                painter.setPen(QtGui.QColor(0, 255, 0, 255 * noise.alpha))
                painter.drawRect(self.center[0] + noise.x, self.center[1] + noise.y, 1, 1)


        return super().paintEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        print(a0.pos())
        return super().mousePressEvent(a0)