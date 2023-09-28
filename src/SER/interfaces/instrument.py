from abc import abstractmethod
from configparser import ConfigParser
from typing import Tuple, Dict, Any, Generator

from lantz.core.log import get_logger
from lantz.qt import Backend


class Instrument(Backend):

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.logger_name = 'SER.Instrument.' + str(self)
        self.logger = get_logger(self.logger_name)

    @abstractmethod
    def get_config(self) -> ConfigParser:
        raise NotImplementedError("The method observe has not been implemented")

    @abstractmethod
    def set_config(self, config: ConfigParser):
        raise NotImplementedError("The method observe has not been implemented")


class ObservableInstrument(Instrument):

    @abstractmethod
    def observe(self, *args) -> Dict[str, Any]:
        raise NotImplementedError("The method observe has not been implemented")


class ConfigurableInstrument(Instrument):

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
