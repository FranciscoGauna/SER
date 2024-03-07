import json
from os import path
from threading import Thread, Lock
from traceback import format_exception_only
from typing import Collection, Any
from logging import getLogger as get_logger

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QPushButton, QProgressBar, QLabel, QWidget, QTableView, \
    QFileDialog, QStackedWidget, QListWidget, QMessageBox
from pimpmyclass.mixins import LogMixin

from .components_dialog import ComponentsDialog
from .coupling_ui import CouplingUI
from .data_table import TableModel
from .localization import localizator
from .process_ui_manager import ProcessUIManager
from .progress_tracker import ProgressTracker
from ..interfaces import ComponentInitialization, ProcessDataUI, FinalDataUI
from ..model.documentation import to_md, to_htm
from ..model.sequencer import ExperimentSequencer


class MainWidget(QWidget, LogMixin):
    sequence_ended = pyqtSignal()

    run_list_widget: QListWidget

    conf_layout: QGridLayout
    run_layout: QGridLayout
    data_layout: QGridLayout

    start_button: QPushButton
    add_run_button: QPushButton
    load_conf_button: QPushButton
    configuration_dialog: ComponentsDialog

    run_stop_button: QPushButton
    progress_manager: ProcessUIManager
    progress_bar: QProgressBar
    progress_label: QLabel

    data_save_docs_htm_button: QPushButton
    data_save_docs_mkd_button: QPushButton
    data_save_mat_button: QPushButton
    data_save_csv_button: QPushButton
    data_table: QTableView
    data_model: TableModel

    stack_widget: QStackedWidget
    conf_page: QWidget
    run_page: QWidget
    data_page: QWidget

    conf_box: QGroupBox
    run_box: QGroupBox
    progress_box: QGroupBox
    data_box: QGroupBox

    def __init__(self, components: Collection[ComponentInitialization], run_data_ui: Collection[ProcessDataUI],
                 final_data_ui: Collection[FinalDataUI], sequencer: ExperimentSequencer,
                 coupling_ui_options: dict[str, Any], conf_folder=".", out_folder="."):
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
        self.error = None  # If we have found an error that forced the run experiment to end, we save the exception here
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

        self.load_run_gui()
        self.load_config_gui(conf_folder,  coupling_ui_options)
        self.out_folder = out_folder

        self.sequence_ended.connect(self.sequence_end)

    def load_config_gui(self, conf_folder: str, coupling_ui_options: dict[str, Any]):
        self.log_debug(msg="Started loading configuration interface")

        for component in self.components:
            if component.component.conf_ui is not None:
                self.conf_layout.addWidget(component.component.conf_ui, component.y, component.x)

        # TODO: Document the couplingUI options
        self.coupling_config = CouplingUI(self.components)
        if coupling_ui_options.get("enabled", False):
            self.conf_layout.addWidget(self.coupling_config,
                                       coupling_ui_options.get("y", 0), coupling_ui_options.get("x", 0))

        self.start_button.pressed.connect(self.start_experiment)
        self.add_run_button.pressed.connect(self.add_run)
        self.stack_widget.setCurrentWidget(self.conf_page)
        self.configuration_dialog = ComponentsDialog(self.progress_manager, self.components, conf_folder)
        self.load_conf_button.pressed.connect(self.configuration_dialog.show)

        # Text
        self.load_conf_button.setText(localizator.get("load_configuration"))
        self.add_run_button.setText(localizator.get("add_run_configuration"))
        self.start_button.setText(localizator.get("start_experiment"))
        self.conf_box.setTitle(localizator.get("configuration"))

    def load_run_gui(self):
        self.log_debug(msg="Started loading run interface")
        progress_tracker = ProgressTracker(self.progress_bar, self.progress_label,
                                                self.sequencer.runner.point_amount)
        self.progress_manager = ProcessUIManager(self.run_data_ui, progress_tracker, self.run_list_widget,
                                                 self.sequencer)
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
        self.data_save_csv_button.setText(localizator.get("save_as_csv"))
        self.data_save_mat_button.setText(localizator.get("save_as_mat"))
        self.data_save_docs_mkd_button.setText(localizator.get("save_as_md"))
        self.data_save_docs_htm_button.setText(localizator.get("save_as_html"))

    def add_run(self):
        run = self.sequencer.add_run()
        self.progress_manager.add_run(run)

    def start_experiment(self):
        """
        This method runs strictly after the configuration, so it cleans the gui of those widgets
        :return: None
        """
        if not self.started:
            self.started = True
            self.log_debug(msg="Changing interface to the experiment interface")
            self.stack_widget.setCurrentWidget(self.run_page)
            self.run_thread.start()

    def run_experiment(self):
        self.log_debug(msg="Changing interface to the data interface")
        self.error = self.sequencer.start_sequence(self.progress_manager.run_started.emit,
                                                   self.progress_manager.point_add)
        self.sequence_ended.emit()

    def stop_experiment(self):
        self.log_info(msg="Stopping the experiment prematurely with the button")
        self.sequencer.stop()
        self.progress_manager.stop(premature=True)

    @pyqtSlot()
    def sequence_end(self):
        self.progress_manager.stop()
        self.data_model = TableModel(self.sequencer.data.to_dataframe())
        self.data_table.setModel(self.data_model)
        self.load_data_gui()
        self.stack_widget.setCurrentWidget(self.data_page)

        if self.error is not None:
            error_box = QMessageBox()
            error_box.setText(f"There was an exception during the execution of the program:\n"
                              f"{''.join(format_exception_only(self.error))}")
            error_box.exec()

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
