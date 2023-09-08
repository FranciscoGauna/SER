from typing import Callable, List, Tuple, Any, Collection, Dict
from concurrent.futures import ThreadPoolExecutor

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin


class Dispatcher(LogMixin):
    tasks: List[Tuple[Callable, Any]]

    def __init__(self):
        self.logger = get_logger("SER.Core.Dispatcher")
        self.tasks = []

    def wrap(self, fun: Callable) -> Callable:
        return lambda *args: self.add_task(fun, args)

    def add_task(self, fun: Callable, args):
        self.tasks.append((fun, args))

    def execute(self) -> Collection[Tuple[str, Dict[str, Any]]]:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(task[0], *task[1]) for task in self.tasks]
        self.tasks.clear()

        return [f.result() for f in futures]
