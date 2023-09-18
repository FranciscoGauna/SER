from os import path
from threading import Thread
from typing import Collection
from logging import getLogger as get_logger

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QProgressBar, QLabel, QStackedWidget, QTableView
from pimpmyclass.mixins import LogMixin

from .data_table import TableModel
from .progress_tracker import ProgressTracker
from ..interfaces import ComponentInitialization
from ..model.runner import ExperimentRunner


class MainWidget(QStackedWidget, LogMixin):
    progress_changed = pyqtSignal()
    progress_ended = pyqtSignal()

    conf_layout: QGridLayout
    run_layout: QGridLayout
    data_layout: QGridLayout

    start_button: QPushButton

    progress_tracker: ProgressTracker
    progress_bar: QProgressBar
    progress_label: QLabel

    data_table: QTableView

    conf_page: QStackedWidget
    run_page: QStackedWidget
    data_page: QStackedWidget

    conf_box: QGroupBox
    run_box: QGroupBox
    progress_box: QGroupBox
    data_box: QGroupBox

    def __init__(self, components: Collection[ComponentInitialization], runner: ExperimentRunner):
        super().__init__()

        # This loads the file and loads up each object as part of this class
        # When using this method it's important to not overlap names with the widget
        # as the class will put the widgets as direct attributes of MainWidget
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "main_widget.ui")
        uic.loadUi(ui_file_path, self)

        # Creating Runner
        self.components = components
        self.runner = runner
        self.run_thread = Thread(target=self.run_experiment)
        self.started = False
        self.logger = get_logger("SER.Core.MainWindow")

        # Loading GUI
        self.conf_layout = self.conf_box.layout()
        self.run_layout = self.run_box.layout()
        self.data_layout = self.data_box.layout()

        self.load_config_gui()
        self.load_run_gui()
        self.load_data_gui()

        # Connecting Slots
        self.progress_changed.connect(self.progress_change)
        self.progress_ended.connect(self.progress_end)

        self.show()

    def load_config_gui(self):
        self.log_debug(msg="Started loading configuration interface")
        max_x = 0
        max_y = 0
        for component in self.components:
            self.conf_layout.addWidget(component.component.conf_ui, component.y, component.x)
            max_x = max(max_x, component.x)
            max_y = max(max_y, component.y)
        self.start_button.pressed.connect(self.start_experiment)
        self.setCurrentWidget(self.conf_page)

    def load_run_gui(self):
        self.log_debug(msg="Started loading run interface")
        self.progress_tracker = ProgressTracker(self.progress_bar, self.progress_label)

    def load_data_gui(self):
        self.log_debug(msg="Started loading data interface")

    def start_experiment(self):
        """
        This method runs strictly after the configuration, so it cleans the gui of those widgets
        :return: None
        """
        if not self.started:
            self.started = True
            self.log_debug(msg="Changing interface to the experiment interface")
            self.setCurrentWidget(self.run_page)
            self.progress_start()
            self.run_thread.start()

    def run_experiment(self):
        self.log_debug(msg="Changing interface to the data interface")
        self.runner.run_experiment(self.progress_changed.emit)
        self.progress_ended.emit()

    def progress_start(self):
        self.progress_tracker.start(self.runner.arg_tracker.points_amount())

    @pyqtSlot()
    def progress_change(self):
        self.progress_tracker.advance()
        # We also execute here the advancements of the data class

    @pyqtSlot()
    def progress_end(self):
        self.data_model = TableModel(self.runner.data.to_dataframe())
        self.data_table.setModel(self.data_model)
        self.setCurrentWidget(self.data_page)
