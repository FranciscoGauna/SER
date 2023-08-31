from typing import Callable

from . import Instrument
from . import ConfigurationUI, ProcessUI


class Component:
    name: str  # The name of the component, used to distinguish the different components for the data UI
    instrument: Instrument
    conf_ui: ConfigurationUI
    run_ui: ProcessUI


class ComponentInitialization:
    component = Component

    def __init__(self, constructor: Callable[[], Component], alignment: int, x: int, y: int):
        self.constructor = constructor
        self.alignment = alignment
        self.x = x
        self.y = y

    def initialize(self):
        self.component = self.constructor()
        return self.component
