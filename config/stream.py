import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
THRESHOLD = 100000
DEVICE = 0

SPLITBUFFER_RESOLUTION = 0.5 # Width of frequency bins, resolution wise, in Hz.
SPLITBUFFER_FREQUENCY = 10 # Frequency of update of data per second, in Hz.
HARMONIC_DEPTH = 5 # Number of harmonics to utilise in THD calculations.
WF_SECONDS = 5 # Size in seconds of the window used for W&F calculations. Use a value of 0 to have no windowing.

LARGE_CHUNK = int(RATE / SPLITBUFFER_RESOLUTION)
SMALL_CHUNK = int(RATE / SPLITBUFFER_FREQUENCY)
OVERLAP_COUNT = int(LARGE_CHUNK / SMALL_CHUNK)
OVERLAP_SIZE = int(LARGE_CHUNK / OVERLAP_COUNT)

WOW_LOWER_THRESHOLD = 0.5
WOW_UPPER_THRESHOLD = 4.0
FLUTTER_THRESHOLD = 4.0
