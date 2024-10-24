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

def calculateTHDN(numData, harmonicDepth = 5):
    FFTdata = np.fft.fft(numData)
    arrayFrequency = np.fft.fftfreq(len(FFTdata), d=1/RATE)

    # Find the fundamental frequency.
    arrayMagnitude = np.abs(FFTdata)
    freqFundamentalIndex = np.argmax(arrayMagnitude[:len(FFTdata) // 2]) 
    freqFundamental = arrayFrequency[freqFundamentalIndex]
    powerFundamental = arrayMagnitude[freqFundamentalIndex] ** 2

    # Calculate harmonic frequencies and powers.
    arrayHarmonics = [freqFundamental * (i + 1) for i in range(harmonicDepth)]
    arrayHarmonicPowers = [arrayMagnitude[np.argmax((arrayFrequency[:len(FFTdata) // 2] >= singleHarmonic))] ** 2 for singleHarmonic in arrayHarmonics]
    powerHarmonic = 0

    for indexX, (singleHarmonic, powerH) in enumerate(zip(arrayHarmonics, arrayHarmonicPowers), start = 1):
        indexHarmonic = np.argmin(np.abs(arrayFrequency - singleHarmonic))
        powerCurrentHarmonic = np.abs(FFTdata[indexHarmonic]) ** 2
        if singleHarmonic > freqFundamental:
            powerHarmonic = powerHarmonic + powerCurrentHarmonic

    # Calculate THD+N.
    THDN = 0
    percentTHDN = 0
    if powerFundamental > 0:
        THDN = np.sqrt(powerHarmonic) / np.sqrt(powerFundamental)
        percentTHDN = calculatedBFromPercent(THDN)

    return freqFundamental, percentTHDN, THDN
