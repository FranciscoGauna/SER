import logging
from typing import Collection

from PyQt5.QtWidgets import QApplication

from .model.runner import ExperimentRunner
from .ui.main_window import MainWidget
from .interfaces import ComponentInitialization
from .log import log_to_socket, LOGGER


def launch_app(
        app: QApplication,
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization]
):
    # TODO: Parametrize logging
    log_to_socket(logging.DEBUG, "127.0.0.1", 19996)
    LOGGER.log(logging.DEBUG, "Starting Framework")

    # The main interface that has the code to start the experiment
    runner = ExperimentRunner(configurable_components, observable_components)
    window = MainWidget([*configurable_components, *observable_components], runner)
    app.exec()
