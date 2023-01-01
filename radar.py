from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui
from utils.helper import rphi_to_xy, dist
import numpy as np

WIDTH = 600
HEIGHT = 600
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

def P(x, y):
    """
    Apply reference system
    """
    x = CENTER_X + x
    y = CENTER_Y - y
    return x, y

class Radar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.current_a = 0
        self.SPEED_A = 1
        self.R_MAX = 250
        self.DIST_THRESH = 30
        self.signals = []
        self.tracking_boxes = []

    def tick(self):
        self.old_w = self.current_a
        self.current_a = (self.current_a + self.SPEED_A) % 360
        
        # Remove old weak signal
        self.signals = list(filter(lambda signal: signal.alpha > 0.01, self.signals))

        # Remove old weak tracking boxes
        self.tracking_boxes = list(filter(lambda t: t.alpha > 0.01, self.tracking_boxes))

        # Scan for signals
        for target in self.parent().targets:
            if target == None: 
                continue

            if self.old_w <= target.a <= self.current_a:
                signal = Signal(target.x, target.y)
                self.signals.append(signal)
                if target == self.parent().tracking_target:
                    self.tracking_boxes.append(TrackingBox(target.x, target.y))
                    index = self.parent().targets.index(target)
                    self.parent().stui[index]['r'].setText(f"{target.r:.2f}")
                    self.parent().stui[index]['a'].setText(f"{target.a:.2f}")
                    self.parent().stui[index]['dir'].setText(f"{target.dir:.2f}")
                    self.parent().stui[index]['v'].setText(f"{target.v:.2f}")
            target.update()

            for noise in target.noises:
                if not self.parent().cfar_on and self.old_w <= noise.a <= self.current_a:
                    signal = Signal(noise.x, noise.y)
                    self.signals.append(signal)
                noise.update()
        self.update()



    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Get painter
        painter = QtGui.QPainter(self)

        # Draw background
        painter.setBrush(QtGui.QColor(0, 0, 0))
        painter.drawEllipse(QtCore.QPointF(*P(0, 0)), self.R_MAX, self.R_MAX)

        # Draw landmark

        painter.setPen(QtGui.QColor(127, 127, 127))
        for phi in [0, 45, 90, 135, 180, 225, 270, 315]:
            p2 = rphi_to_xy(self.R_MAX, phi)
            x1, y1 = P(0, 0)
            x2, y2 = P(p2[0], p2[1])
            painter.drawLine(x1, y1, x2, y2)

        painter.setPen(QtGui.QColor(0, 0, 0))
        for phi in np.arange(0, 360, 15):
            # marker
            p2 = rphi_to_xy(self.R_MAX + 20, phi)
            x2, y2 = P(p2[0] - 8, p2[1] - 5)
            painter.drawText(x2, y2, f"{phi}")

        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QColor(127, 127, 127))
        for r in [50, 100, 150, 200]:
            painter.drawEllipse(QtCore.QPointF(*P(0, 0)), r, r)

        # Draw rotating line
        p2 = rphi_to_xy(self.R_MAX, self.current_a)
        painter.setPen(QtGui.QColor(0, 255, 0))
        x1, y1 = P(0, 0)
        x2, y2 = P(p2[0], p2[1])
        painter.drawLine(x1, y1, x2, y2)

        # Draw signals
        for signal in self.signals:
            color = QtGui.QColor(0, 255, 0, 255 * signal.alpha)
            x, y = P(signal.x, signal.y)
            w, h = 3, 3
            painter.fillRect(x, y, w, h, color)
            signal.update()

        # Draw tracking boxes
        for tracking_box in self.tracking_boxes:
            color = QtGui.QColor(255, 255, 0, 255 * tracking_box.alpha)
            painter.setPen(color)
            x, y = P(tracking_box.x - tracking_box.W // 2, tracking_box.y + tracking_box.H // 2)
            w, h = tracking_box.W, tracking_box.H
            painter.drawRect(x, y, w, h)
            tracking_box.update()

        return super().paintEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        for target in self.parent().targets:
            if target == None:
                continue
            x1, y1 = P(target.x, target.y)
            x0, y0 = a0.x(), a0.y()
            if dist(x0, y0, x1, y1) < self.DIST_THRESH:
                self.parent().tracking_target = target
                print("Set tracking target")
                break
        else:
            if self.parent().tracking_target != None:
                self.parent().tracking_target = None
                print("Unset tracking target")
        return super().mousePressEvent(a0)

class Signal():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.alpha = 1
        self.FADING_RATE = 0.99

    def update(self):
        self.alpha *= self.FADING_RATE

class TrackingBox():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.W = 50
        self.H = 50
        self.alpha = 1
        self.FADING_RATE = 0.99

    def update(self):
        self.alpha *= self.FADING_RATE