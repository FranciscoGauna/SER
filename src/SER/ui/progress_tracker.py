from datetime import datetime
from os import path
from threading import Thread
from typing import Collection
from logging import getLogger as get_logger

from PyQt5.QtWidgets import QGroupBox, QLabel, QProgressBar
from pimpmyclass.mixins import LogMixin


class ProgressTracker(LogMixin):

    def __init__(self, progress_bar: QProgressBar, progress_label: QLabel, amount: int):
        super().__init__()
        self.start_time = None
        self.start_time: datetime
        self.logger = get_logger("SER.Core.ProgressTracker")
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.amount = amount
        self.index = 0

        progress_bar.setRange(0, amount)
        progress_bar.setValue(0)

    def start(self):
        self.start_time = datetime.now()
        self.progress_label.setText(f"0/{self.amount}")

    def advance(self):
        self.index += 1
        self.progress_bar.setValue(self.index)
        time_elapsed = datetime.now() - self.start_time
        time_remaining = time_elapsed * ((self.amount - self.index) / self.index)
        self.progress_label.setText(f"{self.index}/{self.amount}\t Time Elapsed: {time_elapsed}\t "
                                    f"Time Remaining: {time_remaining}")


