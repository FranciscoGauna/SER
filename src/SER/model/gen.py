from typing import Any, Tuple, Callable, List, Generator, Self, Dict


class MultipleArgTracker:
    generators: List[
        Tuple[
            Generator,  # The generators we want to call, we store the reset function on the gen_fun variable
            Callable  # The function that takes the args in generator
        ]
    ]

    def __init__(self, generators: List[Callable[[], Generator]], functions: List[Callable], next_tracker: Callable,
                 parent):
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
            for generator, function in self.generators:
                arg = next(generator)
                function(*arg)
        except StopIteration:
            self.next()
            # The 'last' MultipleArgTracker is connected to the parent calling it to stop
            if self.parent.stopped:
                return
            self.reset_generators()
            for generator, function in self.generators:
                arg = next(generator)
                function(*arg)

    def amount(self) -> int:
        return len(list(self.gen_fun[0]()))


class MetaArgTracker:
    """
    The MetaArgTracker is the class that is tasked with administering the generators for the components, and passing
    those arguments to a function. The function could be arbitrary but the actual responsibility of execution and
    task parallelization will be from the Dispatcher class.
    """

    def __init__(self, generators: List[Tuple[int, Callable[[], Generator], Callable]]):
        self.trackers: List[MultipleArgTracker] = []
        self.stopped = False
        self.started = False

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
        self.started = True
        for tracker in self.trackers:
            tracker.advance()

    def advance(self) -> bool:
        """
        This advances the most "quick" generator (meaning the one that is updated on every iteration) and if it runs
        out of numbers, it advances the next generator. After advancing, it executes the function given.

        :return: bool indicating if the tracker has elements to continue
        """
        if not self.started:
            self.start()
            return not self.stopped
        if not self.stopped:
            self.trackers[-1].advance()
            return not self.stopped
        return False

    def stop(self):
        self.stopped = True

    def points_amount(self) -> int:
        mult = 1
        for tracker in self.trackers:
            mult *= tracker.amount()
        return mult
