import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE
from utilities.functions import calculatePeakFrequency

def get_RPM(audioStream, TARGET_FREQUENCY, TARGET_RPM):

    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    FFTwindow = np.hanning(CHUNK)
    numData = numData * FFTwindow

    peakFreq = calculatePeakFrequency(numData)

    RPM = (peakFreq / TARGET_FREQUENCY) * TARGET_RPM

    return peakFreq, RPM
