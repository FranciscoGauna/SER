from typing import Collection
from logging import getLogger as get_logger

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget
from pimpmyclass.mixins import LogMixin

from .interfaces import Component


### Summary
class MainWindow(QMainWindow, LogMixin):
    central_widget: QWidget

    def __init__(self, components: Collection[Component]):
        super().__init__()
        uic.loadUi("./main_window.ui")
        self.components = components
        self.logger = get_logger("SER.main_window")

    def load_run_gui(self):
        self.log_debug(msg="Started Launching")