from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui
from util import rphi_to_xy, dist, xy_to_rphi
import numpy as np
from noise import Noise
from constant import R_MAX, CENTER_GROUND_RADIUS, TICK_INTERVAL, ROTATE_PERIOD
from option import Option
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

WIDTH = 500
HEIGHT = 500
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
SCALE = 2.2

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


class Radar2(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.a = 0
        self.traces = {}
    

    def tick(self):
        delta_a = 360 * TICK_INTERVAL / ROTATE_PERIOD
        self.a = (self.a + delta_a) % 360
        
        '''
        Mỗi mục tiêu sẽ có một trace tương ứng. Mỗi trace sẽ được apply Kalman Filter vào.
        Khi mục tiêu được tạo thì một trace mới được tạo sau khi radar quét qua lần đầu
        Đối với mỗi trace:
            - Append vị trí mới vào trace khi radar quét qua target
        '''
        for target in self.parent().targets:
            if target == None:
                continue

            if self.a - delta_a <= target.a < self.a and target.r <= R_MAX:
                if target not in self.traces:
                    self.traces[target] = Trace(target)
                self.traces[target].update()

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

        # Draw traces
        painter.setPen(QtCore.Qt.NoPen)
        for target, trace in self.traces.items():
            for h in trace.history:
                x, y = P(*h['observe'])
                color = QtGui.QColor(0, 255, 0)
                painter.setBrush(color)
                painter.drawEllipse(QtCore.QPointF(x, y), 2, 2)

                x, y = P(*h['predict'])
                color = QtGui.QColor(255, 0, 255)
                painter.setBrush(color)
                painter.drawEllipse(QtCore.QPointF(x, y), 2, 2)

        return super().paintEvent(a0)

class Trace:
    def __init__(self, target) -> None:
        self.target = target
        self.history = []
        self.kalman_filter = self._init_kalman_filter()
        

    def _init_kalman_filter(self):        
        f = KalmanFilter(dim_x=4, dim_z=2)
    
        # assign initial value for state
        f.x = np.array([[0.],     # position x
                        [0.],     # position y
                        [0.],     # velocity x
                        [0.]])    # velocity y

        # define state transition matrix
        f.F = np.array([[1, 0, 1, 0],
                        [0, 1, 0, 1],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])

        # define measurement function
        f.H = np.array([[1, 0, 0, 0], 
                        [0, 1, 0, 0]])

        # define covariance matrix
        f.P = 1 * np.eye(4)

        # measurement noise
        f.R = 1 * np.eye(2)

        # Process noise
        f.Q = Q_discrete_white_noise(dim=4, dt=1, var=0.13)

        return f

    def update(self):
        z = np.array([self.target.x, self.target.y])
        self.kalman_filter.predict()
        self.kalman_filter.update(z)

        pred_pos_x = self.kalman_filter.x[0][0]
        pred_pos_y = self.kalman_filter.x[1][0]
        
        self.history.append({
            "observe": (self.target.x, self.target.y), 
            "predict": (pred_pos_x, pred_pos_y)
        })