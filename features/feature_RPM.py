import numpy as np
from config.stream import CHANNELS, RATE, CHUNK, THRESHOLD
from config.stream import SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE
from utilities.functions import calculatePeakFreq

def get_RPM(streamAudio, TARGET_FREQUENCY, TARGET_RPM):

    peakFreq, RPM = [0, 0], [0, 0]

    dataAudio = streamAudio.read(SMALL_CHUNK, exception_on_overflow=False)

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
        numData = [bufferAudio.flatten()]
    else:
        numData = [bufferAudio[:, :, 0].flatten(), bufferAudio[:, :, 1].flatten()]
   
    for channelX in range(CHANNELS):
        peakFreq[channelX] = calculatePeakFreq(numData[channelX])
        RPM[channelX] = (peakFreq[channelX] / TARGET_FREQUENCY) * TARGET_RPM

    return peakFreq, RPM
