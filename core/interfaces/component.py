from abc import ABC
from lantz.qt import Backend

from .conf_ui import ConfigurationUi
from .run_ui import RunningUi
from .data_ui import DataDisplayUi


class Component(ABC):
    backend: Backend
    conf_ui: ConfigurationUi
    run_ui: RunningUi
    data_ui: DataDisplayUi
