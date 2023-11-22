import logging
from typing import Collection, Any

from PyQt5.QtWidgets import QApplication

from .model.sequencer import ExperimentSequencer
from .ui.main_window import MainWidget
from .interfaces import ComponentInitialization, ProcessDataUI, FinalDataUI
from .log import log_to_socket, LOGGER, log_to_screen


# Note we only read the coupling_ui_options, so it doesn't matter if it's mutable.
# noinspection PyDefaultArgument
def get_main_widget(
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization],
        run_data_ui: Collection[ProcessDataUI],
        final_data_ui: Collection[FinalDataUI],
        coupling_ui_options: dict[str, Any] = {},
        conf_folder=".",
        out_folder="."
):
    # TODO: Parametrize logging
    LOGGER.log(logging.DEBUG, "Starting Framework")

    # The main interface that has the code to start the experiment
    sequencer = ExperimentSequencer(configurable_components, observable_components)
    window = MainWidget([*configurable_components, *observable_components],
                        run_data_ui, final_data_ui, sequencer, coupling_ui_options, conf_folder, out_folder)

    return window


# Note we only read the coupling_ui_options, so it doesn't matter if it's mutable.
# noinspection PyDefaultArgument
def launch_app(
        app: QApplication,
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization],
        run_data_ui: Collection[ProcessDataUI],
        final_data_ui: Collection[FinalDataUI],
        coupling_ui_options: dict[str, Any] = {},
        conf_folder=".",
        out_folder="."
):
    window = get_main_widget(configurable_components, observable_components, run_data_ui, final_data_ui,
                             coupling_ui_options, conf_folder, out_folder)
    window.show()
    app.exec()
