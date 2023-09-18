from src.SER.interfaces import Component
from .rand_value import RandValInstrument, RandValConfUi


class RandValue(Component):
    def __init__(self):
        self.instrument = RandValInstrument()
        self.conf_ui = RandValConfUi(backend=self.instrument)
        self.run_ui = None
