from typing import Generator
from abc import abstractmethod

from lantz.qt import Backend


class Component(Backend):

    @abstractmethod
    def get_points(self) -> Generator: pass
