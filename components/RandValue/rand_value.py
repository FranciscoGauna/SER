from random import random
from typing import Generator, Dict, Any

from lantz.core import Feat

from src.SER.interfaces import ConfigurationUI, ObservableInstrument


class RandValInstrument(ObservableInstrument):

    def variable_documentation(self) -> Dict[str, str]:
        return {"val": f"This represents a random value in the {self.min}-{self.max} range"}

    def get_config(self):
        config = {"min": self.min, "max": self.max}
        return config

    def set_config(self, config: Dict):
        self.min = float(config["min"])
        self.max = float(config["max"])

    def __init__(self, **instruments_and_backends):
        super().__init__(**instruments_and_backends)
        self._min = 0
        self._max = 1

    def observe(self, *args) -> Dict[str, Any]:
        val = random() + self._min
        val *= (self._max - self._min)
        return {"val": val}

    @Feat
    def min(self):
        return self._min

    @min.setter
    def min(self, val):
        self._min = val

    @Feat
    def max(self):
        return self._max

    @max.setter
    def max(self, val):
        self._max = val


class RandValConfUi(ConfigurationUI):
    gui = "rand.ui"

    def __init__(self, parent=None, backend=None):
        super().__init__(parent, backend)
        self.connect_feat(self.widget.min_spin_box, self.backend, "min")
        self.connect_feat(self.widget.max_spin_box, self.backend, "max")

    def get_points(self) -> Generator:
        raise NotImplemented("This is an observable, so it doesn't need points")
