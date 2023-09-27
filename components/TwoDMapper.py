from datetime import timedelta

import numpy as np
from typing import Dict, Any, List, Iterable

import matplotlib
from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.colors import Colormap
from PyQt5.QtGui import QColor

from src.SER.interfaces.user_interface import ProcessDataUI

matplotlib.use('Qt5Agg')


class TwoDMapper(ProcessDataUI):
    data: List[List[Any]]

    def __init__(self, width_fun, height_fun, x, y, motor_name, value_name: tuple[str, str], parent=None, backend=None):
        super().__init__(x, y, parent, backend)
        self.width_fun = width_fun
        self.height_fun = height_fun
        self.motor_name = motor_name
        self.value_name = value_name
        self.last_value = None

        self.x_counter = 0
        self.y_counter = 0

    def initialize(self):
        self.width = self.width_fun()
        self.height = self.height_fun()
        self.data = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.canvas = PlotCanvas(self.data)
        self.setCentralWidget(self.canvas)

    def set_datum(self, components: Dict[str, Dict[str, Any]]):
        if self.motor_name not in components:
            return

        if self.value_name[0] in components:
            self.last_value = components[self.value_name[0]][self.value_name[1]]

        x = components[self.motor_name]["x"]
        y = components[self.motor_name]["y"]

        if self.x_counter >= self.width:
            self.x_counter = 0
            self.y_counter += 1

        # TODO: remove ugly hack
        time_delta: timedelta = components["timestamp"]["end_time"] - components["timestamp"]["config_start_time"]
        self.data[self.y_counter][self.x_counter] = time_delta.total_seconds()
        self.canvas.update_with_data(self.data)

        self.x_counter += 1


class PlotCanvas(FigureCanvasQTAgg):

    def __init__(self, data, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PlotCanvas, self).__init__(fig)
        self.scalar = ScalarMappable(cmap=HSVMapper())
        self.figure.colorbar(self.scalar, ax=self.axes)
        self.update_with_data(data)

    def color(self, data: Iterable[float | None]):
        res = []
        for datum in data:
            if datum is None:
                res.append((0, 0, 0, 1))
            else:
                res.append(self.scalar.to_rgba(datum))
        return np.array(res)

    def update_with_data(self, data: List[List[float]]):
        npdata = np.array(data)
        if any(npdata.flatten()):
            self.scalar.norm.autoscale(list(filter(lambda x: x is not None, npdata.flatten())))
        color_data = np.vectorize(self.color, signature="(m)->(m, 4)")(npdata)
        self.map_plot = self.axes.imshow(color_data)
        self.draw()


class HSVMapper(Colormap):

    def __init__(self, hsv_min=(0.1833, 0.18, 1.0), hsv_max=(0, 0.85, 1.0)):
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
