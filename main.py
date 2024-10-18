from features.feature_RPM import get_RPM
import pyaudio
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE


TARGET_RPM = 33.3333
TARGET_FREQUENCY = 3150

# Set up audio input
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=DEVICE)

try:
    print("Listening for audio...")
    while True:
        peak_frequency, rpm = get_RPM(stream, TARGET_FREQUENCY, TARGET_RPM)
        print(f"Peak Frequency: {peak_frequency:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {rpm:.4f}, Difference: {rpm - TARGET_RPM:+.4f}")

except KeyboardInterrupt:
    print("Stopped by User")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()