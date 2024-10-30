import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, RATE

def get_WF(streamAudio, freqReference):

    freqDetected, freqDeviation, valueWowPercent, valueFlutter, valueFlutterPercent, valueWF = [0, 0], 0, [0, 0], [0, 0], [0, 0], [0, 0]
    dataAudio = streamAudio.read(SMALL_CHUNK, exception_on_overflow=False)
    FFTwindow = np.hamming(LARGE_CHUNK)

    if CHANNELS == 1:
        bufferAudio = np.zeros((OVERLAP_COUNT, OVERLAP_SIZE), dtype=np.float32)
        dataPartial = np.frombuffer(dataAudio, dtype=np.float32)
    else:    
        bufferAudio = np.zeros((OVERLAP_COUNT, OVERLAP_SIZE, CHANNELS), dtype=np.float32)
        dataPartial = np.frombuffer(dataAudio, dtype=np.float32).reshape(-1, 2)
    indexBuffer = 0 

    bufferAudio[indexBuffer] = dataPartial
    indexBuffer = (indexBuffer + 1) % OVERLAP_COUNT
    
    if CHANNELS == 1:
        numData = [bufferAudio.flatten() * FFTwindow]
    else:
        numData = [bufferAudio[:, :, 0].flatten() * FFTwindow, bufferAudio[:, :, 1].flatten() * FFTwindow]

    for channelX in range(CHANNELS):
        FFTData = np.fft.fft(numData[channelX])
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