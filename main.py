from features.feature_RPM import get_RPM
from features.feature_WF import get_WF
from features.feature_IMD import get_IMD
from utilities.devices import get_Devices
from utilities.functions import calculatedBFromPercent
from tabulate import tabulate
import pyaudio
import numpy as np
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

            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                listDevices = get_Devices()
                print(tabulate(listDevices, headers="keys", tablefmt="pretty"))

            if choice == '2':
                while True:
                    peak_frequency, RPM = get_RPM(streamAudio, WF_FREQUENCY, TARGET_RPM)
                    if CHANNELS == 1:
                        print(f"Peak Frequency: {peak_frequency[0]:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {RPM[0]:.4f}, Difference: {RPM[0] - TARGET_RPM:+.4f}")
                    if CHANNELS == 2:
                        print("-" * 40)
                        print(f"Peak Frequency: {peak_frequency[0]:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {RPM[0]:.4f}, Difference: {RPM[0] - TARGET_RPM:+.4f}")
                        print(f"Peak Frequency: {peak_frequency[1]:.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {RPM[1]:.4f}, Difference: {RPM[1] - TARGET_RPM:+.4f}")
                        print("-" * 20)
                        print(f"Peak Frequency: {np.mean(peak_frequency):.2f} Hz, Target RPM: {TARGET_RPM:.4f}, RPM: {np.mean(RPM):.4f}, Difference: {np.mean(RPM) - TARGET_RPM:+.4f}")
            if choice == '3':
                while True:
                    detected_frequency, wow_percent, flutter_percent, wf = get_WF(streamAudio, WF_FREQUENCY)
                    if CHANNELS == 1:
                        print(f"Reference Frequency: {WF_FREQUENCY:.2f} Hz | "
                            f"Detected Frequency: {detected_frequency[0]:.2f} Hz | "
                            f"WOW: {wow_percent[0]:.4f} % | "
                            f"FLUTTER: {flutter_percent[0]:.4f} % | "
                            f"JOINT W&F: {wf[0]:.4f} %")
                    if CHANNELS == 2:
                        print("-" * 40)
                        print(f"Reference Frequency: {WF_FREQUENCY:.2f} Hz | "
                            f"Detected Frequency (L): {detected_frequency[0]:.2f} Hz | "
                            f"WOW (L): {wow_percent[0]:.4f} % | "
                            f"FLUTTER (L): {flutter_percent[0]:.4f} % | "
                            f"W&F (L): {wf[0]:.4f} %")
                        print(f"Reference Frequency: {WF_FREQUENCY:.2f} Hz | "
                            f"Detected Frequency (R): {detected_frequency[1]:.2f} Hz | "
                            f"WOW (R): {wow_percent[1]:.4f} % | "
                            f"FLUTTER (R): {flutter_percent[1]:.4f} % | "
                            f"W&F (R): {wf[1]:.4f} %")
                        print("-" * 20)
                        print(f"Reference Frequency: {WF_FREQUENCY:.2f} Hz | "
                            f"Detected Frequency (-): {np.mean(detected_frequency):.2f} Hz | "
                            f"WOW (-): {np.mean(wow_percent):.4f} % | "
                            f"FLUTTER (-): {np.mean(flutter_percent):.4f} % | "
                            f"W&F (-): {np.mean(wf):.4f} %")
                            
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