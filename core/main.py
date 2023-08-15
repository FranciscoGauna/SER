import logging
from typing import Collection

from core.main_window import MainWindow
from core.interfaces import Component
from core.log import log_to_socket, LOGGER


# Dataclass
class ComponentInitialization:

    def __init__(self, component: Component, alignment: int, x: int, y: int):
        """
        This class provides an encapsulation of the data required by core to .

        :param str sender: The person sending the message
        :param str recipient: The recipient of the message
        :param str message_body: The body of the message
        """
        self.component = component
        self.alignment = alignment
        self.x = x
        self.y = y


def launch_app(components: Collection[Component]):
    # TODO: Parametrize logging
    log_to_socket(logging.DEBUG, "127.0.0.1", 19996)
    LOGGER.log(logging.DEBUG, "Test")
    #MainWindow(components)
