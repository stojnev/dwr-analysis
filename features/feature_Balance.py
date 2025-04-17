import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, WF_SECONDS, SPLITBUFFER_FREQUENCY
from utilities.functions import calculatePeakFreq, colorTextGreen, colorTextRed, colorTextYellow

def get_ChannelBalance(streamAudio, arrayFreqStorage, arrayAmpStorage):

    peakFreq, AMP = [0, 0], [0, 0]

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
        if (len(arrayFreqStorage) > WF_SECONDS * SPLITBUFFER_FREQUENCY):
            arrayFreqStorage.pop(0)
            arrayAmpStorage.pop(0)
    else: 
        arrayFreqStorage = []
        arrayAmpStorage = []
    
    if CHANNELS == 1:
        valuePeakFrequency, valueAmplitude, valueAmplitudeDB, valuePhaseDegrees = calculatePeakFreq(numData[0], 1)
        arrayFreqStorage.append(valuePeakFrequency)
        arrayAmpStorage.append(valueAmplitude)
    else:
        valuePeakFrequency1, valueAmplitude1, valueAmplitudeDB1, valuePhaseDegrees1 = calculatePeakFreq(numData[0], 1)
        valuePeakFrequency2, valueAmplitude2, valueAmplitudeDB2, valuePhaseDegrees2 = calculatePeakFreq(numData[1], 1)
        arrayFreqStorage.append([valuePeakFrequency1, valuePeakFrequency2])
        arrayAmpStorage.append([valueAmplitudeDB1, valueAmplitudeDB2])
    for channelX in range(CHANNELS):
        if CHANNELS == 1:
            arrayFreqX = arrayFreqStorage
            arrayAmpX = arrayFreqStorage
        else:
            arrayFreqX = [arrayFreqStorageX[channelX] for arrayFreqStorageX in arrayFreqStorage]
            arrayAmpX = [arrayAmpStorageX[channelX] for arrayAmpStorageX in arrayAmpStorage]

        peakFreq[channelX] = np.mean(arrayFreqX)
        AMP[channelX] = np.mean(arrayAmpX)

    return peakFreq, AMP, arrayFreqStorage, arrayAmpStorage