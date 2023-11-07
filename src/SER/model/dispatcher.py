from os import environ
from cProfile import runctx
from typing import Callable, List, Tuple, Any, Collection, Dict
from concurrent.futures import ThreadPoolExecutor

from lantz.core.log import get_logger
from pimpmyclass.mixins import LogMixin

counter = 0


def execute_fun(task: tuple[callable, tuple]):
    # TODO: documentar esta linea
    if environ.get("ENABLE_PROFILING"):
        global counter
        filename = f"profiling/dispatcher_{counter}.profile"
        counter += 1
        return runctx("task[0](*task[1])", {}, {"task": task}, filename=filename)
    else:
        return task[0](*task[1])


class Dispatcher(LogMixin):
    tasks: List[Tuple[Callable, Tuple]]

    def __init__(self):
        self.logger = get_logger("SER.Core.Dispatcher")
        self.tasks = []

    def wrap(self, fun: Callable) -> Callable:
        return lambda *args: self.add_task(fun, args)

    def add_task(self, fun: Callable, args):
        self.tasks.append((fun, args))

    def execute(self) -> Collection[Tuple[str, Dict[str, Any]]]:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(execute_fun, task) for task in self.tasks]
        self.tasks.clear()

        return [f.result() for f in futures]
