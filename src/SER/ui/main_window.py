from os import path
from typing import Collection
from logging import getLogger as get_logger

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QPushButton, QStackedWidget
from pimpmyclass.mixins import LogMixin

from ..interfaces import ComponentInitialization
from ..model.runner import ExperimentRunner


class MainWindow(QMainWindow, LogMixin):
    conf_layout: QGridLayout
    run_layout: QGridLayout
    data_layout: QGridLayout

    stack_widget: QStackedWidget
    start_button: QPushButton

    def __init__(self, components: Collection[ComponentInitialization], runner: ExperimentRunner):
        super().__init__()
        ui_file_path = path.join(path.dirname(path.realpath(__file__)), "main_window.ui")
        uic.loadUi(ui_file_path, self)

        self.conf_layout = self.conf_page.layout()
        self.run_layout = self.run_page.layout()
        self.data_layout = self.data_page.layout()

        self.components = components
        self.runner = runner
        self.logger = get_logger("SER.Core.MainWindow")
        self.load_config_gui()
        self.show()

    def load_config_gui(self):
        self.log_debug(msg="Started loading configuration interface")
        max_x = 0
        max_y = 0
        for component in self.components:
            self.conf_layout.addWidget(component.component.conf_ui, component.y, component.x)
            max_x = max(max_x, component.x)
            max_y = max(max_y, component.y)
        self.start_button = QPushButton()
        self.start_button.setText("Start Experiment")  # TEXT: Reference to find this and replace with locale
        self.start_button.pressed.connect(self.start_experiment)
        self.conf_layout.addWidget(self.start_button, max_y + 1, max_x)
        self.stack_widget.setCurrentWidget(self.conf_page)

    def start_experiment(self):
        """
        This method runs strictly after the configuration, so it cleans the gui of those widgets
        :return: None
        """
        self.log_debug(msg="Changing interface to the experiment interface")
        self.stack_widget.setCurrentWidget(self.run_page)
        self.runner.run_experiment()
