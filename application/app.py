from components import VirtualPlatina, RandValue

from src.SER import launch_app
from src.SER.interfaces import ComponentInitialization

launch_app([
    ComponentInitialization(VirtualPlatina.create_component, 0, 0, 0, "motor 1"),
    ComponentInitialization(VirtualPlatina.create_component, 1, 1, 0, "motor 2"),
], [
    ComponentInitialization(RandValue.create_component, 1, 0, 1, "Rand"),
])
