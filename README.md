# dŵr Analysis

"dŵr Analysis" ("dŵr") is a set of scripts and snippets that aim to ease and aid turntable system setup utilizing readily available test records.

At the moment, it is a fairly broken set of code snippets, moving forward at a snail's pace.

Hopefully to resemble a usable application at some point in time.

## Requirements

Currently only as a set of Python scripts. Dependencies within `requirements.txt`.

## Usage

Run `main.py` and be presented with a list of currently supported functions, i.e. features.

## Features

With the *semblance* of a user interface, all possible functionalities are now listed within the `config\functionalities\test_functions.json`. That said, the *available* functionalities depend on the choices one makes regarding the available test records.

When first running, the following options are available:

A. **List Audio Devices** will display all available audio I/O devices on the current machine.
B. **Get Current Test Record Configuration** will list all the test records you had selected you own.
C. **Change Test Record Configuration** will allow you to select which test records you own.

After this, the script will automatically determine which functionalities are available to you.

Note that the list of supported test records resides within `config\functionalities\test_records.json`.

## Parameters

Most of the parameters ar set within the `config/stream.py` file.

At the time of writing, default settings have it expecting two channels, a 44.1kHz sample rate, the default device, and a 4Hz point for W&F curve centering. Change at your own peril.

*This is very much a work in progress. Note there still may be many validation issues across the board with pending fixes.*