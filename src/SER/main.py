import logging
from typing import Collection, Any

from PyQt5.QtWidgets import QApplication, QWidget

from .model.sequencer import ExperimentSequencer
from .ui.main_window import MainWidget
from .interfaces import ComponentInitialization, ProcessDataUI, FinalDataUI
from .log import log_to_socket, LOGGER, log_to_screen
from .ui.localization import localizator


# Note we only read the coupling_ui_options, so it doesn't matter if it's mutable.
# noinspection PyDefaultArgument
def get_main_widget(
        configurable_components: Collection[ComponentInitialization],
        observable_components: Collection[ComponentInitialization],
        run_data_ui: Collection[ProcessDataUI],
        final_data_ui: Collection[FinalDataUI],
        coupling_ui_options: dict[str, Any] = {},
        conf_folder=".",
        out_folder=".",
        locale="en",
) -> QWidget:
    """
    This function creates a widget that contains the SER. The widget loads the configuration ui provided by the
    components and can be interacted by the user.

    :param configurable_components: List of ComponentInitialization that include ConfigurableInstrument
    :param observable_components: List of ComponentInitialization that include ObservableInstrument
    :param run_data_ui: List of ProcessDataUI that reads the data and displays it as the experiment is running
    :param final_data_ui: List of FinalDataUI that reads the data and displays it after the experiment is finished
    :param coupling_ui_options: Dictionary with data to initialize the gui that changes the coupling. It should contain
    'enabled' bool, 'x' int, 'y' int, indicating if it needs to be enabled and the coordinated respectively.
    :param conf_folder: Direction to a folder where to open the save dialog for configuration files by default
    :param out_folder: Direction to a folder where to open the save dialog for output files by default
    :param locale: Value indicating what language to display the interface. 'en' for english and 'es' for spanish
    :return: A QWidget that can be embedded in your QT application.
    """
    # TODO: Parametrize logging
    LOGGER.log(logging.DEBUG, "Starting Framework")
    localizator.set(locale)

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
        out_folder=".",
        locale="en"
):
    """
    This function uses the widget created by get_main_widget(...) to create the main QT application.

    :param app: QApplication object in which to run the app. It's necessary to provide as components cannot be
    created without a running QApplication in the background.
    :param configurable_components: List of ComponentInitialization that include ConfigurableInstrument
    :param observable_components: List of ComponentInitialization that include ObservableInstrument
    :param run_data_ui: List of ProcessDataUI that reads the data and displays it as the experiment is running
    :param final_data_ui: List of FinalDataUI that reads the data and displays it after the experiment is finished
    :param coupling_ui_options: Dictionary with data to initialize the gui that changes the coupling. It should contain
    'enabled' bool, 'x' int, 'y' int, indicating if it needs to be enabled and the coordinated respectively.
    :param conf_folder: Direction to a folder where to open the save dialog for configuration files by default
    :param out_folder: Direction to a folder where to open the save dialog for output files by default
    :param locale: Value indicating what language to display the interface. 'en' for english and 'es' for spanish
    :return: None. This will return when the user closes the app.
    """
    window = get_main_widget(configurable_components, observable_components, run_data_ui, final_data_ui,
                             coupling_ui_options, conf_folder, out_folder, locale)
    window.setWindowTitle(localizator.get("SER"))
    window.show()
    app.exec()
