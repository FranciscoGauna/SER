import sys
import random
import matplotlib
import numpy as np
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QSpinBox

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets, uic

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Colormap


class HSVMapper(Colormap):

    def __init__(self, hsv_min=(0.1833, 0.18, 1), hsv_max=(0, 0.85, 1)):
        super().__init__("HSVMapper")
        self.hsv_min = hsv_min
        self.hsv_delta = np.subtract(hsv_max, hsv_min)

    def __call__(self, X: float | np.ndarray, alpha: float | None = ..., bytes: bool = False) \
            -> tuple[float, float, float, float] | np.ndarray:

        rgb_value = []

        xa = np.array(X, copy=True)
        if not xa.dtype.isnative:
            # Native byteorder is faster.
            xa = xa.byteswap().view(xa.dtype.newbyteorder())
        if xa.dtype.kind == "i":
            xa /= self.N

        if np.iterable(xa):
            for x in xa:
                hsv = self.hsv_delta * x + self.hsv_min
                rgba = QColor.fromHsvF(*hsv).getRgb()
                if not bytes:
                    rgba = np.divide(rgba, 255)
                rgb_value.append(rgba)
            if len(rgb_value) == 1:
                rgb_value = rgb_value[0]
            else:
                rgb_value = np.array(rgb_value)
        else:
            hsv = self.hsv_delta * xa + self.hsv_min
            rgb_value = QColor.fromHsvF(*hsv).getRgb()
            if not bytes:
                rgb_value = np.divide(rgb_value, 255)

        return rgb_value


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)




class MainWindow(QtWidgets.QGroupBox):
    value_spin_box: QSpinBox

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('./matplotlib_test.ui', self)  # Load the .ui file
        self.add_value_button.pressed.connect(self.update_plot)

        self.canvas = MplCanvas(self, width=10, height=10, dpi=100)
        self.layout().addWidget(self.canvas, 0, 1)
        self.chart_width = 10
        self.data = []
        self.points = []

        self.scalar = ScalarMappable(cmap=HSVMapper())
        self.canvas.figure.colorbar(self.scalar, ax=self.canvas.axes)
        self.update_plot()

        self.show()

    def index(self, x, y):
        return x + (y * self.chart_width)

    def update_plot(self):
        self.canvas.axes.cla()  # Clear the canvas.
        self.data.append(self.value_spin_box.value())
        self.scalar.norm.autoscale(self.data)
        self.points = []
        for x in range(self.chart_width):
            self.points.append([])
            for y in range(self.chart_width):
                if self.index(x, y) < len(self.data):
                    self.points[-1].append(self.scalar.to_rgba(self.data[self.index(x, y)]))
                else:
                    self.points[-1].append((0, 0, 0, 1))

        self.map_plot = self.canvas.axes.imshow(self.points)
        # Trigger the canvas to update and redraw.
        self.canvas.draw()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
