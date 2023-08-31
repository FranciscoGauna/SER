import lantz.core.log as lantz_log

# Internal components, not to be exposed
# This code is "inspired" by Lantz log method
# We take the same structure and just change the name to start with SER
# With a different hierarchy for logging
# Instead of logging by Frontend, Backend and Device
# The first element in the name should always be the Component Name

lantz_log.LOGGER = lantz_log.get_logger("SER")
LOGGER = lantz_log.LOGGER
log_to_screen = lantz_log.log_to_screen
log_to_socket = lantz_log.log_to_socket

# Naming scheme
# All always start with SER, important to make the handlers work
# Then the next element is the component name, for the core we use Core
# Then we use the name of the class
# Everything there should use PascalCase
