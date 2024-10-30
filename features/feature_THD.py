import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, HARMONIC_DEPTH
from utilities.functions import calculateTHDN

def get_THDN(streamAudio):

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

    for channelX in range(CHANNELS):
        peakFreq[channelX], THDN[channelX], percentTHDN[channelX] = calculateTHDN(numData[channelX], HARMONIC_DEPTH)

    return peakFreq, THDN, percentTHDN
