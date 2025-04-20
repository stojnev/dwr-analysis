import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, RATE, WF_SECONDS, SPLITBUFFER_FREQUENCY
from utilities.functions import calculateProperPeakFrequency, getAmplitudeFromFrequency

def get_IMD(streamAudio, IMD_FREQ1, IMD_FREQ2, arrayIMDStorage, harmonicDepth = 5):

    IMD, freqIMD1, freqIMD2 = [0, 0], [0, 0], [0, 0]

    dataAudio = streamAudio.read(SMALL_CHUNK, exception_on_overflow=False)
    FFTwindow = np.hamming(LARGE_CHUNK)

    if CHANNELS == 1:
        bufferAudio = np.zeros((OVERLAP_COUNT, OVERLAP_SIZE), dtype=np.int16)
        dataPartial = np.frombuffer(dataAudio, dtype=np.int16)
    else:    
        bufferAudio = np.zeros((OVERLAP_COUNT, OVERLAP_SIZE, CHANNELS), dtype=np.int16)
        dataPartial = np.frombuffer(dataAudio, dtype=np.int16).reshape(-1, 2)
    indexBuffer = 0 

    bufferAudio[indexBuffer] = dataPartial
    indexBuffer = (indexBuffer + 1) % OVERLAP_COUNT
    
    if CHANNELS == 1:
        numData = [bufferAudio.flatten() * FFTwindow]
    else:
        numData = [bufferAudio[:, :, 0].flatten() * FFTwindow, bufferAudio[:, :, 1].flatten() * FFTwindow]

    if (WF_SECONDS * SPLITBUFFER_FREQUENCY) > 0:
        if (len(arrayIMDStorage) > WF_SECONDS * SPLITBUFFER_FREQUENCY):
            arrayIMDStorage.pop(0)
    else:
        arrayIMDStorage = []

    for channelX in range(CHANNELS):
        
        FFTData = np.fft.rfft(numData[channelX])
        arrayFrequencies = np.fft.rfftfreq(len(numData[channelX]), d=1/RATE)
        arrayAmplitudes = np.abs(FFTData)

        freqIMD = []
        for indexF in range(0, harmonicDepth):
            modifierL = 1 + indexF
            modifierR = indexF
            if indexF == 0:
                modifierR = 1
                freqIMD.append(np.abs(modifierL * IMD_FREQ1 + modifierR * IMD_FREQ2))
            else:
                freqIMD.append(np.abs(modifierL * IMD_FREQ1 - modifierR * IMD_FREQ2))
            freqIMD.append(np.abs(modifierL * IMD_FREQ2 - modifierR * IMD_FREQ1))
        
        powerIMD = 0

        for indexIMD in freqIMD:
            powerIMD += getAmplitudeFromFrequency(indexIMD, arrayFrequencies, arrayAmplitudes)

        fundamentalPowerIMD1 = getAmplitudeFromFrequency(IMD_FREQ1, arrayFrequencies, arrayAmplitudes) ** 2

        fundamentalPowerIMD2 = getAmplitudeFromFrequency(IMD_FREQ2, arrayFrequencies, arrayAmplitudes) ** 2

        IMD[channelX] = np.sqrt(powerIMD) / np.sqrt(fundamentalPowerIMD1 + fundamentalPowerIMD2)
        
        freqIMD1[channelX] = calculateProperPeakFrequency(IMD_FREQ1, arrayFrequencies, arrayAmplitudes)
        freqIMD2[channelX] = calculateProperPeakFrequency(IMD_FREQ2, arrayFrequencies, arrayAmplitudes)

    if CHANNELS == 1:
        arrayIMDStorage.append([freqIMD1[0], 0, freqIMD2[0], 0, IMD[0] * 100, 0])
    else:
        arrayIMDStorage.append([freqIMD1[0], freqIMD1[1], freqIMD2[0], freqIMD2[1], IMD[0] * 100, IMD[1] * 100])

    return arrayIMDStorage