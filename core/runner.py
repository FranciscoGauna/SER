from typing import Collection

from .interfaces import Component

class Runner:
    """
    Model class at the center of the S.E.R.

    It has the responsibility of grabbing the configuration and executing an iteration of the program.
    This includes the parallelization of the execution
    The MainView window is the one that grabs this class and displays the gui attacked to the components
    """

