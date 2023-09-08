from src.SER.interfaces import Component
from .rand_value import RandValInstrument, RandValConfUi


def create_component() -> Component:
    comp = Component()
    comp.instrument = RandValInstrument()
    comp.conf_ui = RandValConfUi(backend=comp.instrument)
    comp.run_ui = None
    comp.data_ui = None
    return comp
