from components import VirtualPlatina

from core import launch_app
from core.interfaces import ComponentInitialization

launch_app([
    ComponentInitialization(VirtualPlatina.create_component, 0, 0, 0),
    ComponentInitialization(VirtualPlatina.create_component, 1, 0, 1)
])
