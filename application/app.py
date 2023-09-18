from PyQt5.QtWidgets import QApplication

from components.VirtualPlatina import VirtualPlatina
from components.RandValue import RandValue

from src.SER import launch_app
from src.SER.interfaces import ComponentInitialization

launch_app(
    QApplication([]), [
        ComponentInitialization(VirtualPlatina(), 0, 0, 0, "motor 1"),
        ComponentInitialization(VirtualPlatina(), 1, 1, 0, "motor 2"),
    ], [
        ComponentInitialization(RandValue(), 1, 0, 1),
    ]
)
