from features.feature_RPM import get_RPM
from features.feature_WF import get_WF
from features.feature_IMD import get_IMD
from features.feature_THD import get_THDN
from features.feature_Balance import get_ChannelBalance
from utilities.devices import get_Devices
from utilities.functions import calculatedBFromPercent, getChannelName, clearConsole, sanitizeCommaInput, colorValueByLimit
from utilities.records import loadRecords, getSetRecordList, saveSetting, getSetting, printFunctionalityChoices
from tabulate import tabulate
import pyaudio
import numpy as np
import time
from config.stream import FORMAT, CHANNELS, RATE, THRESHOLD, DEVICE, SMALL_CHUNK

TARGET_RPM = 33.3333
RPM_DEVIATION_LIMIT = 0.033
RPM_DEVIATION_PREFERRED = 0.0165
WF_FREQUENCY = 3150
WF_DEVIATION_LIMIT = 0.1
WF_DEVIATION_PREFERRED = 0.05
IMD_FREQ1 = 60
IMD_FREQ2 = 4000
freqAllowedLimit = int(WF_FREQUENCY * (RPM_DEVIATION_LIMIT / TARGET_RPM))
freqAllowedPreferred = int(WF_FREQUENCY * (RPM_DEVIATION_PREFERRED / TARGET_RPM))


def main():

    # Set up audio input.
    audioP = pyaudio.PyAudio()
    streamAudio = audioP.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=SMALL_CHUNK, input_device_index=DEVICE)

    try:
        while True:
            clearConsole()
            
            print("\nSelect an option:\n")
            print("A.  List Audio Devices")
            print("B.  Get Current Test Record Configuration")
            print("C.  Change Test Record Configuration")
            print("-" * 15)
            printFunctionalityChoices()
            print("-" * 15)
            print("X.  Exit\n")

            choiceX = input("Enter your choice: ")

            clearConsole()

            if (choiceX == 'A' or choiceX == 'a'):
                listDevices = get_Devices()
                print(tabulate(listDevices, headers="keys", tablefmt="pretty"))
                print("\nPress any key to return to the previous screen.")
                choiceB = input()

            if (choiceX == 'B' or choiceX == 'b'):
                recordIDs = getSetting("TestRecordIDs")
                tableX = getSetRecordList(recordIDs)
                tableHeaders = ["Record Name", "Available Functionalities"]
                print(tabulate(tableX, headers=tableHeaders, tablefmt="grid"))
                print("\nPress any key to return to the previous screen.")
                choiceB = input()

            if (choiceX == 'C' or choiceX == 'c'):
                recordList = loadRecords()

                print("\nCurrently available test records for selection:\n")
                for recordX in recordList:
                    print(f"{recordX['ID']}: {recordX['Name']}")
                choiceZ = input("\nSelect the records you own separated by commas or X to exit: ")
                if (choiceZ == 'X' or choiceZ == 'x'):
                    print("\nNo changes have been made.")
                else:
                    recordIDs = sanitizeCommaInput(choiceZ)
                    clearConsole()
                    if recordIDs == "":
                        print("\nNo changes have been made.")
                    else:
                        saveSetting("TestRecordIDs", recordIDs)
                        print("\nThe following records have been now set as your collection:\n")
                        tableX = getSetRecordList(recordIDs)
                        tableHeaders = ["Record Name", "Available Functionalities"]
                        print(tabulate(tableX, headers=tableHeaders, tablefmt="grid"))

                print("\nPress any key to return to the previous screen.")
                choiceB = input()

            if choiceX == '7':
                arrayFreqStorage = []
                arrayAmpStorage = []
                while True:
                    peakFrequency, AMP, arrayFreqStorage, arrayAmpStorage = get_ChannelBalance(streamAudio, arrayFreqStorage, arrayAmpStorage)
                    tableData = []
                    tableHeaders = [" ", "Peak Frequency", "Amplitude (dB)", "Difference (dB)"]
                    for channelX in range(CHANNELS):
                        channelName = getChannelName(channelX + 1)
                        tableData.append([channelName, f"{peakFrequency[channelX]:.2f} Hz", f"{AMP[channelX]:+.4f} dB", f"{AMP[channelX] - np.mean(AMP):+.4f} dB"])
                    if CHANNELS > 1:
                        balanceDifference = AMP[0] - AMP[1]
                        separatorRow = [" ", "-----", "-----", "-----"]
                        totalRow = ["T", f"{np.mean(peakFrequency):.2f} Hz", "", f"{colorValueByLimit(balanceDifference, 1, "dB", 0.75)}"]
                        tableData.extend([separatorRow, totalRow])
                    print(tabulate(tableData, headers=tableHeaders, tablefmt="grid", colalign=("left", "right", "right", "right")))
                    print()

            if choiceX == '11':
                arrayRPMStorage = []
                while True:
                    peakFrequency, RPM, arrayRPMStorage = get_RPM(streamAudio, WF_FREQUENCY, TARGET_RPM, arrayRPMStorage)
                    tableData = []
                    tableHeaders = [" ", "Peak Frequency", "Target RPM", "Measured RPM", "Difference", "Percentage"]
                    for channelX in range(CHANNELS):
                        channelName = getChannelName(channelX + 1)
                        tableData.append([channelName, f"{colorValueByLimit(peakFrequency[channelX], freqAllowedLimit, "Hz", freqAllowedPreferred, WF_FREQUENCY, ".2f")}", f"{TARGET_RPM:.4f}", f"{colorValueByLimit(RPM[channelX], RPM_DEVIATION_LIMIT, "", RPM_DEVIATION_PREFERRED, TARGET_RPM, ".4f")}", f"{colorValueByLimit(RPM[channelX], RPM_DEVIATION_LIMIT, "", RPM_DEVIATION_PREFERRED, TARGET_RPM, "+.4f", True)}", f"{colorValueByLimit(RPM[channelX], RPM_DEVIATION_LIMIT, "%", RPM_DEVIATION_PREFERRED, TARGET_RPM, "+.4f", False, True)}"])
                    if CHANNELS > 1:
                        meanRPM = np.mean(RPM)
                        separatorRow = [" ", "-----", "-----", "-----", "-----", "-----"]
                        totalRow = ["T", f"{colorValueByLimit(np.mean(peakFrequency), freqAllowedLimit, "Hz", freqAllowedPreferred, WF_FREQUENCY, ".2f")}", f"{TARGET_RPM:.4f}", f"{colorValueByLimit(meanRPM, RPM_DEVIATION_LIMIT, "", RPM_DEVIATION_PREFERRED, TARGET_RPM, ".4f")}", f"{colorValueByLimit(meanRPM, RPM_DEVIATION_LIMIT, "", RPM_DEVIATION_PREFERRED, TARGET_RPM, "+.4f", True)}", f"{colorValueByLimit(meanRPM, RPM_DEVIATION_LIMIT, "%", RPM_DEVIATION_PREFERRED, TARGET_RPM, "+.4f", False, True)}"]
                        tableData.extend([separatorRow, totalRow])
                    print(tabulate(tableData, headers=tableHeaders, tablefmt="grid", colalign=("left", "right", "right", "right", "right", "right")))
                    print()

            if choiceX == '12':
                arrayFlutterStorage = []
                while True:
                    freqDetected, valueWowPercent, valueFlutterPercent, valueWowPercentWeighted, valueFlutterPercentWeighted, valueWF, valueWFW, valueWFRMS, valueWFWRMS, valueDifference, arrayFlutterStorage = get_WF(streamAudio, WF_FREQUENCY, arrayFlutterStorage)
                    tableData = []
                    tableHeaders = [" ", "Reference", "Peak Frequency", "Difference", "Wow", "Flutter", "W&F Mean", "W&F RMS", "Wow (W)", "Flutter (W)", "W&F Mean (W)", "W&F RMS (W)"]
                    for channelX in range(CHANNELS):
                        channelName = getChannelName(channelX + 1)
                        tableData.append([channelName, f"{WF_FREQUENCY:.2f} Hz", f"{colorValueByLimit(freqDetected[channelX], freqAllowedLimit, "Hz", freqAllowedPreferred, WF_FREQUENCY, ".2f")}", f"{valueDifference[channelX]:+.4f} %", f"{valueWowPercent[channelX]:.4f} %", f"{valueFlutterPercent[channelX]:.4f} %", f"{valueWF[channelX]:.4f} %", f"{valueWFRMS[channelX]:.4f} %", f"{colorValueByLimit(valueWowPercentWeighted[channelX], WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}", f"{colorValueByLimit(valueFlutterPercentWeighted[channelX], WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}", f"{colorValueByLimit(valueWFW[channelX], WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}", f"{colorValueByLimit(valueWFWRMS[channelX], WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}"])
                    if CHANNELS > 1:
                        separatorRow = [" ", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----", "-----"]
                        totalRow = ["T", f"{WF_FREQUENCY:.2f} Hz", f"{colorValueByLimit(np.mean(freqDetected), freqAllowedLimit, "Hz", freqAllowedPreferred, WF_FREQUENCY, ".2f")}", f"{np.mean(valueDifference):+.4f} %", f"{np.mean(valueWowPercent):.4f} %", f"{np.mean(valueFlutterPercent):.4f} %", f"{np.mean(valueWF):.4f} %", f"{np.mean(valueWFRMS):.4f} %", f"{colorValueByLimit(np.mean(valueWowPercentWeighted), WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}", f"{colorValueByLimit(np.mean(valueFlutterPercentWeighted), WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}", f"{colorValueByLimit(np.mean(valueWFW), WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}", f"{colorValueByLimit(np.mean(valueWFWRMS), WF_DEVIATION_LIMIT, "%", WF_DEVIATION_PREFERRED)}"]
                        tableData.extend([separatorRow, totalRow])
                    print(tabulate(tableData, headers=tableHeaders, tablefmt="grid", colalign=("left", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right", "right")))
                    print()
           
            if choiceX == '13':
                while True:
                    freqIMD1, freqIMD2, IMD = get_IMD(streamAudio, IMD_FREQ1, IMD_FREQ2)
                    if CHANNELS == 1:
                        print(f"Test Frequencies: {IMD_FREQ1:.2f} Hz, {IMD_FREQ2:.2f} Hz | Detected Frequencies: {freqIMD1[0]:.2f} Hz, {freqIMD2[0]:.2f} Hz | IMD (%): {IMD[0]*100:.4f}% | IMD (dB): {calculatedBFromPercent(IMD[0]):.2f} dB")
                    if CHANNELS == 2:
                        print("-" * 40)
                        print(f"Test Frequencies: {IMD_FREQ1:.2f} Hz, {IMD_FREQ2:.2f} Hz | Detected Frequencies: {freqIMD1[0]:.2f} Hz, {freqIMD2[0]:.2f} Hz | IMD (%): {IMD[0]*100:.4f}% | IMD (dB): {calculatedBFromPercent(IMD[0]):.2f} dB")
                        print(f"Test Frequencies: {IMD_FREQ1:.2f} Hz, {IMD_FREQ2:.2f} Hz | Detected Frequencies: {freqIMD1[1]:.2f} Hz, {freqIMD2[1]:.2f} Hz | IMD (%): {IMD[1]*100:.4f}% | IMD (dB): {calculatedBFromPercent(IMD[1]):.2f} dB")
                        print("-" * 20)
                        print(f"Test Frequencies: {IMD_FREQ1:.2f} Hz, {IMD_FREQ2:.2f} Hz | Detected Frequencies: {np.mean(freqIMD1):.2f} Hz, {np.mean(freqIMD2):.2f} Hz | IMD (%): {np.mean(IMD)*100:.4f}% | IMD (dB): {calculatedBFromPercent(np.mean(IMD)):.2f} dB")

            if choiceX == '14':
                while True:
                    peakFrequency, THDN, percentTHDN = get_THDN(streamAudio)
                    if CHANNELS == 1:
                        print(f"Peak Frequency: {peakFrequency[0]:.2f} Hz, THD+N (dB): {THDN[0]:.4f} dB, THD+N (%): {percentTHDN[0]:.4f}")
                    if CHANNELS == 2:
                        print("-" * 40)
                        print(f"Peak Frequency: {peakFrequency[0]:.2f} Hz, THD+N: (dB) {THDN[0]:.4f} dB, THD+N (%): {percentTHDN[0]:.4f}")
                        print(f"Peak Frequency: {peakFrequency[1]:.2f} Hz, THD+N: (dB) {THDN[1]:.4f} dB, THD+N (%): {percentTHDN[1]:.4f}")
                        print("-" * 20)
                        print(f"Peak Frequency: {np.mean(peakFrequency):.2f} Hz, THD+N: (dB) {np.mean(THDN):.4f} dB, THD+N (%): {np.mean(percentTHDN):.4f}")

            if (choiceX == 'X' or choiceX == 'x'):
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