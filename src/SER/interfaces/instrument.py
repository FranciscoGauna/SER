from abc import abstractmethod
from typing import Tuple, Dict, Any, Generator

from lantz.core.log import get_logger
from lantz.qt import Backend


class Instrument(Backend):

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.logger_name = 'SER.Instrument.' + str(self)
        self.logger = get_logger(self.logger_name)

    @abstractmethod
    def get_config(self) -> Dict:
        """
        This is used to save the configration parameters for each run. The values are saved on a json format when
        serialized in a file format. As such, return only objects that can be saved in that format.

        :returns: a dictionary of configuration parameters and their values.
        """
        raise NotImplementedError("The method get_config has not been implemented")

    @abstractmethod
    def set_config(self, config: Dict) -> None:
        """
        This is used to restore the configration parameters for each run. The values are saved on a json format when
        serialized in a file format. As such, return only objects that can be saved in that format.
        """
        raise NotImplementedError("The method set_config has not been implemented")

    @abstractmethod
    def variable_documentation(self) -> Dict[str, str]:
        """
        This method should return a string containing the documentation for each kind of variable, including
        what it represents, what is the range of value and what is the unit.

        :returns: a dictionary of variable names and their documentation.
        """
        raise NotImplementedError("The method variable_documentation has not been implemented")

    def stop(self) -> None:
        """
        This method gets called if the experiment stopped prematurely by the user. If that's the case, do any
        procedures necessary to stop the instrument
        """
        return


class ObservableInstrument(Instrument):

    @abstractmethod
    def observe(self, *args) -> Dict[str, Any]:
        raise NotImplementedError("The method observe has not been implemented")


class ConfigurableInstrument(Instrument):
    coupling: int = 0

    def set_coupling(self, value):
        """
        Sets the coupling to the given value
        """
        self.coupling = value

    # For the configurable Instrument, coupling is always a setting we bring
    def set_config(self, config: Dict):
        self.coupling = config["coupling"]

    def get_config(self) -> Dict:
        return {"coupling": self.coupling}

    @abstractmethod
    def configure(self, *args) -> Dict[str, Any]:
        raise NotImplementedError("The method configure has not been implemented")

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

    @abstractmethod
    def point_amount(self) -> int:
        return 0
