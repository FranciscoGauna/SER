from os import path
from threading import Thread, Lock
from typing import Collection
from logging import getLogger as get_logger

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QProgressBar, QLabel, QStackedWidget, QTableView, \
    QFileDialog
from pimpmyclass.mixins import LogMixin

from .components_dialog import ComponentsDialog
from .data_table import TableModel
from .progress_tracker import ProgressTracker
from ..interfaces import ComponentInitialization, ProcessDataUI, FinalDataUI
from ..model.runner import ExperimentRunner


class MainWidget(QStackedWidget, LogMixin):
    progress_ended = pyqtSignal()

    conf_layout: QGridLayout
    run_layout: QGridLayout
    data_layout: QGridLayout

    start_button: QPushButton
    load_conf_button: QPushButton
    configuration_dialog: ComponentsDialog

    run_stop_button:QPushButton
    progress_tracker: ProgressTracker
    progress_bar: QProgressBar
    progress_label: QLabel

    progress_timer: QTimer
    progress_list: list  # This stores the value of each datum that has been added since the last iteration
    progress_lock: Lock

    data_save_mat_button: QPushButton
    data_save_csv_button: QPushButton
    data_table: QTableView
    data_model: TableModel

    conf_page: QStackedWidget
    run_page: QStackedWidget
    data_page: QStackedWidget

    conf_box: QGroupBox
    run_box: QGroupBox
    progress_box: QGroupBox
    data_box: QGroupBox

    def __init__(self, components: Collection[ComponentInitialization], run_data_ui: Collection[ProcessDataUI],
                 final_data_ui: Collection[FinalDataUI], runner: ExperimentRunner, conf_folder=".", out_folder="."):
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

        # Storing and loading UI only components
        self.run_data_ui = run_data_ui
        self.final_data_ui = final_data_ui

        self.load_config_gui(conf_folder)
        self.load_run_gui()
        self.out_folder = out_folder

        # Connecting Slots
        self.progress_ended.connect(self.progress_end)

        self.show()

    def load_config_gui(self, conf_folder):
        self.log_debug(msg="Started loading configuration interface")
        max_x = 0
        max_y = 0
        for component in self.components:
            self.conf_layout.addWidget(component.component.conf_ui, component.y, component.x)
            max_x = max(max_x, component.x)
            max_y = max(max_y, component.y)
        self.start_button.pressed.connect(self.start_experiment)
        self.setCurrentWidget(self.conf_page)
        self.configuration_dialog = ComponentsDialog(self.components, conf_folder)
        self.load_conf_button.pressed.connect(self.configuration_dialog.show)

    def load_run_gui(self):
        self.log_debug(msg="Started loading run interface")
        self.progress_tracker = ProgressTracker(self.progress_bar, self.progress_label)
        self.run_stop_button.pressed.connect(self.stop_experiment)
        for ui in self.run_data_ui:
            self.run_layout.addWidget(ui, ui.x, ui.y)

    def load_data_gui(self):
        self.log_debug(msg="Started loading data interface")
        self.data_save_mat_button.pressed.connect(self.export_to_matlab)
        self.data_save_csv_button.pressed.connect(self.export_to_csv)
        for ui in self.final_data_ui:
            self.data_layout.addWidget(ui, ui.x, ui.y)

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
        self.runner.run_experiment(self.progress_change)
        self.progress_ended.emit()

    def stop_experiment(self):
        self.log_info(msg="Stopping the experiment prematurely with the button")
        self.runner.stopped = True  # Assignment is atomic

    # TODO: Considerar mover esto a una clase propia
    def progress_start(self):
        self.progress_list = []
        self.progress_lock = Lock()
        QTimer().singleShot(50, self.progress_update)
        self.progress_tracker.start(self.runner.arg_tracker.points_amount())
        for run_ui in self.run_data_ui:
            run_ui.initialize()

    def progress_change(self):
        # The lock ensures that we never add data to a list in the middle of being passed to another
        self.progress_lock.acquire()
        self.progress_list.append(self.runner.data.data[-1])
        self.progress_lock.release()

    def progress_update(self):
        # Assignment operations are atomic, but we want to ensure that delta list isn't modified during the update
        self.progress_lock.acquire()
        delta_list = self.progress_list
        self.progress_list = []
        self.progress_lock.release()

        # Now that we have thread safe data, we update the run_ui which the data since the last iteration
        self.progress_tracker.advance()
        for run_ui in self.run_data_ui:
            run_ui.add_data(delta_list)

        if not self.runner.stopped:
            QTimer().singleShot(50, self.progress_update)
        elif len(self.progress_list) > 0:
            QTimer().singleShot(50, self.progress_update)

    @pyqtSlot()
    def progress_end(self):
        self.data_model = TableModel(self.runner.data.to_dataframe())
        self.data_table.setModel(self.data_model)
        self.load_data_gui()
        self.setCurrentWidget(self.data_page)

    def export_to_csv(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.out_folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "Comma-separated values (*.csv);;All Files (*)", options=options)

        if file_name:
            self.runner.data.to_csv(file_name)

    def export_to_matlab(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.out_folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "MAT-file (*.MAT);;All Files (*)", options=options)

        if file_name:
            self.runner.data.to_matlab(file_name)
