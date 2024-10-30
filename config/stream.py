import pyaudio

FORMAT = pyaudio.paFloat32
CHANNELS = 2
RATE = 44100
CHUNK = 16000
THRESHOLD = 100000
DEVICE = 0

SPLITBUFFER_RESOLUTION = 0.5 # Width of frequency bins, resolution wise, in Hz.
SPLITBUFFER_FREQUENCY = 10 # Frequency of update of data per second, in Hz.
HARMONIC_DEPTH = 5 # Number of harmonics to utilise in THD calculations.

LARGE_CHUNK = int(RATE // SPLITBUFFER_RESOLUTION)
SMALL_CHUNK = int(RATE // SPLITBUFFER_FREQUENCY)
OVERLAP_COUNT = int(LARGE_CHUNK // SMALL_CHUNK)
OVERLAP_SIZE = int(LARGE_CHUNK // OVERLAP_COUNT)
