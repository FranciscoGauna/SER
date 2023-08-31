from src.SER.interfaces import Component
from .platina_frontend import PointSelectFrontend, PointSelectBackend


def create_component() -> Component:
    comp = Component()
    comp.instrument = PointSelectBackend()
    comp.conf_ui = PointSelectFrontend(backend=comp.instrument)
    comp.run_ui = None
    comp.data_ui = None
    return comp
