from core.interfaces import Component
from .platina_frontend import PointSelectFrontend


def create_component() -> Component:
    comp = Component()
    comp.conf_ui = PointSelectFrontend()
    comp.run_ui = None
    comp.data_ui = None
    return comp
