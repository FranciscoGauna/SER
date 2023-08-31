from typing import Collection, Generator

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin

from ..interfaces import ComponentInitialization


class ExperimentRunner(LogMixin):

    def __init__(
            self,
            configurable_components: Collection[ComponentInitialization],
            observable_components: Collection[ComponentInitialization]
    ):
        self.logger = get_logger("SER.Core.ExperimentRunner")
        self.observe_comp = observable_components
        self.conf_comp = configurable_components

    def get_config_point(self) -> Generator:
        return []

    def run_experiment(self):
        self.log_info("Starting Experiment")
        self.log_debug(f"Points: {list(self.get_config_point())}")
