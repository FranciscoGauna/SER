from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget
from PyQt5 import uic


# 0 - 1 float values as input
def relative_luminance(r: float, g: float, b: float, alpha: float) -> float:
    R = r / 12.92 if r <= 0.03928 else pow((r + 0.055) / 1.055, 2.4)
    G = g / 12.92 if g <= 0.03928 else pow((g + 0.055) / 1.055, 2.4)
    B = b / 12.92 if b <= 0.03928 else pow((b + 0.055) / 1.055, 2.4)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B


class ColorList:
    def __init__(self, list_widget: QListWidget):
        self.list_widget = list_widget

    def add_item(self, label):
        self.list_widget.addItem(label)
        return self.list_widget.count() - 1

    def clean_list(self):
        self.list_widget.clear()

    def set_color(self, index: int, color: QColor):
        item = self.list_widget.item(index)
        item.setBackground(QBrush(color))
        lum = relative_luminance(*color.getRgbF())
        if lum > 0.179:
            item.setForeground(QBrush(QColor("black")))
        else:
            item.setForeground(QBrush(QColor("white")))