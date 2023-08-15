import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton


class TestWindow(QMainWindow):
    label: QLabel
    label_2: QLabel
    push_button: QPushButton

    def __init__(self):
        super(TestWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('./parallel_test.ui', self)  # Load the .ui file
        self.count_1 = 0
        self.count_2 = 0
        self.count_2_flag = True
        self.push_button.clicked.connect(self.count_up)
        self.running = True
        self.show()  # Show the GUI

    def count_up(self):
        self.count_1 += 1
        self.label.setText(f"{self.count_1}")

    def count_up_loop(self):
        n = 90
        while self.running:
            self.count_2 = self.count_2 + 1
            val = 0
            for x in range(n):
                for y in range(n):
                    val += x * y * (y % 2 - 0.5)
            self.label_2.setText(f"{self.count_2}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    p1 = Thread(target=TestWindow.count_up_loop, args=(window,))
    p1.start()
    app.exec_()
    window.running = False
    p1.join()
