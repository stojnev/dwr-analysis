from features.feature_RPM import get_RPM
import pyaudio
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE


TARGET_RPM = 33.3333
TARGET_FREQUENCY = 3150


def main():

    # Set up audio input
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=DEVICE)
    try:
        while True:
            print("Select an option:")
            print("1. Listen for RPM1")
            print("2. Listen for RPM2")
            print("4. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                while True:
                    peak_frequency, rpm = get_RPM(stream, TARGET_FREQUENCY, TARGET_RPM)
                    print(f"1! Peak Frequency: {peak_frequency:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {rpm:.4f}, Difference: {rpm - TARGET_RPM:+.4f}")

            if choice == '2':
                while True:
                    peak_frequency, rpm = get_RPM(stream, TARGET_FREQUENCY, TARGET_RPM)
                    print(f"2! Peak Frequency: {peak_frequency:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {rpm:.4f}, Difference: {rpm - TARGET_RPM:+.4f}")

            if choice == '4':
                print("Exiting...")
                break
    except KeyboardInterrupt:
        print("OUT!")
        
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
    
if __name__ == "__main__":
    main()