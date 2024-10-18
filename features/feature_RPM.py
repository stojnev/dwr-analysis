import numpy as np
import pyaudio
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def calculate_peak_frequency(numData):
    FFTdata = np.fft.fft(numData)
    arrayMagnitude = np.abs(FFTdata[:len(FFTdata) // 2])
    peakIndex = np.argmax(arrayMagnitude)
    peakFreq = peakIndex * RATE / CHUNK
    return peakFreq

def get_RPM(audioStream, TARGET_FREQUENCY, TARGET_RPM):

    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    # Apply Hanning window
    FFTwindow = np.hanning(CHUNK)
    numData = numData * FFTwindow
 
    # Calculate peak frequency
    peakFreq = calculate_peak_frequency(numData)

    # Calculate RPM based on the peak frequency
    RPM = (peakFreq / TARGET_FREQUENCY) * TARGET_RPM

    return peakFreq, RPM  # Return the values
