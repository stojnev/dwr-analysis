# dŵr Analysis

"dŵr Analysis" ("dŵr") is a set of scripts and snippets that aim to ease and aid turntable system setup utilizing readily available test records.

At the moment, it is a fairly broken set of code snippets, moving forward at a snail's pace.

Hopefully to resemble a usable application at some point in time.

## Requirements

Currently only as a set of Python scripts. Dependencies within `requirements.txt`.

## Usage

Run `main.py` and be presented with a list of currently supported functions, i.e. features.

## Features

1. **List Audio Devices** will display all available audio I/O devices on the current machine.
2. **Get RPM** calculates RPM based on `TARGET_RPM` and listening to `WF_FREQUENCY`.
3. **Get W&F** calculates wow, flutter and joint W&F based on listening to `WF_FREQUENCY`.
4. **Get IMD** calculates IMD based on listening to `IMD_FREQ1` and `IMD_FREQ2`.
5. **Get THD+N** calculates THD+N based on the input stream.

## Parameters

Most of the parameters ar set within the `config/stream.py` file.

At the time of writing, default settings have it expecting two channels, a 44.1kHz sample rate, the default device, and a 4Hz point for W&F curve centering. Change at your own peril.

This is very much a work in progress. Note there still may be many validation issues across the board with pending fixes.