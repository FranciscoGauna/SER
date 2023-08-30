from abc import abstractmethod
from typing import Tuple

from lantz.qt import Backend


class Instrument(Backend):
    headers = Tuple[str]  # This shows the headers for the data returned in the


class ObservableInstrument(Instrument):

    @abstractmethod
    def observe(self, *args):
        raise NotImplementedError("The method observe has not been implemented")


class ConfigurableInstrument(Instrument):

    @abstractmethod
    def configure(self, *args):
        raise NotImplementedError("The method configure has not been implemented")
