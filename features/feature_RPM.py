import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, WF_SECONDS, SPLITBUFFER_FREQUENCY
from utilities.functions import calculatePeakFreq, colorTextGreen, colorTextRed, colorTextYellow

def get_RPM(streamAudio, TARGET_FREQUENCY, TARGET_RPM, arrayRPMStorage):

    peakFreq, RPM = [0, 0], [0, 0]

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
        if (len(arrayRPMStorage) > WF_SECONDS * SPLITBUFFER_FREQUENCY):
            arrayRPMStorage.pop(0)
    else: 
        arrayRPMStorage = []
    
    if CHANNELS == 1:
        arrayRPMStorage.append(calculatePeakFreq(numData[0]))
    else:
        arrayRPMStorage.append([calculatePeakFreq(numData[0]), calculatePeakFreq(numData[1])])
    for channelX in range(CHANNELS):
        if CHANNELS == 1:
            arrayRPMX = arrayRPMStorage
        else:
            arrayRPMX = [arrayRPMStorageX[channelX] for arrayRPMStorageX in arrayRPMStorage]

        peakFreq[channelX] = np.mean(arrayRPMX)
        RPM[channelX] = (peakFreq[channelX] / TARGET_FREQUENCY) * TARGET_RPM

    return peakFreq, RPM, arrayRPMStorage

def calculateRPMDeviation(currentRPM, TARGET_RPM, acceptedDeviation = 0, calculatePercentage = False):
    deviationX = currentRPM - TARGET_RPM
    percentSign = ""
    if calculatePercentage:
        deviationX = deviationX / TARGET_RPM * 100
        deviationBad = abs(deviationX) > acceptedDeviation
        percentSign = "%"
    else:
        deviationBad = abs(deviationX / TARGET_RPM * 100) > acceptedDeviation
    if (acceptedDeviation > 0 and deviationBad):
        return colorTextRed(f"{deviationX:+.4f}{percentSign}")
    else:
        return colorTextGreen(f"{deviationX:+.4f}{percentSign}")