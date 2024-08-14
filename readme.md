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
are those who store that take the measurements once all of the configurable instruments
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

### View Controller

## API Documentation

### 

### Developing Components

To primary tool necessary for using 

![Component Structure](/Documentation/UML%20Trabajo%20Profesional.png)

#### Instrument

#### Configuration UI

#### ProcessDataUI

#### FinalDataUI
