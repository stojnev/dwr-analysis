import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def get_WF(audioStream, freqReference):
    
    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    # Split the stereo stream in two channels.
    numDataM = [numData[0::2], numData[1::2]]

    FFTwindow = np.hanning(CHUNK)

    # Declare all the required variables as "two channel" arrays.
    FFTData = [0, 0], arrayFreq = [0, 0], arrayMagnitude = [0, 0], indexFFTL = [0, 0], freqDetected = [0, 0], freqDeviation = [0, 0], valueWowPercent = [0, 0], valueFlutter = [0, 0], valueFlutterPercent = [0, 0], valueWF = [0, 0]

    for channelX in range(CHANNELS):
        numDataM[channelX] = numDataM[channelX] * FFTwindow
        FFTData[channelX] = np.fft.fft(numDataM[channelX])
        arrayFreq[channelX] = np.fft.fftfreq(len(FFTData[channelX]), 1/RATE)
        arrayMagnitude[channelX] = np.abs(FFTData[channelX][:len(FFTData[channelX])//2])
        indexFFTL[channelX] = np.argmax(arrayMagnitude[channelX])
        freqDetected[channelX] = abs(arrayFreq[channelX][indexFFTL[channelX]])
        valueWowPercent[channelX] = (abs(freqDeviation[channelX]) / freqReference) * 100
        valueFlutter[channelX] = np.std(arrayMagnitude[channelX])
        valueFlutterPercent[channelX] = (valueFlutter[channelX] / np.max(arrayMagnitude[channelX])) * 100
        valueWF[channelX] = (valueWowPercent[channelX] + valueFlutterPercent[channelX]) / 2
    
    return freqDetected, valueWowPercent, valueFlutterPercent, valueWF