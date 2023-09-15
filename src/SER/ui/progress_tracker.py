from os import path
from threading import Thread
from typing import Collection
from logging import getLogger as get_logger

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QStackedWidget
from pimpmyclass.mixins import LogMixin


class ProgressTracker(QWidget, LogMixin):
    conf_layout: QGridLayout
    run_layout: QGridLayout
    data_layout: QGridLayout

    stack_widget: QStackedWidget
    start_button: QPushButton

    def __init__(self):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "progress_tracker.ui")
        uic.loadUi(ui_file_path, self)
