import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, THRESHOLD, DEVICE
import os
import platform
import re

def clearConsole():
    systemX = platform.system()

    if systemX == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def calculatePeakFreq(numData, optionExpanded=0):
    FFTData = np.fft.rfft(numData)
    FFTFreqs = np.fft.rfftfreq(len(numData), d=1/RATE)
    arrayMagnitude = np.abs(FFTData)
    indexPeakFrequency = np.argmax(arrayMagnitude)
    valuePeakFrequency = FFTFreqs[indexPeakFrequency]
    valueAmplitude = arrayMagnitude[indexPeakFrequency]
    valueAmplitudeDB = 20 * np.log10(valueAmplitude + 1e-10)
    valuePhaseDegrees = np.degrees(np.angle(FFTData[indexPeakFrequency]))
    if optionExpanded == 1:
        return valuePeakFrequency, valueAmplitude, valueAmplitudeDB, valuePhaseDegrees
    else:
        return valuePeakFrequency

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

def getDINCorrectedWF(freqDeviation):
    arrayFrequencies = np.array([0.2, 0.315, 0.4, 0.63, 0.8, 1.0, 1.6, 2.0, 4.0, 6.3, 10, 20, 40, 63, 100, 200])
    arrayVoltageGains = np.array([0.02951209227, 0.1035142167, 0.177827941, 0.3801893963, 0.5011872336, 0.6165950019, 0.8128305162, 0.9015711376, 1, 0.9015711376, 0.7852356346, 0.5069907083, 0.301995172, 0.19498446, 0.1364583137, 0.07079457844])
    returnValue = 0
    if not (freqDeviation < arrayFrequencies[0] or freqDeviation > arrayFrequencies[-1]):
        returnValue = np.interp(freqDeviation, arrayFrequencies, arrayVoltageGains)
    return returnValue

def getChannelName(channelNumber):
    nameChannel = 'M'
    if CHANNELS > 1:
        if channelNumber == 1:
            nameChannel = 'L'
        if channelNumber == 2:
            nameChannel = 'R'
        if channelNumber > 2:
            nameChannel = channelNumber
    return nameChannel

def sanitizeCommaInput(stringX):
    stringSanitized = re.sub(r'[^0-9,]', '', stringX)
    stringSanitized = re.sub(r',+', ',', stringSanitized)
    return stringSanitized.strip(',')

def colorTextRed(stringX):
    return "\033[31m" + stringX + "\033[0m"

def colorTextGreen(stringX):
    return "\033[32m" + stringX + "\033[0m"

def colorTextYellow(stringX):
    return "\033[33m" + stringX + "\033[0m"