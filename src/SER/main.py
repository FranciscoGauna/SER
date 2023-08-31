import logging
from typing import Collection

from PyQt5.QtWidgets import QApplication

from .model.run_experiment import ExperimentRunner
from .ui.main_window import MainWindow
from .interfaces import ComponentInitialization
from .log import log_to_socket, LOGGER


def launch_app(
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization]
):
    # TODO: Parametrize logging
    log_to_socket(logging.DEBUG, "127.0.0.1", 19996)
    LOGGER.log(logging.DEBUG, "Starting Framework")

    app = QApplication([])  # We don't use any Qt commandline args

    # The list here is an ugly hack to get the map to execute
    list(map(ComponentInitialization.initialize, configurable_components))
    list(map(ComponentInitialization.initialize, observable_components))

    # The main interface that has the code to start the experiment
    runner = ExperimentRunner(configurable_components, observable_components)
    window = MainWindow([*configurable_components, *observable_components], runner)
    app.exec()
