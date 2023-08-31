from typing import Any, Tuple, Callable, List, Generator, Self, Dict


class MultipleArgTracker:
    def __init__(self, generators: List[Callable[[], Generator]], functions: List[Callable], next_tracker: Callable, parent):
        self.fun_gens = generators
        assert len(generators) == len(functions)
        self.generators = []
        for i in range(len(generators)):
            self.generators.append((generators[i](), functions[i]))
        self.next = next_tracker
        self.parent = parent

    def advance(self):
        try:
            for g, f in self.generators:
                arg = next(g)
                f(arg)
        except StopIteration:
            self.next()
            if self.parent.stopped:
                return
            old_gens = self.generators
            self.generators = []
            for i in range(len(old_gens)):
                self.generators.append((self.fun_gens[i](), old_gens[i][1]))
            for g, f in self.generators:
                arg = next(g)
                f(arg)


class MetaArgTracker:

    def __init__(self, generators: List[Tuple[int, Callable[[], Generator], Callable]]):
        self.trackers: List[MultipleArgTracker] = []
        self.stopped = False

        alignments: Dict[int, List[Tuple[Callable[[], Generator], Callable]]]
        alignments = {}
        for comp in generators:
            if comp[0] in alignments:
                alignments[comp[0]].append((comp[1], comp[2]))
            else:
                alignments[comp[0]] = [(comp[1], comp[2])]

        sorted_gens: List[List[Tuple[Callable[[], Generator], Callable]]] = []
        for k in sorted(alignments.keys()):
            sorted_gens.append(alignments[k])

        self.trackers.append(MultipleArgTracker(
            [x[0] for x in sorted_gens[0]],
            [x[1] for x in sorted_gens[0]],
            self.stop,
            self
        ))

        for i in range(1, len(sorted_gens)):
            self.trackers.append(MultipleArgTracker(
                [x[0] for x in sorted_gens[i]],
                [x[1] for x in sorted_gens[i]],
                self.trackers[-1].advance,
                self
            ))

    def start(self):
        for tracker in self.trackers:
            tracker.advance()

    def advance(self) -> bool:
        if not self.stopped:
            self.trackers[-1].advance()
            return not self.stopped
        return False

    def stop(self):
        self.stopped = True
