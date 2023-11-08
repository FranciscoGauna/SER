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
from .localization import localizator
from .progress_tracker import ProgressTracker
from ..interfaces import ComponentInitialization, ProcessDataUI, FinalDataUI
from ..model.documentation import to_md, to_htm
from ..model.sequencer import ExperimentSequencer


class MainWidget(QStackedWidget, LogMixin):
    sequence_ended = pyqtSignal()
    run_started = pyqtSignal()

    conf_layout: QGridLayout
    run_layout: QGridLayout
    data_layout: QGridLayout

    start_button: QPushButton
    add_run_button: QPushButton
    load_conf_button: QPushButton
    configuration_dialog: ComponentsDialog

    run_stop_button: QPushButton
    progress_tracker: ProgressTracker
    progress_bar: QProgressBar
    progress_label: QLabel

    progress_timer: QTimer
    progress_list: list  # This stores the value of each datum that has been added since the last iteration
    progress_lock: Lock

    data_save_docs_htm_button: QPushButton
    data_save_docs_mkd_button: QPushButton
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
                 final_data_ui: Collection[FinalDataUI], sequencer: ExperimentSequencer, conf_folder=".",
                 out_folder="."):
        super().__init__()

        # This loads the file and loads up each object as part of this class
        # When using this method it's important to not overlap names with the widget
        # as the class will put the widgets as direct attributes of MainWidget
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "main_widget.ui")
        uic.loadUi(ui_file_path, self)

        # Creating Sequencer
        self.components = components
        self.sequencer = sequencer
        self.run_thread = Thread(target=self.run_experiment)
        self.started = False
        self.logger = get_logger("SER.Core.MainWindow")

        # Loading GUI
        self.conf_layout = self.conf_box.layout()
        self.run_layout = self.run_box.layout()
        self.data_layout = self.data_box.layout()

        # Storing and loading UI only components
        self.run_data_ui = run_data_ui
        self.timer_started = False
        self.final_data_ui = final_data_ui

        self.load_config_gui(conf_folder)
        self.load_run_gui()
        self.out_folder = out_folder

        # Connecting Slots
        self.sequence_ended.connect(self.sequence_end)
        self.run_started.connect(self.run_start)

        self.show()

    def load_config_gui(self, conf_folder):
        self.log_debug(msg="Started loading configuration interface")

        for component in self.components:
            if component.component.conf_ui is not None:
                self.conf_layout.addWidget(component.component.conf_ui, component.y, component.x)

        self.start_button.pressed.connect(self.start_experiment)
        self.add_run_button.pressed.connect(self.add_run)
        self.setCurrentWidget(self.conf_page)
        self.configuration_dialog = ComponentsDialog(self.components, conf_folder)
        self.load_conf_button.pressed.connect(self.configuration_dialog.show)

        # Text
        self.load_conf_button.setText(localizator.get("load_configuration"))
        self.add_run_button.setText(localizator.get("add_run_configuration"))
        self.start_button.setText(localizator.get("start_experiment"))
        self.conf_box.setTitle(localizator.get("configuration"))

    def load_run_gui(self):
        self.log_debug(msg="Started loading run interface")
        self.progress_tracker = ProgressTracker(self.progress_bar, self.progress_label)
        self.run_stop_button.pressed.connect(self.stop_experiment)

        for ui in self.run_data_ui:
            self.run_layout.addWidget(ui, ui.x, ui.y)

        for component in self.components:
            if component.component.conf_ui is not None:
                self.conf_layout.addWidget(component.component.conf_ui, component.y, component.x)

        # Text
        self.run_box.setTitle(localizator.get("running"))
        self.progress_box.setTitle(localizator.get("progress"))
        self.run_stop_button.setText(localizator.get("stop"))

    def load_data_gui(self):
        self.log_debug(msg="Started loading data interface")
        self.data_save_docs_htm_button.pressed.connect(self.export_docs_to_htm)
        self.data_save_docs_mkd_button.pressed.connect(self.export_docs_to_md)
        self.data_save_mat_button.pressed.connect(self.export_to_matlab)
        self.data_save_csv_button.pressed.connect(self.export_to_csv)
        for ui in self.final_data_ui:
            self.data_layout.addWidget(ui, ui.x, ui.y)

        # Text
        self.data_box.setTitle(localizator.get("data"))
        self.data_save_csv_button.setText(localizator.get("Save as csv"))
        self.data_save_mat_button.setText(localizator.get("Save as MAT"))
        self.data_save_docs_mkd_button.setText(localizator.get("Save docs as Markdown"))
        self.data_save_docs_htm_button.setText(localizator.get("Save docs as HTML"))

    def add_run(self):
        self.sequencer.add_run()

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
        self.sequencer.start_sequence(self.sequence_change_sync, self.progress_change)
        self.sequence_ended.emit()

    def stop_experiment(self):
        self.log_info(msg="Stopping the experiment prematurely with the button")
        self.sequencer.stop()

    # TODO: Considerar mover esto a una clase propia
    def progress_start(self):
        self.progress_list = []
        self.progress_lock = Lock()

    def sequence_change_sync(self):
        self.progress_lock.acquire()
        self.progress_list = []
        self.progress_lock.release()
        self.run_started.emit()

    @pyqtSlot()
    def run_start(self):
        self.progress_tracker.start(self.sequencer.runner.arg_tracker.points_amount())
        for run_ui in self.run_data_ui:
            run_ui.initialize()
        if not self.timer_started:
            QTimer().singleShot(50, self.progress_update)
            self.timer_started = True

    def progress_change(self):
        # The lock ensures that we never add data to a list in the middle of being passed to another
        self.progress_lock.acquire()
        self.progress_list.append(self.sequencer.data.last_datum())
        self.progress_lock.release()

    def progress_update(self):
        # Assignment operations are atomic, but we want to ensure that delta list isn't modified during the update
        self.progress_lock.acquire()
        delta_list = self.progress_list
        self.progress_list = []
        self.progress_lock.release()

        # Now that we have thread safe data, we update the run_ui which the data since the last iteration
        total_amount = 1
        self.progress_tracker.advance(len(delta_list))
        for run_ui in self.run_data_ui:
            run_ui.add_data(delta_list)

        if not self.sequencer.stopped:
            QTimer().singleShot(50, self.progress_update)
        elif len(self.progress_list) > 0:
            QTimer().singleShot(50, self.progress_update)

    @pyqtSlot()
    def sequence_end(self):
        self.data_model = TableModel(self.sequencer.data.to_dataframe())
        self.data_table.setModel(self.data_model)
        self.load_data_gui()
        self.setCurrentWidget(self.data_page)

    # Export Data
    def export_to_csv(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.out_folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "Comma-separated values (*.csv);;All Files (*)", options=options)

        if file_name:
            self.sequencer.data.to_csv(file_name)

    def export_to_matlab(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.out_folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "MAT-file (*.MAT);;All Files (*)", options=options)

        if file_name:
            self.sequencer.data.to_matlab(file_name)

    def export_docs_to_htm(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.out_folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "HyperText Markup Language (*.html);;All Files (*)", options=options)

        if file_name:
            to_htm(file_name, self.components)

    def export_docs_to_md(self):
        options = QFileDialog.Options()
        file_dialog = QFileDialog()
        file_dialog.setDirectory(self.out_folder)
        file_name, _ = file_dialog.getSaveFileName(self, "Save File", "",
                                                   "Markdown (*.md);;All Files (*)", options=options)

        if file_name:
            to_md(file_name, self.components)
