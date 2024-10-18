import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def calculatePeakFrequency(numData):
    FFTdata = np.fft.fft(numData)
    arrayMagnitude = np.abs(FFTdata[:len(FFTdata) // 2])
    peakIndex = np.argmax(arrayMagnitude)
    peakFreq = peakIndex * RATE / CHUNK
    return peakFreq
