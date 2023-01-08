from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui
from util import rphi_to_xy, dist, xy_to_rphi
import numpy as np
from noise import Noise
from constant import R_MAX, CENTER_GROUND_RADIUS, TICK_INTERVAL, ROTATE_PERIOD
from option import Option

WIDTH = 500
HEIGHT = 500
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

SCALE = 2.2
SIGNAL_PARTICLE_BASE_SIZE = 3
SIGNAL_POWER_FOR_TARGET = 1
SIGNAL_POWER_FOR_NOISE = 0.1
NOISE_RATIO = 0.1
PICKING_DISTANCE_THRESHOLD = 10

def P(x, y):
    """
    Apply reference system for x, y (for painting)
    """
    x = CENTER_X + SCALE * x
    y = CENTER_Y - SCALE * y
    return x, y

def R(r):
    """
    Apply reference system for radius (for painting)
    """
    return SCALE * r


class Radar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.a = 0
        self.signals = []
        self.noises = self.gen_noises()
        self.tracking_boxes = []
    
    def gen_noises(self):
        noises = []
        N = 1000
        X = np.random.uniform(-R_MAX, R_MAX, size=N)
        Y = np.random.uniform(-R_MAX, R_MAX, size=N)
        Dir = np.random.randint(0, 360, size=N)
        V = np.random.randn(N) * 0.01
        for i in range(N):
            r, a = xy_to_rphi(X[i], Y[i])
            dir = Dir[i]
            v = V[i]
            noises.append(Noise(r, a, dir, v))
        return noises

    def tick(self):
        delta_a = 360 * TICK_INTERVAL / ROTATE_PERIOD
        self.a = (self.a + delta_a) % 360
        
        # Remove old weak signal
        self.signals = list(filter(lambda signal: signal.alpha > 0.1, self.signals))

        # Remove old weak tracking boxes
        self.tracking_boxes = list(filter(lambda t: t.alpha > 0.01, self.tracking_boxes))

        # Scan for signals
        for target in self.parent().targets:
            if target == None: 
                continue

            if self.a - delta_a <= target.a < self.a and target.r <= R_MAX:
                p = SIGNAL_POWER_FOR_TARGET + np.random.randn() * NOISE_RATIO
                signal = Signal(target.x, target.y, p)
                self.signals.append(signal)
                # Tracking box
                if target == self.parent().tracking_target:
                    self.tracking_boxes.append(TrackingBox(target.x, target.y))
                    index = self.parent().targets.index(target)
                    self.parent().stui[index]['r'].setText(f"{target.r:.2f}")
                    self.parent().stui[index]['a'].setText(f"{target.a:.2f}")
                    self.parent().stui[index]['dir'].setText(f"{target.dir:.2f}")
                    self.parent().stui[index]['v'].setText(f"{target.v:.2f}")
            target.tick()

            for noise in target.noises:
                if not Option.cfar and self.a - delta_a <= noise.a < self.a and noise.r <= R_MAX:
                    p = SIGNAL_POWER_FOR_NOISE + np.random.randn() * NOISE_RATIO
                    signal = Signal(noise.x, noise.y, p)
                    self.signals.append(signal)
                noise.tick()

        for noise in self.noises:
            if not Option.cfar and self.a - delta_a <= noise.a < self.a and noise.r <= R_MAX:
                p = SIGNAL_POWER_FOR_NOISE + np.random.randn() * NOISE_RATIO
                signal = Signal(noise.x, noise.y, p)
                self.signals.append(signal)
            noise.tick()
        
        self.update()



    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Get painter
        painter = QtGui.QPainter(self)

        # Draw background
        painter.setBrush(QtGui.QColor(0, 0, 0))
        painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(R_MAX), R(R_MAX))

        # Draw ground
        painter.setBrush(QtGui.QColor(0, 255, 0, 200))
        painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(CENTER_GROUND_RADIUS), R(CENTER_GROUND_RADIUS))

        ## Draw landmark
        # Draw azimuth landmark
        painter.setPen(QtGui.QColor(127, 127, 127))
        for phi in [0, 45, 90, 135, 180, 225, 270, 315]:
            p2 = rphi_to_xy(R_MAX, phi)
            x1, y1 = P(0, 0)
            x2, y2 = P(p2[0], p2[1])
            painter.drawLine(x1, y1, x2, y2)
        # Draw azimuth marker
        painter.setPen(QtGui.QColor(0, 0, 0))
        for phi in np.arange(0, 360, 15):
            p2 = rphi_to_xy(R_MAX + 8, phi)
            x2, y2 = P(p2[0] - 4, p2[1] - 2)
            painter.drawText(x2, y2, f"{phi}")
        # Draw radius landmark
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QColor(127, 127, 127))
        for r in [25, 50, 75]:
            painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(r), R(r))

        # Draw rotating line
        p2 = rphi_to_xy(R_MAX, self.a)
        painter.setPen(QtGui.QColor(0, 255, 0))
        x1, y1 = P(0, 0)
        x2, y2 = P(p2[0], p2[1])
        painter.drawLine(x1, y1, x2, y2)

        # Draw signals
        painter.setPen(QtCore.Qt.NoPen)
        for signal in self.signals:
            color = QtGui.QColor(0, 255, 0, 255 * signal.alpha)
            painter.setBrush(color)
            x, y = P(signal.x, signal.y)
            s = signal.p * SIGNAL_PARTICLE_BASE_SIZE
            painter.drawEllipse(QtCore.QPointF(x, y), s, s)
            signal.tick()

        # Draw tracking boxes
        painter.setBrush(QtCore.Qt.NoBrush)
        for tracking_box in self.tracking_boxes:
            color = QtGui.QColor(255, 255, 0, 255 * tracking_box.alpha)
            painter.setPen(color)
            x, y = P(tracking_box.x - tracking_box.W // 2, tracking_box.y + tracking_box.H // 2)
            w, h = R(tracking_box.W), R(tracking_box.H)
            painter.drawRect(x, y, w, h)
            tracking_box.tick()

        return super().paintEvent(a0)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        for target in self.parent().targets:
            if target == None:
                continue
            x1, y1 = P(target.x, target.y)
            x0, y0 = a0.x(), a0.y()
            if dist(x0, y0, x1, y1) < PICKING_DISTANCE_THRESHOLD:
                self.parent().tracking_target = target
                print("Set tracking target")
                break
        else:
            if self.parent().tracking_target != None:
                self.parent().tracking_target = None
                print("Unset tracking target")
        return super().mousePressEvent(a0)

class Signal():
    def __init__(self, x, y, p) -> None:
        self.x = x
        self.y = y
        self.p = p # power of signal
        self.alpha = 1
        self.FADING_RATE = 0.99

    def tick(self):
        self.alpha *= self.FADING_RATE

class TrackingBox():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.W = 10
        self.H = 10
        self.alpha = 1
        self.FADING_RATE = 0.99

    def tick(self):
        self.alpha *= self.FADING_RATE
