from datetime import datetime
from traceback import format_exc
from typing import Collection, Callable

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin

from .data_repository import DataRepository
from ..interfaces import ComponentInitialization
from .dispatcher import Dispatcher
from .gen import MetaArgTracker


class ExperimentRunner(LogMixin):
    arg_tracker: MetaArgTracker

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
        self.error = None

        # We create an instance of the dispatcher:
        self.dispatcher = Dispatcher()

    def wrap_fun(self, name, fun):
        wrapped_fun = lambda *args: self.data.add_datum(name, fun(*args))
        return self.dispatcher.wrap(wrapped_fun)

    def setup_arg_tracker(self):

        # We create the meta arg tracker
        # To do so we need a structure of each generator with the corresponding functions
        generators = [
            (
                comp.component.instrument.coupling,
                comp.component.instrument.get_points,
                self.wrap_fun(comp.name, comp.component.instrument.configure)
            )
            for comp in self.conf_comp
        ]

        self.arg_tracker = MetaArgTracker(generators)

    def point_amount(self) -> int:
        # This function should always be called after setup_arg_tracker
        return self.arg_tracker.points_amount()

    def run_experiment(self, point_callback: Callable = None):
        # Precondition, call setup_arg_tracker
        self.log_info("Starting Experiment Run")
        self.stopped = False

        # Main experimental loop
        try:
            while not self.stopped and self.arg_tracker.advance():
                self.log_debug("Advanced Generator")
                self.data.next()
                config_time_start = datetime.now()
                self.dispatcher.execute()
                self.log_debug("Executed Configurator Dispatch")
                observe_time_start = datetime.now()

                for comp in self.observe_comp:
                    self.wrap_fun(comp.name, comp.component.instrument.observe)()

                self.dispatcher.execute()
                self.log_debug("Executed Observer Dispatch")

                self.data.add_datum("timestamp", {
                    "config_start_time": config_time_start,
                    "observe_start_time": observe_time_start,
                    "end_time": datetime.now()
                })
                self.log_debug("Added datum")

                if point_callback:
                    point_callback()
                self.log_debug("Advanced one iteration")
        except Exception as e:
            self.log_error(f"There has been an exception! {format_exc()}")
            self.error = e

        self.stopped = True

        self.log_info("Ending Experiment Run")
