from typing import List

from ..interfaces import ComponentInitialization


def verify_names(comps: List[ComponentInitialization]):
    names = set([x.name for x in comps])
    if len(names) != len(comps):
        raise Exception("There is an overlapping name in the list of components")
