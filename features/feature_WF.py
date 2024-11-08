import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, RATE, WF_SECONDS, SPLITBUFFER_FREQUENCY

def get_WF(streamAudio, freqReference, arrayFlutterStorage):

    freqDetected, freqDeviation, valueWowPercent, valueFlutterPercent, valueWF = [0, 0], 0, [0, 0], [0, 0], [0, 0]
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
        if (len(arrayFlutterStorage) > WF_SECONDS * SPLITBUFFER_FREQUENCY):
            arrayFlutterStorage.pop(0)

    for channelX in range(CHANNELS):
        FFTData = np.fft.fft(numData[channelX])
        arrayFreq = np.fft.fftfreq(len(FFTData), 1/RATE)
        arrayMagnitude = np.abs(FFTData[:len(FFTData)//2])
        indexFFTL = np.argmax(arrayMagnitude)

        freqDetected[channelX] = 0
        valueWowPercent[channelX] = 0
        valueFlutterPercent[channelX] = 0
        valueWF[channelX] = 0

        if np.max(arrayMagnitude) > 0:
            freqDetected[channelX] = abs(arrayFreq[indexFFTL])
            freqDeviation = freqDetected[channelX] - freqReference
            valueWowPercent[channelX] = (abs(freqDeviation) / freqReference) * 100
        
    if CHANNELS == 1:
        arrayFlutterStorage.append(abs(freqReference - freqDetected[0]))
        if (len(arrayFlutterStorage) > 1):
            valueFlutterPercent[0] = np.std(arrayFlutterStorage, ddof=1) / freqReference * 100
            valueWF[0] = (valueWowPercent[0] + valueFlutterPercent[0]) / 2
    else:
        arrayFlutterStorage.append([abs(freqReference - freqDetected[0]), abs(freqReference - freqDetected[1])])
        if (len(arrayFlutterStorage) > 1):
            for channelX in range(CHANNELS):
                arrayFlutterX = [arrayFlutterStorageX[channelX] for arrayFlutterStorageX in arrayFlutterStorage]
                valueFlutterPercent[channelX] = np.std(arrayFlutterX, ddof=1) / freqReference * 100
                valueWF[channelX] = (valueWowPercent[channelX] + valueFlutterPercent[channelX]) / 2

    return freqDetected, valueWowPercent, valueFlutterPercent, valueWF, arrayFlutterStorage