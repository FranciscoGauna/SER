from typing import Callable, Collection, Any
from logging import getLogger as get_logger

from pimpmyclass.mixins import LogMixin

from .data_repository import DataRepository
from .runner import ExperimentRunner
from ..interfaces import Instrument, ComponentInitialization


class ExperimentSequencer(LogMixin):
    sequence: list[dict[str, dict]]
    components: dict[str, Instrument]
    runner: ExperimentRunner
    data: DataRepository

    def __init__(
            self,
            configurable_components: Collection[ComponentInitialization],
            observable_components: Collection[ComponentInitialization]
    ):
        self.sequence = []
        self.data = DataRepository()
        self.runner = ExperimentRunner(configurable_components, observable_components, self.data)

        self.components = {}
        for comp in configurable_components:
            self.components[comp.name] = comp.component.instrument
        for comp in observable_components:
            self.components[comp.name] = comp.component.instrument

        self.stopped = True
        self.logger = get_logger("SER.Core.Sequencer")

    def stop(self):
        self.stopped = True
        self.runner.stopped = True

    def add_run(self):
        new_run = {}
        for name, instrument in self.components.items():
            new_run[name] = instrument.get_config()
        self.sequence.append(new_run)
        self.log_info(f"Added new run: {new_run}")
        return new_run

    def load_sequence(self, sequence):
        self.sequence = sequence

    def start_sequence(self, run_callback: Callable[[], Any], point_callback: Callable):
        # TODO: mention the initialize in documentation
        # We initialize every component
        for conf in self.runner.conf_comp:
            conf.component.instrument.initialize()
        for observe in self.runner.observe_comp:
            observe.component.instrument.initialize()

        self.stopped = False

        for run in self.sequence:
            for comp, conf in run.items():
                self.components[comp].set_config(conf)
            self.runner.setup_arg_tracker()
            if run_callback:
                run_callback()
            self.runner.run_experiment(point_callback)
            # If we have an error we stop the run and alert the user in the
            if self.runner.error is not None:
                break
            self.data.next_run()
            if self.stopped:
                break

        self.stopped = True

        # We finalize every component
        for conf in self.runner.conf_comp:
            conf.component.instrument.finalize()
        for observe in self.runner.observe_comp:
            observe.component.instrument.finalize()

        return self.runner.error
