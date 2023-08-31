from typing import List, Any, Generator
from time import sleep
from datetime import datetime

from src.SER.utils.gen import MetaArgTracker


def log_print(*args):
    print(f"{datetime.now()}: {args}")


def util_gen(elements: List[Any]) -> Generator:
    for element in elements:
        yield element


if __name__ == "__main__":
    tracker = MetaArgTracker([
        (0, lambda: util_gen([0, 1]), log_print),
        (0, lambda: util_gen([2, 3]), log_print),
        (2, lambda: util_gen([4, 5]), log_print)
    ])

    tracker.start()
    sleep(1)
    while tracker.advance():
        sleep(1)
