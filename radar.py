import numpy as np
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget
import cv2

import constant as C
from option import Option
from util import P, P_revert, R, dist, rphi_to_xy, gaussian_kernel_2d, vectorized_xy_to_rphi, CFARDetector1D
from constant import A_RES, R_RES, GM_TRACE_LENGTH

class Radar(QWidget):
    """Base class"""

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.a = 0
        self.tracking_boxes = []
    
        # Load map image
        self.map = cv2.imread("assets/map.png", cv2.IMREAD_GRAYSCALE)
        if self.map.shape != (C.HEIGHT, C.WIDTH):
            raise Exception(f"The map image must be a binary image with a size of {C.HEIGHT}x{C.WIDTH}")

    def tick(self):
        self.a = (self.a + C.DELTA_A) % 360

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        # Get painter
        painter = QtGui.QPainter(self)

        # Draw background
        painter.setBrush(QtGui.QColor(0, 0, 0))
        painter.drawEllipse(QtCore.QPointF(*P(0, 0)), R(C.R_MAX), R(C.R_MAX))

        # Draw ground
        image_data = np.full(shape=(C.HEIGHT, C.WIDTH, 4), fill_value=0, dtype=np.uint8)
        def myfunc(i, j):
            i, j = P_revert(i, j)
            return i ** 2 + j ** 2 < C.R_MAX ** 2
        mask = np.fromfunction(myfunc, shape=(C.HEIGHT, C.WIDTH))
        mask &= (self.map == 255)
        image_data[mask] = (50, 168, 82, 200)
        image = QtGui.QImage(image_data, image_data.shape[0], image_data.shape[1], QtGui.QImage.Format_RGBA8888)
        painter.drawImage(self.rect(), image)
        
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

    def draw_tracking_boxes(self, painter):
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
        
################################################################################################
####################################### Left radar #############################################

class LeftRadar(Radar):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.tracking_boxes = []
        self.mat = np.zeros(shape=(A_RES, R_RES))

        # Indices conversion
        Y, X = np.indices((C.HEIGHT, C.WIDTH))
        X2, Y2 = P_revert(X, Y)
        R, A = vectorized_xy_to_rphi(X2, Y2)
        self.R, self.A = R.astype(int), A.astype(int)
        self.R[self.R >= 100] = 100

    def tick(self):
        super().tick()
        
        # Create gradient mask
        a = int(self.a)
        L = GM_TRACE_LENGTH
        stick = np.zeros(shape=(A_RES,))
        stick[np.arange(a-L, a) % A_RES] = np.linspace(0.99, 1, num=L)
        gradient_mask = np.tile(stick.reshape(A_RES, 1), (1, R_RES))
        self.mat *= gradient_mask

        # Generate new row of signal (noise)
        noise = np.random.rand(R_RES)
        self.mat[a] = noise * 0.3

        for target in self.parent().targets:
            if target == None: 
                continue

            # If target radar's azimuth go through target 
            if self.a - C.DELTA_A <= target.a < self.a and target.r <= C.R_MAX:
                # Add some signal in target position
                signal = gaussian_kernel_2d(3, 5, 0, 1)
                self.mat[np.arange(a - 2, a + 3) % A_RES, int(target.r) - 1:int(target.r) + 2] += signal
                self.mat = self.mat.clip(0,1)

                # Tracking box
                if target == self.parent().tracking_target:
                    # Create new tracking box
                    self.tracking_boxes.append(TrackingBox(target.x, target.y))
                    # Update status UI
                    index = self.parent().targets.index(target)
                    self.parent().stui[index]['r'].setText(f"{target.r:.2f}")
                    self.parent().stui[index]['a'].setText(f"{target.a:.2f}")
                    self.parent().stui[index]['dir'].setText(f"{target.dir:.2f}")
                    self.parent().stui[index]['v'].setText(f"{target.v:.2f}")
            # Update target
            target.tick()

        if Option.enable_CFAR:
            self.mat[a] = CFARDetector1D(self.mat[a], Option.pfa, Option.train_size, Option.guard_size)

        # Repaint
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        super().paintEvent(a0)

        # Get painter
        painter = QtGui.QPainter(self)

        # Draw signal in matrix
        image_data = np.full(shape=(C.HEIGHT, C.WIDTH, 4), fill_value=0, dtype=np.uint8)
        image_data[:, :, 1] = 255
        tmp_mat = np.zeros(shape=(A_RES, R_RES + 1))
        tmp_mat[:,:-1] = self.mat
        image_data[:, :, 3] = 255 * tmp_mat[self.A, self.R]
        image = QtGui.QImage(image_data, image_data.shape[0], image_data.shape[1], QtGui.QImage.Format_RGBA8888)
        painter.drawImage(self.rect(), image)

        # Draw tracking boxes
        self.draw_tracking_boxes(painter)

class TrackingBox():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.W = 10
        self.H = 10
        self.alpha = 1
        self.FADING_RATE = 0.996

    def tick(self):
        self.alpha *= self.FADING_RATE
        self.H *= self.FADING_RATE
        self.W *= self.FADING_RATE

################################################################################################
####################################### Right radar #############################################

class RightRadar(Radar):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.a = 0 # azimuth
        # where to save Trace objects of targets.
        # self.traces[target_1] is the Trace object of target_1
        self.traces = {} 
    

    def tick(self):
        # Calculate delta_a and increase azimuth
        delta_a = 360 * C.TICK_INTERVAL / C.ROTATE_PERIOD
        self.a = (self.a + delta_a) % 360

        # For each target
        for target in self.parent().targets:
            # If target is not created, skip
            if target == None:
                continue
            
            # If target in delta_a area
            if self.a - delta_a <= target.a < self.a and target.r <= C.R_MAX:
                # Create a trace for target if not already existed
                if target not in self.traces:
                    self.traces[target] = Trace(target)
                
                # Update trace
                self.traces[target].update()

                # Tracking box
                if target == self.parent().tracking_target:
                    # Create new tracking box
                    self.tracking_boxes.append(TrackingBox(target.x, target.y))

        # Repaint
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

        # Draw tracking boxes
        self.draw_tracking_boxes(painter)

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
        # Simulate observing target's position 
        observe_x = self.target.x + C.MEASUREMENT_NOISE * np.random.rand()
        observe_y = self.target.y + C.MEASUREMENT_NOISE * np.random.rand()

        # Predict and Update Kalman Filter
        z = np.array([observe_x, observe_y])
        self.kalman_filter.predict()
        self.kalman_filter.update(z)

        # Get the prediction
        pred_pos_x = self.kalman_filter.x[0][0]
        pred_pos_y = self.kalman_filter.x[1][0]
        
        # Save position to history
        self.history.append({
            "actual": (self.target.x, self.target.y),
            "observe": (observe_x, observe_y), 
            "predict": (pred_pos_x, pred_pos_y)
        })