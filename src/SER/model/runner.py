from datetime import datetime
from typing import Collection, Generator

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin

from ..interfaces import ComponentInitialization
from ..utils.gen import MetaArgTracker




class ExperimentRunner(LogMixin):

    def __init__(
            self,
            configurable_components: Collection[ComponentInitialization],
            observable_components: Collection[ComponentInitialization]
    ):
        self.logger = get_logger("SER.Core.ExperimentRunner")
        self.observe_comp = observable_components
        self.conf_comp = configurable_components

        # We create the meta arg tracker
        # To do so we need a structure of each generator with the corresponding functions
        generators = [
            (
                comp.coupling,
                comp.component.conf_ui.get_points,
                self.lambda_creator(comp.name)
            )
            for comp in configurable_components
        ]
        self.arg_tracker = MetaArgTracker(generators)

    def lambda_creator(self, name):
        return lambda args: self.log_print(name, args)

    # TODO: Remove this
    def log_print(self, identifier, args):
        self.log_debug(f"{identifier}: {args}, type:{type(args)}")

    def run_experiment(self):
        self.log_info("Starting Experiment")
        self.arg_tracker.start()

        self.log_debug("Advanced one iteration")
        while self.arg_tracker.advance():
            self.log_debug("Advanced one iteration")

