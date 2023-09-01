from typing import Any, Tuple, Callable, List, Generator, Self, Dict


class MultipleArgTracker:
    generators: List[
        Tuple[
            Generator,  # The generators we want to call, we store the reset function on the gen_fun variable
            Callable  # The function that takes the args in generator
        ]
    ]

    def __init__(self, generators: List[Callable[[], Generator]], functions: List[Callable], next_tracker: Callable, parent):
        self.functions = functions
        self.gen_fun = generators
        assert len(generators) == len(functions)
        self.reset_generators()
        self.next = next_tracker
        self.parent = parent

    def reset_generators(self):
        self.generators = []
        for i in range(len(self.functions)):
            self.generators.append((self.gen_fun[i](), self.functions[i]))

    def advance(self):
        try:
            for g, f in self.generators:
                arg = next(g)
                f(arg)
        except StopIteration:
            self.next()
            # The 'last' MultipleArgTracker is connected to the parent calling it to stop
            if self.parent.stopped:
                return
            self.reset_generators()
            for g, f in self.generators:
                arg = next(g)
                f(arg)


class MetaArgTracker:
    """
    The MetaArgTracker is the class that is tasked with administering the generators for the components, and passing
    those arguments to a function. The function could be arbitrary but the actual responsibility of task parallelization
    will be from the Dispatcher
    """

    def __init__(self, generators: List[Tuple[int, Callable[[], Generator], Callable]]):
        self.trackers: List[MultipleArgTracker] = []
        self.stopped = False

        # First, we store the
        couplings: Dict[int, List[Tuple[Callable[[], Generator], Callable]]]
        couplings = {}
        for comp in generators:
            if comp[0] in couplings:
                couplings[comp[0]].append((comp[1], comp[2]))
            else:
                couplings[comp[0]] = [(comp[1], comp[2])]

        sorted_gens: List[List[Tuple[Callable[[], Generator], Callable]]] = []
        for k in sorted(couplings.keys()):
            sorted_gens.append(couplings[k])

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
