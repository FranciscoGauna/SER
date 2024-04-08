from typing import Callable

from . import Instrument
from . import ConfigurationUI


class Component:
    instrument: Instrument
    conf_ui: ConfigurationUI


class ComponentInitialization:
    name: str  # The name of the component, used to distinguish the different components for the data

    def __init__(self, component: Component, coupling: int, x: int, y: int, name: str = None):
        self.component = component
        self.component.instrument.coupling = coupling
        self.x = x
        self.y = y
        if name is None:
            self.name = type(component).__name__
        else:
            self.name = name
