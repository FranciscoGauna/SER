import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from lantz import Feat
from lantz.core.driver import Base
from lantz.qt import Frontend, Backend
from lantz.qt.connect import connect_feat


class TestFrontend(Frontend):
    gui = (".", "lantz_test_front.ui")

    def __init__(self, backend):
        super().__init__(backend=backend)
        connect_feat(self.widget.spinBox, backend, "value")
        self.widget.pushButton.clicked.connect(self.add_1)

    def add_1(self):
        self.backend.value += 1


class TestBackend(Backend):
    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self._value = 0
        self._value_square = 0

    @Feat
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.value_squared = value ** 2

    @Feat
    def value_squared(self):
        return self._value_square

    @value_squared.setter
    def value_squared(self, value):
        self._value_square = value


class TestWindow(QMainWindow):
    def __init__(self):
        super(TestWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('./lantz_test_main.ui', self)  # Load the .ui file

        self.backend = TestBackend()
        self.frontend = TestFrontend(self.backend)
        self.centralWidget().layout().addWidget(self.frontend)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    app.exec_()
