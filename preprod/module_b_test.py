from lantz.core.log import LOGGER, log_to_screen
from logging import DEBUG


def fun():
    LOGGER.log(msg="tests", level=DEBUG)


if __name__ == "__main__":
    log_to_screen(DEBUG)
    fun()
