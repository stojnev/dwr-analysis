import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def get_WF(audioStream, freqReference):
    
    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.float32)

    # Split the stereo stream in two channels.
    if CHANNELS == 1:
        numDataM = []
        numDataM.append(numData)
    if CHANNELS == 2:
        numDataM = [numData[0::2], numData[1::2]]

    FFTwindow = np.hanning(CHUNK)

    # Declare the required variables as "stereo", two channel arrays.
    freqDetected, freqDeviation, valueWowPercent, valueFlutter, valueFlutterPercent, valueWF = [0, 0], 0, [0, 0], [0, 0], [0, 0], [0, 0]

    for channelX in range(CHANNELS):
        numDataM[channelX] = numDataM[channelX] * FFTwindow
        FFTData = np.fft.fft(numDataM[channelX])
        arrayFreq = np.fft.fftfreq(len(FFTData), 1/RATE)
        arrayMagnitude = np.abs(FFTData[:len(FFTData)//2])
        indexFFTL = np.argmax(arrayMagnitude)

        # Set basic values in case no audio data.
        freqDetected[channelX] = 0
        valueWowPercent[channelX] = 0
        valueFlutterPercent[channelX] = 0
        valueWF[channelX] = 0

        # Proceed with calculation provided audio data exists.
        if np.max(arrayMagnitude) > 0:
            freqDetected[channelX] = abs(arrayFreq[indexFFTL])
            freqDeviation = freqDetected[channelX] - freqReference
            valueWowPercent[channelX] = (abs(freqDeviation) / freqReference) * 100
            valueFlutter[channelX] = np.std(arrayMagnitude)
            valueFlutterPercent[channelX] = (valueFlutter[channelX] / np.max(arrayMagnitude)) * 100
            valueWF[channelX] = (valueWowPercent[channelX] + valueFlutterPercent[channelX]) / 2
    
    return freqDetected, valueWowPercent, valueFlutterPercent, valueWF