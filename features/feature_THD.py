import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, HARMONIC_DEPTH, WF_SECONDS, SPLITBUFFER_FREQUENCY
from utilities.functions import calculateTHDN

def get_THDN(streamAudio, arrayTHDStorage):

    peakFreq, THDN, percentTHDN = [0, 0], [0, 0], [0, 0]

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
        if (len(arrayTHDStorage) > WF_SECONDS * SPLITBUFFER_FREQUENCY):
            arrayTHDStorage.pop(0)
    else:
        arrayTHDStorage = []


#    for channelX in range(CHANNELS):
#        peakFreq[channelX], THDN[channelX], percentTHDN[channelX] = calculateTHDN(numData[channelX], HARMONIC_DEPTH)

    peakFreq[0], THDN[0], percentTHDN[0] = calculateTHDN(numData[0], HARMONIC_DEPTH)
    if CHANNELS == 1:
        arrayTHDStorage.append([peakFreq[0], 0, THDN[0], 0, percentTHDN[0], 0])
    else:
        peakFreq[1], THDN[1], percentTHDN[1] = calculateTHDN(numData[1], HARMONIC_DEPTH)
        arrayTHDStorage.append([peakFreq[0], peakFreq[1], THDN[0], THDN[1], percentTHDN[0], percentTHDN[1]])


    return arrayTHDStorage
