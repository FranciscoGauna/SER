import logging

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from lantz.qt import Frontend
from lantz.core.log import LOGGER, log_to_socket, get_logger

log_to_socket(logging.DEBUG, "127.0.0.1", 19996)


class TestDriver(Frontend):
    def __init__(self):
        super().__init__()
        self.logger_name = "lantz.tests"

    def log_shit(self):
        self.log_error("tests")


app = QApplication([])
foo = TestDriver()
foo.log_shit()
app.exit()
