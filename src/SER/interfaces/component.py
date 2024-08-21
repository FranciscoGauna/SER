from typing import Callable

from . import Instrument
from . import ConfigurationUI


class Component:
    instrument: Instrument
    conf_ui: ConfigurationUI


class ComponentInitialization:
    name: str  # The name of the component, used to distinguish the different components for the data

    def __init__(self, component: Component, coupling: int, x: int, y: int, name: str = None):
        """
        This class provides a wrapper for the component, allowing it to have identifiable information distinct
        from the other components. This information is provided as parameters for this constructor.

        :param component: The component to be wrapped.
        :param coupling: The coupling of the component. See tests/generator_test.py for a detailed explanation.
        :param x: The x coordinate for the configuration ui to be displayed in the configuration screen grid.
        :param y: The y coordinate for the configuration ui to be displayed in the configuration screen grid.
        :param name: The unique name for the component. If multiple devices with the same name are provided an exception
        will be raised.
        """
        self.component = component
        self.component.instrument.coupling = coupling
        self.x = x
        self.y = y
        if name is None:
            self.name = type(component).__name__
        else:
            self.name = name
