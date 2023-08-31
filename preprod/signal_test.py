import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton

thread_device = QThread()
thread_device.start()


class TestWindow(QMainWindow):
    label: QLabel
    label_2: QLabel
    push_button: QPushButton

    def __init__(self):
        super(TestWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('./parallel_test.ui', self)  # Load the .ui file
        self.count = 0
        self.push_button.clicked.connect(self.count_up)
        self.show()  # Show the GUI

    def count_up(self):
        self.count += 1
        self.label.setText(f"{self.count}")

    def count_2(self, value):
        self.label_2.setText(f"{value}")


class TestDevice(QObject):
    done = pyqtSignal()

    def __init__(self, main_window: TestWindow):
        super().__init__()
        self.moveToThread(thread_device)
        self.count = 0
        self.main_window: TestWindow = main_window
        self.done.connect(self.next)

    @pyqtSlot()
    def next(self):
        n = 1000
        self.count = self.count + 1
        val = 0
        for x in range(n):
            for y in range(n):
                val += x * y * (y % 2 - 0.5)
        self.main_window.count_2(self.count)
        self.done.emit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    counter = TestDevice(window)
    counter.next()
    app.exec_()
