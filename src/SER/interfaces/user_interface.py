from typing import Union, Generator, Collection, Dict
from abc import abstractmethod

from lantz.qt import Frontend

from . import Instrument


class ConfigurationUI(Frontend):
    """This class represents a Configuration User Interface. It's used before the start of the experiment, and it's
    used to set up the instrument before execution and provide the points during which the experiment is executed."""

    # This is a recommendation, you can rename the instrument to something else
    instrument: Instrument

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)

    @abstractmethod
    def get_points(self) -> Generator:
        """
        The function get_points is tasked with providing the points a component will use during its execution.
        The way it does this is through python Generators, as the task reads the task point by point. You can also
        provide other iterators that support next(_) and StopIteration.

        If 2 components are coupled AKA they both move simultaneously, they need to yield the same amount of points.
        Not respecting this is undefined behaviour
        :return: Generator with the amount of desired points
        """
        yield


class ProcessUI(Frontend):
    """This class represents the User Interface that is displayed to the during the execution of the experiment. It
    provides the user with a live tracking of the results of the experiment, and if applicable, controls that may
    be required during its execution."""

    # This is a recommendation, you can rename the instrument to something else
    instrument: Instrument

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)

    @abstractmethod
    def set_result(self, *args):
        raise NotImplementedError("The function set_result was not implemented")


class ProcessDataUI(Frontend):
    """This class represents the User Interface that displays the data from experiment during its execution.
    It gets updated at the end of each iteration with the method set_result."""

    # This is a recommendation, you can rename the instrument to something else
    instrument: Instrument

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)

    @abstractmethod
    def set_datum(self, components: Dict[str, Collection]):
        raise NotImplementedError("The function set_result was not implemented")


class FinalDataUI(Frontend):
    """This class represents the User Interface that displays the data from experiment. Once it has concluded"""

    # This is a recommendation, you can rename the instrument to something else
    instrument: Instrument

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)

    @abstractmethod
    def set_data(self, components: Dict[str, Collection]):
        raise NotImplementedError("The function set_result was not implemented")
