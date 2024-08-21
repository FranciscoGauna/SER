from typing import List, Any, Generator
from time import sleep
from datetime import datetime

from src.SER.model.gen import MetaArgTracker


"""
Each configurable instrument has a parameter called coupling. This parameter
dictates the pattern in which the "points" provided by each configurable device
are sent to each device. The device with the higher coupling value will iterate
over the points first. If two devices share the same coupling value, they will be coupled
meaning they receive the point at the same time.

The internal class MetaArgTracker provides the functionality to manage this coupling
behaviour. The examples below provide an example of expected behaviour.
"""


def add_elements(element, index, current_elements):
    current_elements[index] = element


def util_gen(elements: List[Any], index, current_elements) -> Generator:
    for element in elements:
        yield element, index, current_elements


def test_basic_coupling():
    current_elements = [None, None]

    tracker = MetaArgTracker([
        (0, lambda: util_gen([0, 1], 0, current_elements), add_elements),
        (1, lambda: util_gen([2, 3], 1, current_elements), add_elements),
    ])

    tracker.start()
    assert current_elements == [0, 2]
    tracker.advance()
    assert current_elements == [0, 3]
    tracker.advance()
    assert current_elements == [1, 2]
    tracker.advance()
    assert current_elements == [1, 3]


def test_basic_coupled():
    current_elements = [None, None]

    tracker = MetaArgTracker([
        (0, lambda: util_gen([0, 1], 0, current_elements), add_elements),
        (0, lambda: util_gen([2, 3], 1, current_elements), add_elements),
    ])

    tracker.start()
    assert current_elements == [0, 2]
    tracker.advance()
    assert current_elements == [1, 3]


def test_mixed_coupled():
    current_elements = [None, None, None]

    tracker = MetaArgTracker([
        (0, lambda: util_gen([0, 1], 0, current_elements), add_elements),
        (0, lambda: util_gen([2, 3], 1, current_elements), add_elements),
        (-1, lambda: util_gen(['A', 'B'], 2, current_elements), add_elements),
    ])

    tracker.start()
    assert current_elements == [0, 2, 'A']
    tracker.advance()
    assert current_elements == [1, 3, 'A']
    tracker.advance()
    assert current_elements == [0, 2, 'B']
    tracker.advance()
    assert current_elements == [1, 3, 'B']

