from abc import ABC
from typing import Callable

from lantz.qt import Backend, Frontend


class Module(ABC):
    component: Backend
    conf_ui: Frontend
    run_ui: Frontend


# Dataclass
class ModuleInit:
    module: Module

    def __init__(self, creator: Callable[[], Module], alignment: int, x: int, y: int):
        """
        This class provides an encapsulation of the data required by core to start up the components and locate it
        in the interface
        """
        self.creator = creator
        self.alignment = alignment
        self.x = x
        self.y = y

    def init(self):
        self.component = self.creator()
