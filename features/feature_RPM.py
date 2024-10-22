import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE
from utilities.functions import calculatePeakFrequency

def get_RPM(audioStream, TARGET_FREQUENCY, TARGET_RPM):

    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    # Split the stereo stream in two channels.
    numDataM = [numData[0::2], numData[1::2]]

    FFTwindow = np.hanning(CHUNK)
    
    peakFreq, RPM = [0, 0], [0, 0]
    for channelX in range(CHANNELS):
        numDataM[channelX] = numDataM[channelX] * FFTwindow
        peakFreq[channelX] = calculatePeakFrequency(numDataM[channelX])
        RPM[channelX] = (peakFreq[channelX] / TARGET_FREQUENCY) * TARGET_RPM

    return peakFreq, RPM
