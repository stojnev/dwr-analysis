import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, RATE
from utilities.functions import calculateProperPeakFrequency, getAmplitudeFromFrequency

def get_IMD(streamAudio, IMD_FREQ1, IMD_FREQ2):

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

    for channelX in range(CHANNELS):
        
        FFTData = np.fft.rfft(numData[channelX])
        arrayFrequencies = np.fft.rfftfreq(len(numData[channelX]), d=1/RATE)
        arrayAmplitudes = np.abs(FFTData)

        freqIMD = [
            IMD_FREQ1 + IMD_FREQ2,
            np.abs(IMD_FREQ1 - IMD_FREQ2),
            np.abs(2*IMD_FREQ1 - IMD_FREQ2),
            np.abs(2*IMD_FREQ2 - IMD_FREQ1),
            np.abs(3*IMD_FREQ1 - 2*IMD_FREQ2),
            np.abs(3*IMD_FREQ2 - 2*IMD_FREQ1)
        ]

        powerIMD = 0

        for indexIMD in freqIMD:
            powerIMD += getAmplitudeFromFrequency(indexIMD, arrayFrequencies, arrayAmplitudes)

        fundamentalPowerIMD1 = getAmplitudeFromFrequency(IMD_FREQ1, arrayFrequencies, arrayAmplitudes) ** 2

        fundamentalPowerIMD2 = getAmplitudeFromFrequency(IMD_FREQ2, arrayFrequencies, arrayAmplitudes) ** 2

        IMD[channelX] = np.sqrt(powerIMD) / np.sqrt(fundamentalPowerIMD1 + fundamentalPowerIMD2)
        
        freqIMD1[channelX] = calculateProperPeakFrequency(IMD_FREQ1, arrayFrequencies, arrayAmplitudes)
        freqIMD2[channelX] = calculateProperPeakFrequency(IMD_FREQ2, arrayFrequencies, arrayAmplitudes)

    return freqIMD1, freqIMD2, IMD