import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget

import constant as C
from noise import Noise
from option import Option
from util import P, R, dist, rphi_to_xy, xy_to_rphi

class Radar(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.a = 0
    
    def tick(self):
        self.a = (self.a + C.DELTA_A) % 360

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Get painter
        painter = QtGui.QPainter(self)

        # Draw background
        painter.setBrush(QtGui.QColor(0, 0, 0))
        painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(C.R_MAX), R(C.R_MAX))

        # Draw ground
        painter.setBrush(QtGui.QColor(0, 255, 0, 200))
        painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(C.CENTER_GROUND_RADIUS), R(C.CENTER_GROUND_RADIUS))

        ## Draw landmark
        # Draw azimuth landmark
        painter.setPen(QtGui.QColor(127, 127, 127))
        for phi in [0, 45, 90, 135, 180, 225, 270, 315]:
            p2 = rphi_to_xy(C.R_MAX, phi)
            x1, y1 = P(0, 0)
            x2, y2 = P(p2[0], p2[1])
            painter.drawLine(x1, y1, x2, y2)
        # Draw azimuth marker
        painter.setPen(QtGui.QColor(0, 0, 0))
        for phi in np.arange(0, 360, 15):
            p2 = rphi_to_xy(C.R_MAX + 8, phi)
            x2, y2 = P(p2[0] - 4, p2[1] - 2)
            painter.drawText(x2, y2, f"{phi}")
        # Draw radius landmark
        painter.setBrush(QtCore.Qt.NoBrush)
        painter.setPen(QtGui.QColor(127, 127, 127))
        for r in [25, 50, 75]:
            painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(r), R(r))

        # Draw rotating line
        p2 = rphi_to_xy(C.R_MAX, self.a)
        painter.setPen(QtGui.QColor(0, 255, 0))
        x1, y1 = P(0, 0)
        x2, y2 = P(p2[0], p2[1])
        painter.drawLine(x1, y1, x2, y2)
        
################################################################################################
####################################### Left radar #############################################

class LeftRadar(Radar):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.signals = []
        self.noises = self.gen_noises()
        self.tracking_boxes = []
    
    def gen_noises(self):
        noises = []
        N = 1000
        X = np.random.uniform(-C.R_MAX, C.R_MAX, size=N)
        Y = np.random.uniform(-C.R_MAX, C.R_MAX, size=N)
        Dir = np.random.randint(0, 360, size=N)
        V = np.random.randn(N) * 0.01
        for i in range(N):
            r, a = xy_to_rphi(X[i], Y[i])
            dir = Dir[i]
            v = V[i]
            noises.append(Noise(r, a, dir, v))
        return noises

    def tick(self):
        super().tick()
        
        # Remove old weak signal
        self.signals = list(filter(lambda signal: signal.alpha > 0.1, self.signals))

        # Remove old weak tracking boxes
        self.tracking_boxes = list(filter(lambda t: t.alpha > 0.01, self.tracking_boxes))

        # Scan for signals
        for target in self.parent().targets:
            if target == None: 
                continue

            if self.a - C.DELTA_A <= target.a < self.a and target.r <= C.R_MAX:
                p = C.SIGNAL_POWER_FOR_TARGET + np.random.randn() * C.NOISE_RATIO
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
                if not Option.cfar and self.a - C.DELTA_A <= noise.a < self.a and noise.r <= C.R_MAX:
                    p = C.SIGNAL_POWER_FOR_NOISE + np.random.randn() * C.NOISE_RATIO
                    signal = Signal(noise.x, noise.y, p)
                    self.signals.append(signal)
                noise.tick()

        for noise in self.noises:
            if not Option.cfar and self.a - C.DELTA_A <= noise.a < self.a and noise.r <= C.R_MAX:
                p = C.SIGNAL_POWER_FOR_NOISE + np.random.randn() * C.NOISE_RATIO
                signal = Signal(noise.x, noise.y, p)
                self.signals.append(signal)
            noise.tick()
        
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)

        # Get painter
        painter = QtGui.QPainter(self)

        # Draw signals
        painter.setPen(QtCore.Qt.NoPen)
        for signal in self.signals:
            color = QtGui.QColor(0, 255, 0, 255 * signal.alpha)
            painter.setBrush(color)
            x, y = P(signal.x, signal.y)
            s = signal.p * C.SIGNAL_PARTICLE_BASE_SIZE
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

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        for target in self.parent().targets:
            if target == None:
                continue
            x1, y1 = P(target.x, target.y)
            x0, y0 = a0.x(), a0.y()
            if dist(x0, y0, x1, y1) < C.PICKING_DISTANCE_THRESHOLD:
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

################################################################################################
####################################### Right radar #############################################

class RightRadar(Radar):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.a = 0
        self.traces = {}
    

    def tick(self):
        delta_a = 360 * C.TICK_INTERVAL / C.ROTATE_PERIOD
        self.a = (self.a + delta_a) % 360

        for target in self.parent().targets:
            if target == None:
                continue

            if self.a - delta_a <= target.a < self.a and target.r <= C.R_MAX:
                if target not in self.traces:
                    self.traces[target] = Trace(target)
                self.traces[target].update()

        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)

        # Get painter
        painter = QtGui.QPainter(self)

        # Draw traces
        painter.setPen(QtCore.Qt.NoPen)
        for target, trace in self.traces.items():
            for h in trace.history:
                if Option.show_actual:
                    x, y = P(*h['actual'])
                    color = QtGui.QColor(255, 0, 0)
                    painter.setBrush(color)
                    painter.drawEllipse(QtCore.QPointF(x, y), 1, 1)

                if Option.show_observe:
                    x, y = P(*h['observe'])
                    color = QtGui.QColor(0, 255, 0)
                    painter.setBrush(color)
                    painter.drawEllipse(QtCore.QPointF(x, y), 1, 1)

                if Option.show_predict:
                    x, y = P(*h['predict'])
                    color = QtGui.QColor(255, 255, 255)
                    painter.setBrush(color)
                    painter.drawEllipse(QtCore.QPointF(x, y), 1, 1)

class Trace:
    '''
    Mỗi mục tiêu sẽ có một trace tương ứng. Mỗi trace sẽ được apply Kalman Filter vào.
    Khi mục tiêu được tạo thì một trace mới được tạo sau khi radar quét qua lần đầu
    Đối với mỗi trace:
        - Append vị trí mới vào trace khi radar quét qua target
    '''
    
    def __init__(self, target) -> None:
        self.target = target
        self.history = []
        self.kalman_filter = self._init_kalman_filter()
        

    def _init_kalman_filter(self):        
        f = KalmanFilter(dim_x=4, dim_z=2)
    
        # assign initial value for state
        pos_x = self.target.x + C.MEASUREMENT_NOISE * np.random.rand()
        pos_y = self.target.y + C.MEASUREMENT_NOISE * np.random.rand()
        vel_x = np.random.rand()
        vel_y = np.random.rand()
        f.x = np.array([[pos_x],     # position x
                        [pos_y],     # position y
                        [vel_x],     # velocity x
                        [vel_y]])    # velocity y

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
        f.R = C.MEASUREMENT_NOISE * np.eye(2)

        # Process noise
        f.Q = Q_discrete_white_noise(dim=4, dt=1, var=0.13)

        return f

    def update(self):
        observe_x = self.target.x + C.MEASUREMENT_NOISE * np.random.rand()
        observe_y = self.target.y + C.MEASUREMENT_NOISE * np.random.rand()

        z = np.array([observe_x, observe_y])
        self.kalman_filter.predict()
        self.kalman_filter.update(z)

        pred_pos_x = self.kalman_filter.x[0][0]
        pred_pos_y = self.kalman_filter.x[1][0]
        
        self.history.append({
            "actual": (self.target.x, self.target.y),
            "observe": (observe_x, observe_y), 
            "predict": (pred_pos_x, pred_pos_y)
        })