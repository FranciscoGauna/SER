import json
from os import path

from PyQt5.QtWidgets import QApplication
from lantz.core.log import log_to_screen

from components.TwoDMapper import TwoDMapper
from components.VirtualPlatina import VirtualPlatina
from components.RandValue import RandValue

from src.SER import launch_app
from src.SER.interfaces import ComponentInitialization

app = QApplication([])
motor_x = VirtualPlatina("Motor X")
motor_y = VirtualPlatina("Motor Y")
mapper = TwoDMapper(("motor X", "pos", "X"), ("motor Y", "pos", "Y"),
                    ("Random", "val", "Random Value"))

log_to_screen()
launch_app(
    app, [
        ComponentInitialization(motor_x, 0, 0, 0, "motor X"),
        ComponentInitialization(motor_y, 1, 1, 0, "motor Y"),
    ], [
        ComponentInitialization(RandValue(), 1, 0, 1, "Random"),
    ],
    [mapper],
    [mapper],
    locale="en",
    coupling_ui_options={"enabled": True, "x": 1, "y": 1}
)
