import logging
from typing import Collection

from PyQt5.QtWidgets import QApplication

from .model.sequencer import ExperimentSequencer
from .ui.main_window import MainWidget
from .interfaces import ComponentInitialization, ProcessDataUI, FinalDataUI
from .log import log_to_socket, LOGGER, log_to_screen


def launch_app(
        app: QApplication,
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization],
        run_data_ui: Collection[ProcessDataUI],
        final_data_ui: Collection[FinalDataUI]
):
    # TODO: Parametrize logging
    #log_to_socket(logging.DEBUG, "127.0.0.1", 19996)
    #log_to_screen(logging.DEBUG)
    LOGGER.log(logging.DEBUG, "Starting Framework")

    # The main interface that has the code to start the experiment
    sequencer = ExperimentSequencer(configurable_components, observable_components)
    window = MainWidget([*configurable_components, *observable_components],
                        run_data_ui, final_data_ui, sequencer)
    app.exec()
