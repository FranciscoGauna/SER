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
motor_1 = VirtualPlatina()
if path.exists("motor_1.json"):
    with open("motor_1.json", "r+") as file:
        config = json.load(file)
        motor_1.instrument.set_config(config)
mapper = TwoDMapper(motor_1.conf_ui.x_amount, motor_1.conf_ui.y_amount, 0, 0, "motor 1",
                    ("RandValue", "val"))

log_to_screen()
launch_app(
    app, [
        ComponentInitialization(motor_1, 0, 0, 0, "motor 1"),
        ComponentInitialization(VirtualPlatina(), 1, 1, 0, "motor 2"),
    ], [
        ComponentInitialization(RandValue(), 1, 0, 1),
    ],
    [mapper],
    [mapper],
    coupling_ui_options={"enabled": True, "x": 1, "y": 1}
)
with open("motor_1.json", "w+") as file:
    json.dump(motor_1.instrument.get_config(), file)
