# dŵr Analysis

"dŵr Analysis" ("dŵr") is a set of scripts and snippets that aim to ease and aid turntable system setup utilizing readily available test records.

At the moment, it is a fairly broken set of code snippets, moving forward at a snail's pace.

Hopefully to resemble a usable application at some point in time.

## Requirements

Currently only as a set of Python scripts. Dependencies within `requirements.txt`.

## Usage

Run `main.py` and be presented with a list of currently supported functions, i.e. features.

## Features

1. List Audio Devices will display all available audio I/O devices on the current machine.
2. Get RPM will listen for a specific target tone and calculate RPM based on readings with defaults set at 3,150Hz and 33.3333.
3. Get W&F will listen for a specific target tone and calculate wow, flutter and joing W&F with defaults set at 3,150Hz.
4. Get IMD will listen for a combination of two target tones and calculate IMD, with defaults set at 60Hz and 4,000Hz.