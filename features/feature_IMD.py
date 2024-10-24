import numpy as np
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE
from utilities.functions import calculatePeakFrequency

def get_IMD(audioStream, IMD_FREQ1, IMD_FREQ2):

    numData = audioStream.read(CHUNK, exception_on_overflow=False)
    numData = np.frombuffer(numData, dtype=np.float32)

    # Split the stereo stream in two channels.
    if CHANNELS == 1:
        numDataM = []
        numDataM.append(numData)
    if CHANNELS == 2:
        numDataM = [numData[0::2], numData[1::2]]

    FFTwindow = np.hanning(CHUNK)

    IMD, freqIMD1, freqIMD2 = [0, 0], [0, 0], [0, 0]

    for channelX in range(CHANNELS):

        FFTData = np.fft.fft(numDataM[channelX])
        
        arrayFreq = np.fft.fftfreq(len(FFTData), 1/RATE)
        arrayMagnitude = np.abs(FFTData[:len(FFTData)//2])

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

        IMD[channelX] = np.sqrt(powerIMD) / np.sqrt(fundamentalPowerIMD1 + fundamentalPowerIMD2)
        freqIMD1[channelX] = calculatePeakFrequency(numDataM[channelX])
        freqIMD2[channelX] = calculatePeakFrequency(numDataM[channelX], 1)

    return freqIMD1, freqIMD2, IMD