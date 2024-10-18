import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def get_WF(audioStream, freqReference):
    
    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    FFTwindow = np.hanning(CHUNK)
    numData = numData * FFTwindow

    FFTdata = np.fft.fft(numData)
    arrayFreq = np.fft.fftfreq(len(FFTdata), 1/RATE)

    arrayMagnitude = np.abs(FFTdata[:len(FFTdata)//2])

    indexFFT = np.argmax(arrayMagnitude)

    freqDetected = abs(arrayFreq[indexFFT])

    freqDeviation = freqDetected - freqReference

    valueWowPercent = (abs(freqDeviation) / freqReference) * 100

    valueFlutter = np.std(arrayMagnitude)
    valueFlutterPercent = (valueFlutter / np.max(arrayMagnitude)) * 100

    valueWF = (valueWowPercent + valueFlutterPercent) / 2
    
    return freqDetected, valueWowPercent, valueFlutterPercent, valueWF