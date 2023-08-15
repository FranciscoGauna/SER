from typing import Union, Generator, List

from PyQt5.QtWidgets import QSpinBox, QApplication
from lantz.core import Feat
from lantz.qt import Frontend, Backend


class PointSelectBackend(Backend):
    """
    This class exists only to utilize the connect_feat function from Lantz.
    """

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self._x_amount = 0
        self._x_init = 0
        self._x_final = 0
        self._y_amount = 0
        self._y_init = 0
        self._y_final = 0

    @Feat
    def x_amount(self):
        return self._x_amount

    @x_amount.setter
    def x_amount(self, val):
        self._x_amount = val

    @Feat
    def x_init(self):
        return self._x_init

    @x_init.setter
    def x_init(self, val):
        self._x_init = val

    @Feat
    def x_final(self):
        return self._x_final

    @x_final.setter
    def x_final(self, val):
        self._x_final = val

    @Feat
    def y_amount(self):
        return self._y_amount

    @y_amount.setter
    def y_amount(self, val):
        self._y_amount = val

    @Feat
    def y_init(self):
        return self._y_init

    @y_init.setter
    def y_init(self, val):
        self._y_init = val

    @Feat
    def y_final(self):
        return self._y_final

    @y_final.setter
    def y_final(self, val):
        self._y_final = val


class PointSelectFrontend(Frontend):
    gui = "point_select.ui"

    def get_runtime_params(self) -> Union[Generator, List]:
        x_delta = (self.backend.x_final - self.backend.x_init) / (self.backend.x_amount - 1)
        y_delta = (self.backend.y_final - self.backend.y_init) / (self.backend.y_amount - 1)

        for x in range(self.backend.x_amount):
            for y in range(self.backend.y_amount):
                yield self.backend.x_init + x * x_delta, self.backend.y_init + y * y_delta
