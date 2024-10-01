from datetime import timedelta

import numpy as np
from typing import Dict, Any, List, Iterable

import matplotlib
from matplotlib.cm import ScalarMappable
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.colors import Colormap
from PyQt5.QtGui import QColor

from src.SER.interfaces.user_interface import ProcessDataUI, FinalDataUI

matplotlib.use('Qt5Agg')


class TwoDMapper(ProcessDataUI, FinalDataUI):
    data: List[tuple[Any, Any, float]]

    def __init__(self, x_variable: tuple[str, str, str], y_variable: tuple[str, str, str],
                 z_variable: tuple[str, str, str], x=0, y=0, parent=None, backend=None):
        super().__init__(x, y, parent, backend)
        self.x_device, self.x_var_name, self.x_display_name = x_variable
        self.y_device, self.y_var_name, self.y_display_name = y_variable
        self.z_device, self.z_var_name, self.z_display_name = z_variable
        self.last_x = 0
        self.last_y = 0

        # The y counter is necessary because we need it to be a consistent shape the figure
        self.y_counter = 0

    def initialize(self):
        self.data = []
        self.canvas = PlotCanvas([[None]])
        self.setCentralWidget(self.canvas)
        self.last_x = 0
        self.last_y = 0
        self.y_counter = 0

    def add_data(self, data: List[Dict[str, Dict[str, Any]]]):
        parsed_matrix: List[List[float | None]] = []

        for datum in data:
            if self.x_device in datum:
                self.last_x = datum[self.x_device][self.x_var_name]

            if self.y_device in datum:
                self.last_y = datum[self.y_device][self.y_var_name]

            if self.z_device in datum:
                self.data.append((self.last_x, self.last_y, float(datum[self.z_device][self.z_var_name])))

        x_set = set(map(lambda tup: tup[0], self.data))
        y_set = set(map(lambda tup: tup[1], self.data))
        parsed_dictionary: Dict[Any, Dict[Any, float | None]] = dict()
        for x in x_set:
            parsed_dictionary[x] = {}
            for y in y_set:
                parsed_dictionary[x][y] = None

        for datum in self.data:
            parsed_dictionary[datum[0]][datum[1]] = datum[2]

        for _, v in parsed_dictionary.items():
            parsed_matrix.append(list(v.values()))
        self.canvas.update_with_data(parsed_matrix)

    def set_data(self, data: List[Dict[str, Dict[str, Any]]]):
        self.initialize()
        self.add_data(data)



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
        if len(list(data)) == 0:
            res.append((0, 0, 0, 1))
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
