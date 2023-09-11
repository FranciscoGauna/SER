from typing import Collection, Callable

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin

from .data_repository import DataRepository
from ..interfaces import ComponentInitialization
from .dispatcher import Dispatcher
from .gen import MetaArgTracker


class ExperimentRunner(LogMixin):

    def __init__(
            self,
            configurable_components: Collection[ComponentInitialization],
            observable_components: Collection[ComponentInitialization]
    ):
        self.logger = get_logger("SER.Core.ExperimentRunner")
        self.observe_comp = observable_components
        self.conf_comp = configurable_components
        self.data = DataRepository()

        # We create an instance of the dispatcher:
        self.dispatcher = Dispatcher()

        # We create the meta arg tracker
        # To do so we need a structure of each generator with the corresponding functions
        generators = [
            (
                comp.coupling,
                comp.component.conf_ui.get_points,
                self.wrap_fun(comp.name, comp.component.instrument.configure)
            )
            for comp in configurable_components
        ]

        self.arg_tracker = MetaArgTracker(generators)

    def wrap_fun(self, name, fun):
        wrapped_fun = lambda *args: self.data.add_datum(name, fun(*args))
        return self.dispatcher.wrap(wrapped_fun)

    def run_experiment(self, iteration_callback: Callable = None):
        self.log_info("Starting Experiment")

        while self.arg_tracker.advance():
            self.data.next()
            self.dispatcher.execute()

            for comp in self.observe_comp:
                self.wrap_fun(comp.name, comp.component.instrument.observe)()
                self.dispatcher.execute()

            if iteration_callback:
                iteration_callback()
            self.log_debug("Advanced one iteration")

        # TODO: Remove this forced print to file
        self.data.to_csv("output.csv")
        self.log_info("Ending Experiment")
