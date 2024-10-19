from features.feature_RPM import get_RPM
from features.feature_WF import get_WF
from features.feature_IMD import get_IMD
from utilities.devices import get_Devices
from utilities.functions import calculatedBFromPercent
from tabulate import tabulate
import pyaudio
from config.stream import FORMAT, CHANNELS, RATE, CHUNK, THRESHOLD, DEVICE

TARGET_RPM = 33.3333
WF_FREQUENCY = 3150
IMD_FREQ1 = 60
IMD_FREQ2 = 4000

def main():

    # Set up audio input.
    audioP = pyaudio.PyAudio()
    streamAudio = audioP.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index=DEVICE)

    try:
        while True:
            print("Select an option:")
            print("1. List Audio Devices")
            print("2. Get RPM")
            print("3. Get W&F")
            print("4. Get IMD")
            print("5. Exit")

            choice = input("Enter your choice (1-4): ")

            if choice == '1':
                listDevices = get_Devices()
                print(tabulate(listDevices, headers="keys", tablefmt="pretty"))

            if choice == '2':
                while True:
                    peak_frequency, rpm = get_RPM(streamAudio, WF_FREQUENCY, TARGET_RPM)
                    print(f"Peak Frequency: {peak_frequency:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {rpm:.4f}, Difference: {rpm - TARGET_RPM:+.4f}")

            if choice == '3':
                while True:
                    detected_frequency, wow_percent, flutter_percent, joint_wf = get_WF(streamAudio, WF_FREQUENCY)
                    print(f"Reference Frequency: {WF_FREQUENCY:.2f} Hz | "
                        f"Detected Frequency: {detected_frequency:.2f} Hz | "
                        f"WOW: {wow_percent:.4f} % | "
                        f"FLUTTER: {flutter_percent:.4f} % | "
                        f"JOINT W&F: {joint_wf:.4f} %")

            if choice == '4':
                while True:

                    actual_freq1, actual_freq2, imd = get_IMD(streamAudio, IMD_FREQ1, IMD_FREQ2)
                    print(f"Test Frequencies: {IMD_FREQ1:.2f} Hz, {IMD_FREQ2:.2f} Hz | "
                        f"Detected Frequencies: {actual_freq1:.2f} Hz, {actual_freq2:.2f} Hz | "
                        f"IMD (%): {imd*100:.4f}% | "
                        f"IMD (dB): {calculatedBFromPercent(imd):.2f} dB")
                    
            if choice == '5':
                print("Exiting...")
                break
    except KeyboardInterrupt:
        print("OUT!")

    finally:

        # Terminate stream.
        streamAudio.stop_stream()
        streamAudio.close()
        audioP.terminate()
    
if __name__ == "__main__":
    main()