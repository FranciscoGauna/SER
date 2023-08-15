from abc import ABC, abstractmethod
from typing import Union, Generator, List

from lantz.qt import Frontend


class ConfigurationUi(Frontend):

    @abstractmethod
    def get_runtime_params(self) -> Union[Generator, List]:
        raise NotImplementedError("This component has not implemented it's runtime parameters generator")
