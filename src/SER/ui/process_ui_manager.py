from threading import Lock
from typing import Collection
from logging import getLogger as get_logger

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QObject
from pimpmyclass.mixins import LogMixin

from ..interfaces import ProcessDataUI
from ..model.data_repository import DataRepository
from .progress_tracker import ProgressTracker


# Time between update ticks
# TODO: Think about changing this to a parameter or an environment variable
REFRESH_TIME = 50  # ms


class ProcessUIManager(QObject, LogMixin):
    progress_list: list[dict]  # This holds all the data of the previous iteration
    progress_lock: Lock  # This is used to avoid synchronicity problems

    run_started = pyqtSignal()  # This signal is sent each time we start a new run. It's used to refresh the guis

    # This run number is checked against the sequence. It ensures we always have the correct number for the correct
    # initialization level for the ui
    run_number = 0

    def __init__(self, process_uis: Collection[ProcessDataUI], progress_tracker: ProgressTracker, data: DataRepository):
        super().__init__()
        self.logger = get_logger("SER.Core.UI.ProcessUIManager")
        self.process_uis = process_uis
        self.progress_tracker = progress_tracker
        self.data = data

        self.progress_list = []
        self.progress_lock = Lock()
        self.running = False

        self.run_started.connect(self.run_start)

    def stop(self):
        self.running = False

    def point_add(self):
        self.progress_lock.acquire()
        self.progress_list.append(self.data.last_datum())
        self.progress_lock.release()

    # Start
    @pyqtSlot()
    def run_start(self):
        # We lock the list until we reinitialize the process ui
        self.progress_lock.acquire()
        self.progress_list = []

        self.progress_tracker.start()
        for process_ui in self.process_uis:
            process_ui.initialize()

        if not self.running:
            QTimer().singleShot(50, self.screen_tick)
            self.running = True
        else:
            self.run_number += 1
        self.progress_lock.release()

    @pyqtSlot()
    def screen_tick(self):
        # Assignment operations are atomic, but we want to ensure that delta list isn't modified during the update
        self.progress_lock.acquire()
        delta_list = self.progress_list
        self.progress_list = []

        # we filter the delta_list to only the latest run initialized
        delta_list = list(filter(lambda x: x["run"]["id"] == self.run_number, delta_list))

        # Now that we have thread safe data, we update the process_ui which the data since the last iteration
        self.progress_tracker.advance(len(delta_list))
        for process_ui in self.process_uis:
            process_ui.add_data(delta_list)

        if self.running:
            QTimer().singleShot(REFRESH_TIME, self.screen_tick)

        self.progress_lock.release()
