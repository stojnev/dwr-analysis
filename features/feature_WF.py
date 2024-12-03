import numpy as np
from config.stream import CHANNELS, SMALL_CHUNK, OVERLAP_COUNT, OVERLAP_SIZE, LARGE_CHUNK, RATE, WF_SECONDS, SPLITBUFFER_FREQUENCY
from config.stream import WOW_LOWER_THRESHOLD, WOW_UPPER_THRESHOLD, FLUTTER_THRESHOLD
from utilities.functions import getDINCorrectedWF

def get_WF(streamAudio, freqReference, arrayFlutterStorage):

    freqDetected, valueWowPercent, valueFlutterPercent, valueWowPercentWeighted, valueFlutterPercentWeighted, valueWF, valueWFW, valueWFRMS, valueWFWRMS, valueDifference = [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]
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
    else:
        arrayFlutterStorage = []

    for channelX in range(CHANNELS):
        FFTData = np.fft.fft(numData[channelX])
        arrayFreq = np.fft.fftfreq(len(FFTData), 1/RATE)
        arrayMagnitude = np.abs(FFTData[:len(FFTData)//2])
        indexFFTL = np.argmax(arrayMagnitude)

        freqDetected[channelX] = 0
        valueWowPercent[channelX] = 0
        valueFlutterPercent[channelX] = 0
        valueWF[channelX] = 0
        valueDifference[channelX] = 0

        if np.max(arrayMagnitude) > 0:
            freqDetected[channelX] = abs(arrayFreq[indexFFTL])
            valueDifference[channelX] = (freqReference - freqDetected[channelX]) / 100
        
    if CHANNELS == 1:
        arrayFlutterStorage.append(freqDetected[0])
    else:
        arrayFlutterStorage.append([freqDetected[0], freqDetected[1]])
    if (len(arrayFlutterStorage) > 1):
        for channelX in range(CHANNELS):
            if CHANNELS == 1:
                arrayFlutterX = arrayFlutterStorage
            else:
                arrayFlutterX = [arrayFlutterStorageX[channelX] for arrayFlutterStorageX in arrayFlutterStorage]
            freqDetectedMean =  np.mean(arrayFlutterX)
            arrayDeviation = arrayFlutterX - freqDetectedMean
            arrayWowD = arrayDeviation[arrayDeviation <= WOW_UPPER_THRESHOLD]
            arrayFlutterD = arrayDeviation[arrayDeviation > FLUTTER_THRESHOLD]
            
            if (len(arrayWowD) > 1):
                arrayWowDC = correctWFWeight(arrayWowD)
                valueWowPercent[channelX] = np.std(arrayWowD, ddof=1) / freqDetectedMean * 100
                valueWowPercentWeighted[channelX] = np.std(arrayWowDC, ddof=1) / freqDetectedMean * 100
            if (len(arrayFlutterD) > 1):
                arrayFlutterDC = correctWFWeight(arrayFlutterD)
                valueFlutterPercent[channelX] = np.std(arrayFlutterD, ddof=1) / freqDetectedMean * 100
                valueFlutterPercentWeighted[channelX] = np.std(arrayFlutterDC, ddof=1) / freqDetectedMean * 100
            valueWF[channelX] = (valueWowPercent[channelX] + valueFlutterPercent[channelX]) / 2
            valueWFW[channelX] = (valueWowPercentWeighted[channelX] + valueFlutterPercentWeighted[channelX]) / 2
            valueWFRMS[channelX] = np.sqrt(valueWowPercent[channelX] ** 2 + valueFlutterPercent[channelX] ** 2)
            valueWFWRMS[channelX] = np.sqrt(valueWowPercentWeighted[channelX] ** 2 + valueFlutterPercentWeighted[channelX] ** 2)

    return freqDetected, valueWowPercent, valueFlutterPercent, valueWowPercentWeighted, valueFlutterPercentWeighted, valueWF, valueWFW, valueWFRMS, valueWFWRMS, valueDifference, arrayFlutterStorage

def correctWFWeight(arrayWF):
    arrayReturn = []
    for arrayX in range(len(arrayWF)):
        correctedValue = getDINCorrectedWF(arrayWF[arrayX]) * arrayWF[arrayX]
        arrayReturn.append(correctedValue)
    return arrayReturn