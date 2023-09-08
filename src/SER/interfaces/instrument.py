from abc import abstractmethod
from typing import Tuple, Dict, Any

from lantz.core.log import get_logger
from lantz.qt import Backend


class Instrument(Backend):

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self.logger_name = 'SER.Instrument.' + str(self)
        self.logger = get_logger(self.logger_name)


class ObservableInstrument(Instrument):

    @abstractmethod
    def observe(self, *args) -> Dict[str, Any]:
        raise NotImplementedError("The method observe has not been implemented")


class ConfigurableInstrument(Instrument):

    @abstractmethod
    def configure(self, *args) -> Dict[str, Any]:
        raise NotImplementedError("The method configure has not been implemented")
