# Scientific Experiment Runner - Developer Documentation

This module provides a framework for developing and controlling hardware in a GUI application.

This readme is for developers that want to build with SER. If you want to see
how to operate a SER application, see the following documentation
[Scientific Experiment Runner - User Documentation](readme_user.md)

For spanish documentation see [Scientific Experiment Runner - Spanish](readme_es.md)

## Summary

The core model of the SER is based on integrating multiple devices that
need to operate in parallel to configure an experiment and observe its results.
This is achieved through a series of independent components, which are provided by
the developer and managed centrally by the SER. SER also provides a consistent surrounding
UI in which the component's UI is embedded, and a series of useful commands
for the user.

## Dependencies

### Lantz

The core dependency of the SER is [Lantz](https://github.com/lantzproject), which 
provides the base clases of Backend and Frontend as the backbone of the component
system. It is recommended that SER components are developed with Lantz
[drivers](https://github.com/lantzproject/lantz-drivers) and Lantz
[QT helper functions](https://github.com/lantzproject/lantz-qt).

## Model



## API Documentation

### 

### Developing Components

To primary tool necessary for using 

![Component Structure](/Documentation/UML%20Trabajo%20Profesional.png)

#### Instrument

#### Configuration UI

#### ProcessDataUI

#### FinalDataUI
