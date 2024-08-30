from typing import Union, Generator, List, Dict
from time import sleep

from lantz.core import Feat
from lantz.qt import Backend

from src.SER.interfaces import ConfigurationUI, ConfigurableInstrument


class PointSelectBackend(ConfigurableInstrument):
    """
    This class exists only to utilize the connect_feat function from Lantz.
    """

    def variable_documentation(self) -> Dict[str, str]:
        return {
            "pos": "The coordinate of the motor. It's a virtual variable."
        }

    def configure(self, pos):
        sleep(0.1)
        self.log_debug("Finished configuration")
        return {"pos": pos}

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self._amount = 2
        self._init = 0.0
        self._final = 0.0

    @Feat
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, val: int):
        self._amount = val

    @Feat
    def init(self):
        return self._init

    @init.setter
    def init(self, val: float):
        self._init = val

    @Feat
    def final(self):
        return self._final

    @final.setter
    def final(self, val: float):
        self._final = val

    def get_points(self) -> Union[Generator, List]:
        delta = (self._final - self._init) / (self._amount - 1)

        for x in range(self._amount):
            yield (self._init + x * delta,)

    def point_amount(self) -> int:
        return self._amount

    def get_config(self) -> {}:
        config = {
            "amount": str(self._amount),
            "init": str(self._init),
            "final": str(self._final),
        }
        return config | super().get_config()

    def set_config(self, config: Dict):
        super().set_config(config)
        self.amount = int(config["amount"])
        self.init = float(config["init"])
        self.final = float(config["final"])


class PointSelectFrontend(ConfigurationUI):

    gui = "point_select.ui"

    def __init__(self, name, parent=None, backend=None):
        super().__init__(parent, backend)
        self.widget.setTitle(name)
        self.connect_feat(self.widget.amount_spinbox, self.backend, "amount")
        self.connect_feat(self.widget.init_spinbox, self.backend, "init")
        self.connect_feat(self.widget.final_spinbox, self.backend, "final")
