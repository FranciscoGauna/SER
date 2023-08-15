import logging
from typing import Collection

from PyQt5.QtWidgets import QApplication

from core.main_window import MainWindow
from core.interfaces import ComponentInitialization
from core.log import log_to_socket, LOGGER


def launch_app(
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization]
):
    # TODO: Parametrize logging
    log_to_socket(logging.DEBUG, "127.0.0.1", 19996)
    LOGGER.log(logging.DEBUG, "Starting Framework")

    app = QApplication([])  # We don't use any Qt commandline args

    # The list here is an ugly hack to get the map to execute
    list(map(ComponentInitialization.init, configurable_components))
    list(map(ComponentInitialization.init, observable_components))

    # The main interface that has the code to start the experiment
    window = MainWindow(configurable_components, observable_components)
    app.exec()
