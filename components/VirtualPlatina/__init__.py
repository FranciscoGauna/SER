from src.SER.interfaces import Component
from .platina_frontend import PointSelectFrontend, PointSelectBackend


class VirtualPlatina(Component):
    def __init__(self, name):
        self.instrument = PointSelectBackend()
        self.conf_ui = PointSelectFrontend(name, backend=self.instrument)
        self.run_ui = None
