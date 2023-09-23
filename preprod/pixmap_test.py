import sys
from threading import Thread
from math import inf, fabs
from typing import List, Tuple

from PyQt5 import uic
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QImage, QColor, QPixmap
from PyQt5.QtWidgets import QGroupBox, QApplication, QDoubleSpinBox, QPushButton, QGraphicsPixmapItem, QGraphicsView, \
    QGraphicsScene

thread_device = QThread()
thread_device.start()


class PixmapText(QGroupBox):
    add_value_button: QPushButton
    value_spin_box: QDoubleSpinBox
    map_view: QGraphicsView

    points: List[float]
    min_val: float
    max_val: float
    hsv_min = 0.1833, 0.18, 1
    hsv_max = 0, 0.85, 1
    width = 10
    height = 10

    def __init__(self):
        super(PixmapText, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('./pixmap_test.ui', self)  # Load the .ui file

        self.points = []
        self.min_val = inf
        self.max_val = -inf

        self.add_value_button.pressed.connect(self.add_value)
        self.zoom_in_button.pressed.connect(self.view_zoom_in)
        self.zoom_out_button.pressed.connect(self.view_zoom_out)
        self.zoom_reset_button.pressed.connect(self.view_zoom_reset)

        self.current_zoom = 1
        self.q_image = QImage(self.width, self.height, QImage.Format_RGB32)
        self.q_image.fill(QColor.fromHsvF(0, 1, 0))
        self.q_pixmap = QPixmap()
        self.q_pixmap.convertFromImage(self.q_image)
        self.g_pixmap = QGraphicsPixmapItem(self.q_pixmap)
        self.scene = QGraphicsScene(0, 0, self.width, self.height)
        self.scene.addItem(self.g_pixmap)
        self.map_view.setScene(self.scene)

        self.show()  # Show the GUI

    def reload_colors(self, value):
        if self.min_val > value:
            self.min_val = value
        if self.max_val < value:
            self.max_val = value

        if self.min_val == self.max_val:
            for i in range(len(self.points)):
                self.set_color(*self.hsv_min, i)

    def calculate_color(self, value) -> Tuple[float, float, float]:
        return 0, 0, 1

    def set_color(self, h: float, s: float, v: float, index=None):
        if index is None:
            index = len(self.points) - 1
        x = index % self.width
        y = int((index - x) / self.width)

        self.q_image.setPixelColor(x, y, QColor.fromHsvF(h, s, v))

    def add_value(self):
        value = self.value_spin_box.value()
        self.points.append(value)
        if self.min_val > value or self.max_val < value:
            self.reload_colors(value)
        else:
            self.set_color(*self.calculate_color(value))
        self.reload_image()

    def reload_image(self):
        self.q_pixmap.convertFromImage(self.q_image)
        self.g_pixmap.setPixmap(self.q_pixmap)
        self.g_pixmap.update()

    def view_zoom_in(self):
        scale = 2
        self.current_zoom *= scale
        self.map_view.scale(scale, scale)

    def view_zoom_out(self):
        scale = 0.5
        self.current_zoom *= scale
        self.map_view.scale(scale, scale)

    def view_zoom_reset(self):
        self.map_view.scale(1 / self.current_zoom, 1 / self.current_zoom)
        self.current_zoom = 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PixmapText()
    app.exec_()
