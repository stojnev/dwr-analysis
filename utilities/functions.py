import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def calculatePeakFrequency(numData, nextPeak=0):
    FFTdata = np.fft.fft(numData)
    arrayMagnitude = np.abs(FFTdata[:len(FFTdata) // 2])
    peakIndex = np.argmax(arrayMagnitude)
    peakFreq = peakIndex * RATE / CHUNK
    if nextPeak > 0:
        for peakX in range(nextPeak):
            maskedMagnitude = np.delete(arrayMagnitude, peakIndex)
            nextPeakIndex = np.argmax(maskedMagnitude)
            if nextPeakIndex >= peakIndex:
                nextPeakIndex += 1
        nextPeakFreq = nextPeakIndex * RATE / CHUNK
        arrayMagnitude = maskedMagnitude
        peakFreq = nextPeakFreq
    return peakFreq

def calculatedBFromPercent(percentValue):
    return 20 * np.log10(percentValue)