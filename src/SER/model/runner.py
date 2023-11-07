from datetime import datetime
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
            observable_components: Collection[ComponentInitialization],
            data: DataRepository
    ):
        self.logger = get_logger("SER.Core.ExperimentRunner")
        self.observe_comp = observable_components
        self.conf_comp = configurable_components
        self.data = data

        # We create an instance of the dispatcher:
        self.dispatcher = Dispatcher()

    def wrap_fun(self, name, fun):
        wrapped_fun = lambda *args: self.data.add_datum(name, fun(*args))
        return self.dispatcher.wrap(wrapped_fun)

    def run_experiment(self, iteration_callback: Callable = None):
        self.log_info("Starting Experiment Run")

        # We create the meta arg tracker
        # To do so we need a structure of each generator with the corresponding functions
        generators = [
            (
                comp.coupling,
                comp.component.instrument.get_points,
                self.wrap_fun(comp.name, comp.component.instrument.configure)
            )
            for comp in self.conf_comp
        ]

        self.arg_tracker = MetaArgTracker(generators)
        self.stopped = False

        # Main experimental loop
        while not self.stopped and self.arg_tracker.advance():
            self.data.next()
            config_time_start = datetime.now()
            self.dispatcher.execute()
            observe_time_start = datetime.now()

            for comp in self.observe_comp:
                self.wrap_fun(comp.name, comp.component.instrument.observe)()
                self.dispatcher.execute()

            self.data.add_datum("timestamp", {
                "config_start_time": config_time_start,
                "observe_start_time": observe_time_start,
                "end_time": datetime.now()
            })

            if iteration_callback:
                iteration_callback()
            self.log_debug("Advanced one iteration")

        self.stopped = True

        self.log_info("Ending Experiment Run")

    def point_amount(self) -> int:
        return self.arg_tracker.points_amount()
