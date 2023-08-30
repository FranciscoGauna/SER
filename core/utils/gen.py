from typing import List, Generator, Any, Callable, Dict

from ..interfaces import ComponentInitialization


def gen_sum(generators: [Callable[[], Generator]]):
    generators = [g() for g in generators]
    n_s = (next(g) for g in generators)
    while True:
        yield n_s
        try:
            n_s = (next(g) for g in generators)
        except StopIteration:
            return


def gen_permute(prev: List[Any], next_gen: [Callable[[], Generator]]):
    gen = next_gen[0]
    if len(next_gen) == 1:
        for i in gen():
            yield *prev, i
    else:
        for i in gen():
            for j in gen_permute([*prev, i], next_gen[1:]):
                yield j


def comp_generator(comps: List[ComponentInitialization]) -> Generator:
    alignments: Dict[int, List[ComponentInitialization]]
    alignments = {}
    for comp in comps:
        if comp.alignment in alignments:
            alignments[comp.alignment].append(comp)
        else:
            alignments[comp.alignment] = [comp]

    generators: Dict[int, Callable[[], Generator]]
    generators = {}
    for k, v in alignments.items():
        generators[k] = lambda: gen_sum([comp.component.conf_ui.get_points for comp in v])

    sorted_gens: List[Callable[[], Generator]] = []
    for k in sorted(generators.keys()):
        sorted_gens.append(generators[k])

    for perm in gen_permute([], sorted_gens):
        yield perm
