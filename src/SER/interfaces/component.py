from typing import Callable

from . import Instrument
from . import ConfigurationUI, ProcessUI


class Component:
    name: str  # The name of the component, used to distinguish the different components for the data
    instrument: Instrument
    conf_ui: ConfigurationUI
    run_ui: ProcessUI  # UI for tracking a single component and modify during execution if necessary


class ComponentInitialization:

    def __init__(self, component: Component, coupling: int, x: int, y: int, name: str = None):
        self.component = component
        self.coupling = coupling
        self.x = x
        self.y = y
        if name is None:
            self.name = type(component).__name__
        else:
            self.name = name
