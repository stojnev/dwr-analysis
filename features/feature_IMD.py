import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

def get_IMD(audioStream, IMD_FREQ1, IMD_FREQ2):

    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.int16)

    FFTwindow = np.hanning(CHUNK)
    numData = numData * FFTwindow

    FFTdata = np.fft.fft(numData)
    arrayFreq = np.fft.fftfreq(len(FFTdata), 1/RATE)

    arrayMagnitude = np.abs(FFTdata[:len(FFTdata)//2])
    indexIMD1 = np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - IMD_FREQ1))
    indexIMD2 = np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - IMD_FREQ2))

    fundamentalPowerIMD1 = arrayMagnitude[indexIMD1] ** 2
    fundamentalPowerIMD2 = arrayMagnitude[indexIMD2] ** 2

    powerIMD = 0

    # Perform some aliasing on the third order of IMD products.
    thirdorderIMD = [np.abs(3*IMD_FREQ1 - 2*IMD_FREQ2), np.abs(3*IMD_FREQ2 - 2*IMD_FREQ1)]
    if thirdorderIMD[0] > RATE / 2:
        thirdorderIMD[0] = np.abs(thirdorderIMD[0] - RATE / 2)
    if thirdorderIMD[1] > RATE / 2:
        thirdorderIMD[1] = np.abs(thirdorderIMD[1] - RATE / 2)

    indicesIMD = [
        np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - (IMD_FREQ1 + IMD_FREQ2))),
        np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - (np.abs(IMD_FREQ1 - IMD_FREQ2)))),
        np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - (np.abs(2*IMD_FREQ1 - IMD_FREQ2)))),
        np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - (np.abs(2*IMD_FREQ2 - IMD_FREQ1)))),
        np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - (thirdorderIMD[0]))),
        np.argmin(np.abs(arrayFreq[:len(arrayFreq)//2] - (thirdorderIMD[1])))
    ]

    for indexIMD in indicesIMD:
        powerIMD += arrayMagnitude[indexIMD] ** 2

    IMD = np.sqrt(powerIMD) / np.sqrt(fundamentalPowerIMD1 + fundamentalPowerIMD2)

    actual_IMD_FREQ1 = np.abs(np.fft.fftfreq(len(numData), 1/RATE)[indexIMD1])
    actual_IMD_FREQ2 = np.abs(np.fft.fftfreq(len(numData), 1/RATE)[indexIMD2])

    return actual_IMD_FREQ1, actual_IMD_FREQ2, IMD