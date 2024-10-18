import pyaudio

def get_Devices():
    audioD = pyaudio.PyAudio()
    listDevices = []
    for i in range(audioD.get_device_count()):
        deviceInfo = audioD.get_device_info_by_index(i)
        singleDevice = {
            'index': i,
            'name': deviceInfo['name'],
            'maxInputChannels': deviceInfo['maxInputChannels'],
            'maxOutputChannels': deviceInfo['maxOutputChannels'],
            'defaultSampleRate': deviceInfo['defaultSampleRate']
        }
        listDevices.append(singleDevice)
    audioD.terminate()
    return listDevices