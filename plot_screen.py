from PyQt5.QtWidgets import QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from util import P

# main window
# which inherits QDialog
class PlotScreen(QDialog):
    # constructor
    def __init__(self, navigator):
        super().__init__()
        self.setWindowTitle("Kalman Filter plot")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
  
  
    def update(self, traces):  
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.invert_yaxis()
        
        data = dict()
        for target, trace in traces.items():
            data[target] = {
                "actual": [],
                "predict": [],
                "observe": []
            }
            for h in trace.history:
                x, y = P(*h['actual'])
                data[target]['actual'].append((x, y))
            for h in trace.history:
                x, y = P(*h['predict'])
                data[target]['predict'].append((x, y))
            for h in trace.history:
                x, y = P(*h['observe'])
                data[target]['observe'].append((x, y))
        
        colors = {
            'actual': 'r',
            'predict': 'g',
            'observe': 'b'
        }
        markers = ['+', '.', 'o', '1']
        for type in ['actual', 'predict', 'observe']:
            for target in data:
                points = data[target][type]
                x, y = list(zip(*points))
                target_ind = list(data.keys()).index(target)
                ax.plot(x, y, label=f"t{target_ind}:{type}", c=colors[type], marker=markers[target_ind])
        ax.legend()
        self.canvas.draw()