# Scientific Experiment Runner - Developer Documentation

This module provides a framework for developing and controlling hardware in a GUI application.
This readme is for developers that want to build with the Scientific Experiment Runner
(SER).

For spanish documentation see [Scientific Experiment Runner - Spanish](readme_es.md)

## Summary

The core model of the SER is based on integrating multiple devices that
need to operate in parallel to configure an experiment and observe its results.
This is achieved through a series of independent components, which are provided by
the developer and managed centrally by the SER. SER also provides a consistent surrounding
UI in which the component's UI is embedded, and a series of useful commands
for the user.

Example use case: coordinating a translation stage containing a sample, 
a probing laser heating the material and a lock-in amplifier to measure the laser distortion.

Example Screenshots of the demo application:

![Configuration Screen](/Documentation/App%20Conf%20Screenshot.png)

![Run Screen](/Documentation/App%20Progress%20Screenshot.png)

![Data Screen](/Documentation/App%20Data%20Screenshot.png)

## Dependencies

A pip requirements file is provided, with a `frozenreqs.txt` file specifying the
version with which it was tested. The python version used was 3.11.


### Lantz

The core dependency of the SER is [Lantz](https://github.com/lantzproject), which 
provides the base clases of Backend and Frontend as the backbone of the component
system. It is recommended that SER components are developed with Lantz
[drivers](https://github.com/lantzproject/lantz-drivers) and Lantz
[Qt helper functions](https://github.com/lantzproject/lantz-qt).

### Qt

For the development of the user graphical interface SER we utilize the 
[QT Framework](https://doc.qt.io/qt-5/qtgui-index.html) through its python bindings
called [PyQt](https://pypi.org/project/PyQt5/). For the development of interfaces it 
is recommended the [Qt gui designer application](https://doc.qt.io/qt-6/qtdesigner-manual.html)
, that can be downloaded through PyPi with [pyqt5-tools](https://pypi.org/project/pyqt5-tools/).

## Testing

There are unit test available for components in the model. 
These can be run with `python -m pytest tests`.

There is also available a sample program to see the interface, available with
`python main.py`

## Architecture

The application is designed with a Model View Controller model, with Qt handling
the View Controller part.

### Model

The core purpose of the model is to coordinate the different configurations for each
device in order to take the measurements. Each device can provide a series of "points"
that need to configured in the device to take the sample. Consider the Summary's example case:
the sample needs to be measured at different place and with different frequencies
from the laser probe. SER in a multithreaded fashion handles giving each instrument
the correct argument and storing the result.

![UML Activity Diagram](/Documentation/UML%20Run%20Activity%20Diagram.png)

#### Instruments

Instruments are the class meant to represent a single piece of hardware in our model.
Examples include: a function generator, a translation stage or a Digital to Analog Converter.
Each device can be categorized in either a configurable instrument or observable instrument.
Configurable instruments are those who need to be set up before a measure is taken. These
are the devices that provide "points" for configuration to the SER. In our
Summary's example case the function generator and translation unit are the configurable 
instruments. The other kind of instruments are those which are observable. These instruments
are those who store that take the measurements once all the configurable instruments
are observed. In our example case the lock-in amplifier would be the observable
instrument.

#### Coupling

Each configurable instrument has a parameter called coupling. This parameter
dictates the pattern in which the "points" provided by each configurable device
are sent to each device. The device with the higher coupling value will iterate
over the points first. If two devices share the same coupling value, they will be coupled
meaning they receive the point at the same time. Consider this example for our use case:
we have the translation unit providing the points (1mm, 2mm) and the function generator
providing the frequencies (10Hz, 100Hz). If the function generator has a higher coupling
value, the resulting configurations will look like this:
(1mm, 10Hz) -> (1mm, 100Hz) -> (2mm, 10Hz) -> (2mm, 100Hz). For more examples, see 
the [test file for the arg tracker](tests/generator_test.py)

#### Sequence and Runs

When the user is configuring the experiment, they may chain multiple different runs
in a sequence. Each run has its own configuration data. The scheduled runs can be
seen in a list at the bottom of the application. The User can also save them to disk
through a series of controls under "Load Configuration". During execution, at the 
beginning of each run SER loads the configuration into the components.

#### Logging

Logging is handled through the Lantz library logging core. As such it is recommended
developers read its documentation for handling.

#### Profiling

If you are having issues with performance and need to run a profiler
of your module in execution, the module can run in profiling mode by setting to
true the environment variable `ENABLE_PROFILING`. This will create a profile
file for each execution

### View Controller

Each component has an independent UI that is tasked with display its configuration parameters
to the user and allowing to change them as necessary. These UIs are developed in the
QT framework. In general, it's recommended that it's a groupbox that includes the name of
the device as the title, and it be created with the QT designer application. For
ease of use, we utilize the helper functions provided by lantz that allow automatic connection
between its feats and QT widgets and loading up a .ui file as a widget in the Frontend 
lantz class.

Example of the application with:

![Configuration Screen](/Documentation/App%20Conf%20Screenshot.png)

## API Documentation

### Launch Functions

    get_main_widget(configurable_components: Collection[src.SER.interfaces.component.ComponentInitialization], observable_components: Collection[src.SER.interfaces.component.ComponentInitialization], run_data_ui: Collection[src.SER.interfaces.user_interface.ProcessDataUI], final_data_ui: Collection[src.SER.interfaces.user_interface.FinalDataUI], coupling_ui_options: dict[str, typing.Any] = {}, conf_folder='.', out_folder='.', locale='en') -> PyQt5.QtWidgets.QWidget
        This function creates a widget that contains the SER. The widget loads the configuration ui provided by the
        components and can be interacted by the user.

        :param configurable_components: List of ComponentInitialization that include ConfigurableInstrument
        :param observable_components: List of ComponentInitialization that include ObservableInstrument
        :param run_data_ui: List of ProcessDataUI that reads the data and displays it as the experiment is running
        :param final_data_ui: List of FinalDataUI that reads the data and displays it after the experiment is finished
        :param coupling_ui_options: Dictionary with data to initialize the gui that changes the coupling. It should contain
        'enabled' bool, 'x' int, 'y' int, indicating if it needs to be enabled and the coordinated respectively.
        :param conf_folder: Direction to a folder where to open the save dialog for configuration files by default
        :param out_folder: Direction to a folder where to open the save dialog for output files by default
        :param locale: Value indicating what language to display the interface. 'en' for english and 'es' for spanish
        :return: A QWidget that can be embedded in your QT application.

    launch_app(app: PyQt5.QtWidgets.QApplication, configurable_components: Collection[src.SER.interfaces.component.ComponentInitialization], observable_components: Collection[src.SER.interfaces.component.ComponentInitialization], run_data_ui: Collection[src.SER.interfaces.user_interface.ProcessDataUI], final_data_ui: Collection[src.SER.interfaces.user_interface.FinalDataUI], coupling_ui_options: dict[str, typing.Any] = {}, conf_folder='.', out_folder='.', locale='en')
        This function uses the widget created by get_main_widget(...) to create the main QT application.

        :param app: QApplication object in which to run the app. It's necessary to provide as components cannot be
        created without a running QApplication in the background.
        :param configurable_components: List of ComponentInitialization that include ConfigurableInstrument
        :param observable_components: List of ComponentInitialization that include ObservableInstrument
        :param run_data_ui: List of ProcessDataUI that reads the data and displays it as the experiment is running
        :param final_data_ui: List of FinalDataUI that reads the data and displays it after the experiment is finished
        :param coupling_ui_options: Dictionary with data to initialize the gui that changes the coupling. It should contain
        'enabled' bool, 'x' int, 'y' int, indicating if it needs to be enabled and the coordinated respectively.
        :param conf_folder: Direction to a folder where to open the save dialog for configuration files by default
        :param out_folder: Direction to a folder where to open the save dialog for output files by default
        :param locale: Value indicating what language to display the interface. 'en' for english and 'es' for spanish
        :return: None. This will return when the user closes the app.

### Developing Components

The components that the launch function requires are to be provided by the user, 
which most follow the following structure.

![Component Structure](/Documentation/UML%20Trabajo%20Profesional.png)

The component is created by inheriting either ObservableInstrument and ConfigurableInstrument
and inheriting ConfigurationUI and wrapping them in a Component and ComponentInitialization.

    class ComponentInitialization:
        name: str  # The name of the component, used to distinguish the different components for the data
    
        def __init__(self, component: Component, coupling: int, x: int, y: int, name: str = None):
            This class provides a wrapper for the component, allowing it to have identifiable information distinct
            from the other components. This information is provided as parameters for this constructor.
    
            :param component: The component to be wrapped.
            :param coupling: The coupling of the component. See tests/generator_test.py for a detailed explanation.
            :param x: The x coordinate for the configuration ui to be displayed in the configuration screen grid.
            :param y: The y coordinate for the configuration ui to be displayed in the configuration screen grid.
            :param name: The unique name for the component. If multiple devices with the same name are provided an exception
            will be raised.

#### Instrument

    class Instrument(Backend):
        Class handling one or multiple devices, their configuration between runs and providing the variable documentation
        and points over which the device will iterate over the course of the experiment

        Note that the Backend class has an initialize method that gets executed each time a run is started
        if you need to update a parameter between runs, you can overload it and utilize it

        def get_config(self) -> Dict:
            This is used to save the configration parameters for each run. The values are saved on a json format when
            serialized in a file format. As such, return only objects that can be saved in that format.
    
            :return: a dictionary of configuration parameters and their values.
    
        def set_config(self, config: Dict) -> None:
            This is used to restore the configration parameters for each run. The values are saved on a json format when
            serialized in a file format. As such, return only objects that can be saved in that format.
            
        def variable_documentation(self) -> Dict[str, str]:
            This method should return a string containing the documentation for each kind of variable, including
            what it represents, what is the range of value and what is the unit.
    
            :return: a dictionary of variable names and their documentation.
    
        def stop(self) -> None:
            This method gets called if the experiment stopped prematurely by the user. If that's the case, do any
            procedures necessary to stop the instrument
    
    
    class ObservableInstrument(Instrument):
    
        def observe(self) -> Dict[str, Any]:
            This method gets called on each iteration points of the experiment.
    
            :return: a dictionary of observable parameters and their values.
    
    
    class ConfigurableInstrument(Instrument):
        coupling: int # Stores the coupling level. 
    
        def set_config(self, config: Dict):
            This is used to restore the configration parameters for each run. The values are saved on a json format when
            serialized in a file format. As such, return only objects that can be saved in that format. The super
            call for this function includes coupling, so it should be called on reimplementation.
    
        def get_config(self) -> Dict:
            This is used to save the configration parameters for each run. The values are saved on a json format when
            serialized in a file format. As such, return only objects that can be saved in that format. The super
            call for this function includes coupling, so it should be called on reimplementation.
    
            :return: a dictionary of configuration parameters and their values.
    
        def configure(self, *args) -> Dict[str, Any]:
            This method gets called on each iteration points of the experiment. It receives an unrolled tuple,
            so you can replace *args with your arguments.
            
            :return: a dictionary of relevant parameters and their values.
    
        def get_points(self) -> Generator[Tuple, None, None]:
            The function get_points is tasked with providing the points a component will use during its execution.
            The way it does this is through python Generators, as the task reads the task point by point. You can also
            provide other iterators that support next(_) and StopIteration.
    
            If 2 components are coupled AKA they both move simultaneously, they need to yield the same amount of points.
            Not respecting this is undefined behaviour
            :return: Generator with the amount of desired points
    
        def point_amount(self) -> int:
            :return: the amount of points this instrument generates with the Generator from get_points

#### Configuration UI

    class ConfigurationUI(Frontend):
        """This class represents a Configuration User Interface. It's used before the start of the experiment, and it's
        used to set up the instrument before execution and provide the points during which the experiment is executed."""
    
        # This is a recommendation, you can rename the instrument to something else
        instrument: Instrument
    
        # path to the ui file you want to load. The format is either a string or a tuple with the folders of the path
        # ex: "ui/example.ui" or ("ui", "example.ui")
        gui: Union[str, tuple] 

#### ProcessDataUI

    class ProcessDataUI(Frontend):
        This class represents the User Interface that displays the data from experiment during its execution.
        It gets updated at the end of each iteration with the method add_data.
    
        # These are used by the gui to load its position
        x: int
        y: int
    
        def __init__(self, x, y, parent=None, backend=None):
            :param x: The x coordinate for the process ui to be displayed in the progress screen grid.
            :param y: The y coordinate for the process ui to be displayed in the progress screen grid.
            :param parent: Sent to the Frontend Construct. See Lantz for more information.
            :param backend: Sent to the Frontend Construct. See Lantz for more information.

        def initialize(self):
            This method gets run by the ui manager (SER/ui/process_ui_manager.py) each time a new run is started.
            Use it to reset the status of the ui to an empty one without data.
    
        def add_data(self, data: List[Dict[str, Dict[str, Any]]]):
            This method gets run periodically by the ui manager. The data is in the following format.
            [
                {"component 1 name": {var1 : value1, var2 : value2, ...}, ...},  # This corresponds to one iteration
                {"component 1 name": {var1 : value3, var2 : value4, ...}, ...},  # of the instrument configuration cycle
            ]
    
            Component data for configuration devices is added only if that device was configured during this iteration.
            Due to this is it strongly recommended to store the previous value if it's needed for display calculations.
            The variables and values depend on what is given by the observe and configure methods in the components
            provided.

#### FinalDataUI

    class FinalDataUI(Frontend):
        This class represents the User Interface that displays the data from experiment, once it has concluded.
        It displays only the data from the last run in the sequence.
    
        # These are used by the gui to load its position
        x: int
        y: int
    
        def __init__(self, x, y, parent=None, backend=None):
            :param x: The x coordinate for the process ui to be displayed in the data screen grid.
            :param y: The y coordinate for the process ui to be displayed in the data screen grid.
            :param parent: Sent to the Frontend Construct. See Lantz for more information.
            :param backend: Sent to the Frontend Construct. See Lantz for more information.
    
        def set_data(self, data: List[Dict[str, Dict[str, Any]]]):
            This method gets run once at the end by the ui manager. The data is in the following format.
            [
                {"component 1 name": {var1 : value1, var2 : value2, ...}, ...},  # This corresponds to one iteration
                {"component 1 name": {var1 : value3, var2 : value4, ...}, ...},  # of the instrument configuration cycle
            ]
    
            The variables and values depend on what is given by the observe and configure methods in the components
            provided.
