from datetime import datetime
from os import path
from threading import Thread
from typing import Collection, Callable
from logging import getLogger as get_logger

from PyQt5.QtWidgets import QGroupBox, QLabel, QProgressBar
from PyQt5.QtCore import pyqtSignal
from pimpmyclass.mixins import LogMixin

from .localization import localizator


class ProgressTracker(LogMixin):

    def __init__(self, progress_bar: QProgressBar, progress_label: QLabel, point_amount: Callable[[], int]):
        super().__init__()
        self.start_time = None
        self.start_time: datetime
        self.logger = get_logger("SER.Core.ProgressTracker")
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.amount = 0
        self.index = 0
        self.point_amount = point_amount

    def start(self):
        self.amount = self.point_amount()
        self.index = 0
        self.progress_bar.setRange(0, self.amount)
        self.progress_bar.setValue(0)
        self.start_time = datetime.now()
        self.progress_label.setText(f"0/{self.amount}")  # No Locale because it's only numeric

    def advance(self, amount):
        self.index += amount
        if self.index > 0:
            self.progress_bar.setValue(self.index)
            time_elapsed = datetime.now() - self.start_time
            time_remaining = time_elapsed * ((self.amount - self.index) / self.index)
            self.progress_label.setText(localizator.get("progress_label").format(
                self.index, self.amount, time_elapsed, time_remaining))


