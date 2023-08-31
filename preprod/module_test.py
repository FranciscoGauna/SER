import lantz.core.log as blah
from module_b_test import fun, log_to_screen, DEBUG

blah.LOGGER = None

log_to_screen(DEBUG)
fun()
