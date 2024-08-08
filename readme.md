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

#### Instruments

Instruments are the class meant to represent a single piece of hardware in our model.
Examples include: a function generator, a translation stage or a Digital to Analog Converter.

#### Coupling

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
