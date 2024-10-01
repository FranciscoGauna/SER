import json
from threading import Lock
from traceback import format_exception
from typing import Collection
from logging import getLogger as get_logger

from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QListWidget
from pimpmyclass.mixins import LogMixin

from .color_list import ColorList
from ..interfaces import ProcessDataUI
from ..model.data_repository import DataRepository
from .progress_tracker import ProgressTracker
from ..model.sequencer import ExperimentSequencer

# Time between update ticks
# TODO: Think about changing this to a parameter or an environment variable
REFRESH_TIME = 50  # ms
COLOR_RUN_END = "green"
COLOR_RUN_IN_PROGRESS = "yellow"
COLOR_RUN_STOPPED = "red"


class ProcessUIManager(QObject, LogMixin):
    progress_list: list[dict]  # This holds all the data of the previous iteration
    progress_lock: Lock  # This is used to avoid synchronicity problems

    run_started = pyqtSignal()  # This signal is sent each time we start a new run. It's used to refresh the guis

    # This run number is checked against the sequence. It ensures we always have the correct number for the correct
    # initialization level for the ui
    run_number = 0

    def __init__(self, process_uis: Collection[ProcessDataUI], progress_tracker: ProgressTracker,
                 run_list: QListWidget, sequencer: ExperimentSequencer):
        super().__init__()
        self.logger = get_logger("SER.Core.UI.ProcessUIManager")
        self.process_uis = process_uis
        self.run_list = ColorList(run_list)
        self.progress_tracker = progress_tracker
        self.sequencer = sequencer
        self.data = sequencer.data

        self.progress_list = []
        self.progress_lock = Lock()
        self.running = False

        self.run_started.connect(self.run_start)

    def stop(self, premature=False):
        if self.running:
            self.running = False
            if premature:
                self.run_list.set_color(self.run_number, QColor(COLOR_RUN_STOPPED))
            else:
                self.run_list.set_color(self.run_number, QColor(COLOR_RUN_END))

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

        if self.run_number != 0:
            self.run_list.set_color(self.run_number - 1, QColor(COLOR_RUN_END))
            self.run_list.set_color(self.run_number, QColor(COLOR_RUN_IN_PROGRESS))
        else:
            self.run_list.set_color(self.run_number, QColor(COLOR_RUN_IN_PROGRESS))

    @pyqtSlot()
    def screen_tick(self):
        # Assignment operations are atomic, but we want to ensure that delta list isn't modified during the update
        self.progress_lock.acquire()
        delta_list = self.progress_list
        self.progress_list = []
        self.progress_lock.release()

        # we filter the delta_list to only the latest run initialized
        delta_list = list(filter(lambda x: x["run"]["id"] == self.run_number, delta_list))

        # Now that we have thread safe data, we update the process_ui which the data since the last iteration
        self.progress_tracker.advance(len(delta_list))
        for process_ui in self.process_uis:
            try:
                process_ui.add_data(delta_list)
            except Exception as e:
                process_ui.log_critical("".join(format_exception(e)))

        if self.running:
            QTimer().singleShot(REFRESH_TIME, self.screen_tick)

    def add_run(self, run: object):
        self.run_list.add_item(json.dumps(run))

    def load_sequence(self, sequence):
        self.run_list.clean_list()
        self.log_info(f"Sequence: {sequence}")
        for run in sequence:
            self.add_run(run)
        self.sequencer.sequence = sequence

    def sequence(self):
        return self.sequencer.sequence
