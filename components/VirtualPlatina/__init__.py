from src.SER.interfaces import Component
from .platina_frontend import PointSelectFrontend, PointSelectBackend


class VirtualPlatina(Component):
    def __init__(self):
        self.instrument = PointSelectBackend()
        self.conf_ui = PointSelectFrontend(backend=self.instrument)
        self.run_ui = None
