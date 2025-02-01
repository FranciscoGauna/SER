from typing import Union, Generator, Collection, Dict, Any, List
from abc import abstractmethod

from lantz.core.log import get_logger
from lantz.qt import Frontend

from . import Instrument


class ConfigurationUI(Frontend):
    """This class represents a Configuration User Interface. It's used before the start of the experiment, and it's
    used to set up the instrument before execution and provide the points during which the experiment is executed."""

    # This is a recommendation, you can rename the instrument to something else
    instrument: Instrument

    # path to the ui file you want to load. The format is either a string or a tuple with the folders of the path
    # ex: "ui/example.ui" or ("ui", "example.ui")
    gui: Union[str, tuple]

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)
        self.logger_name = 'SER.UI.ConfigurationUI.' + str(self)
        self.logger = get_logger(self.logger_name)


class ProcessDataUI(Frontend):
    """This class represents the User Interface that displays the data from experiment during its execution.
    It gets updated at the end of each iteration with the method add_data."""

    # These are used by the gui to load its position
    x: int
    y: int

    def __init__(self, x, y, parent=None, backend=None):
        """
        :param x: The x coordinate for the process ui to be displayed in the progress screen grid.
        :param y: The y coordinate for the process ui to be displayed in the progress screen grid.
        :param parent: Sent to the Frontend Construct. See Lantz for more information.
        :param backend: Sent to the Frontend Construct. See Lantz for more information.
        """
        super().__init__(parent, backend)
        self.logger_name = 'SER.UI.ProcessDataUI.' + str(self)
        self.logger = get_logger(self.logger_name)
        self.x = x
        self.y = y

    @abstractmethod
    def initialize(self):
        """
        This method gets run by the ui manager (SER/ui/process_ui_manager.py) each time a new run is started.
        Use it to reset the status of the ui to an empty one without data.
        """
        raise NotImplementedError("The function initialize was not implemented")

    @abstractmethod
    def add_data(self, data: List[Dict[str, Dict[str, Any]]]):
        """
        This method gets run periodically by the ui manager. The data is in the following format.
        [
            {"component 1 name": {var1 : value1, var2 : value2, ...}, ...},  # This corresponds to one iteration
            {"component 1 name": {var1 : value3, var2 : value4, ...}, ...},  # of the instrument configuration cycle
        ]

        Component data for configuration devices is added only if that device was configured during this iteration.
        Due to this is it strongly recommended to store the previous value if it's needed for display calculations.
        The variables and values depend on what is given by the observe and configure methods in the components
        provided.
        """
        raise NotImplementedError("The function add_data was not implemented")


class FinalDataUI(Frontend):
    """This class represents the User Interface that displays the data from experiment, once it has concluded.
    It displays only the data from the last run in the sequence."""

    # These are used by the gui to load its position
    x: int
    y: int

    def __init__(self, x, y, parent=None, backend=None):
        """
        :param x: The x coordinate for the process ui to be displayed in the data screen grid.
        :param y: The y coordinate for the process ui to be displayed in the data screen grid.
        :param parent: Sent to the Frontend Construct. See Lantz for more information.
        :param backend: Sent to the Frontend Construct. See Lantz for more information.
        """
        super().__init__(parent, backend)
        self.logger_name = 'SER.UI.FinalDataUI.' + str(self)
        self.logger = get_logger(self.logger_name)
        self.x = x
        self.y = y

    @abstractmethod
    def set_data(self, data: List[Dict[str, Dict[str, Any]]]):
        """
        This method gets run once at the end by the ui manager. The data is in the following format.
        [
            {"component 1 name": {var1 : value1, var2 : value2, ...}, ...},  # This corresponds to one iteration
            {"component 1 name": {var1 : value3, var2 : value4, ...}, ...},  # of the instrument configuration cycle
        ]

        The variables and values depend on what is given by the observe and configure methods in the components
        provided.
        """
        raise NotImplementedError("The function set_data was not implemented")
