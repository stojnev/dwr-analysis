import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def calculatePeakFreq(numData):
    FFTValues = np.fft.rfft(numData)
    peakIndex = np.argmax(np.abs(FFTValues))
    return peakIndex * (RATE / len(numData))

def calculatedBFromPercent(percentValue):
    return 20 * np.log10(percentValue)

def calculateTHDN(numData, harmonicDepth = 5):
    FFTdata = np.fft.fft(numData)
    arrayFrequency = np.fft.fftfreq(len(FFTdata), d=1/RATE)

    arrayMagnitude = np.abs(FFTdata)
    freqFundamentalIndex = np.argmax(arrayMagnitude[:len(FFTdata) // 2]) 
    freqFundamental = arrayFrequency[freqFundamentalIndex]
    powerFundamental = arrayMagnitude[freqFundamentalIndex] ** 2

    arrayHarmonics = [freqFundamental * (i + 1) for i in range(harmonicDepth)]
    arrayHarmonicPowers = [arrayMagnitude[np.argmax((arrayFrequency[:len(FFTdata) // 2] >= singleHarmonic))] ** 2 for singleHarmonic in arrayHarmonics]
    powerHarmonic = 0

    for indexX, (singleHarmonic, powerH) in enumerate(zip(arrayHarmonics, arrayHarmonicPowers), start = 1):
        indexHarmonic = np.argmin(np.abs(arrayFrequency - singleHarmonic))
        powerCurrentHarmonic = np.abs(FFTdata[indexHarmonic]) ** 2
        if singleHarmonic > freqFundamental:
            powerHarmonic = powerHarmonic + powerCurrentHarmonic

    THDN = 0
    percentTHDN = 0
    if powerFundamental > 0:
        THDN = np.sqrt(powerHarmonic) / np.sqrt(powerFundamental)
        percentTHDN = calculatedBFromPercent(THDN)

    return freqFundamental, percentTHDN, THDN

def calculateProperPeakFrequency(frequencyTarget, arrayFrequencies, arrayAmplitudes):
    indexProper = np.argmin(np.abs(arrayFrequencies - frequencyTarget))
    placeholderX = 0
    for indexF in range(indexProper - 20, indexProper + 20):
        if arrayAmplitudes[indexF] > placeholderX:
            placeholderX = arrayAmplitudes[indexF]
            indexProper = indexF
    return arrayFrequencies[indexProper]

def getAmplitudeFromFrequency(frequencyTarget, arrayFrequencies, arrayAmplitudes):
    return arrayAmplitudes[np.argmin(np.abs(arrayFrequencies - frequencyTarget))]