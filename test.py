import sys
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget


class Heatmap(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.image = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every second

    def update_data(self):
        self.data = np.random.rand(*self.data.shape)
        self.update_image()

    def get_color(self, value):
        # Map value to a color gradient
        return QColor.fromHsvF(240 * (1 - value), 1, 1)

    def update_image(self):
        data = np.fromfunction(lambda i, j, k: self.get_color(self.data[i][j]).getRgb()[k],
                               (len(self.data), len(self.data[0]), 3), dtype=np.uint8)
        self.image = QImage(data.data, len(self.data[0]), len(self.data), QImage.Format_RGB888)
        self.update()

    def paintEvent(self, event):
        if self.image is None:
            return
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image)

    def sizeHint(self):
        return self.image.size() if self.image else super().sizeHint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = np.random.rand(10, 10)
    heatmap = Heatmap(data)
    heatmap.show()
    sys.exit(app.exec_())
