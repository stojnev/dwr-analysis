import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE
from utilities.functions import calculateTHDN

def get_THDN(audioStream):

    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    # Split the stereo stream in two channels.
    if CHANNELS == 1:
        numDataM = []
        numDataM.append(numData)
    if CHANNELS == 2:
        numDataM = [numData[0::2], numData[1::2]]

    FFTwindow = np.hanning(CHUNK)
    
    # Declare the required variables as "stereo", two channel arrays.
    peakFreq, THDN, percentTHDN = [0, 0], [0, 0], [0, 0]

    for channelX in range(CHANNELS):
        numDataM[channelX] = numDataM[channelX] * FFTwindow
        peakFreq[channelX], THDN[channelX], percentTHDN[channelX] = calculateTHDN(numDataM[channelX])

    return peakFreq, THDN, percentTHDN
