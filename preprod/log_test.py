import logging

from lantz.core.log import LOGGER, log_to_socket, get_logger

log_to_socket(logging.DEBUG, "127.0.0.1", 19996)
LOGGER.warning("Test")
get_logger("lantz.device").warning("test2")