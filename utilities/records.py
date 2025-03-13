import json
import tabulate

jsonRecordsFilePath = 'config/functionalities/test_records.json'
jsonFunctionalitiesFilePath = 'config/functionalities/test_functions.json'
jsonSettingsFilePath = 'config/settings/settings.json'

def loadRecords():
    with open(jsonRecordsFilePath, 'r') as file:
        data = json.load(file)
    return data["RECORDS"]

def loadJSON(pathX):
    with open(pathX, 'r') as fileX:
        return json.load(fileX)

def getSetRecordList(recordList=None):
    dataRecords = loadJSON(jsonRecordsFilePath)
    dataFunctionalities = loadJSON(jsonFunctionalitiesFilePath)
    dictFunctionalities = {funcX['ID']: funcX['Name'] for funcX in dataFunctionalities['FUNCTIONS']}
    dataTable = []

    if recordList:
        recordList = set(map(int, recordList.split(',')))
    else:
        dataTable.append(["No test records configured.", ""])
        return dataTable

    for recordX in dataRecords['RECORDS']:
        recordID = recordX['ID']
        if recordList and recordID not in recordList:
            continue
        recordName = recordX['Name']
        functionList = recordX['Functions']
        functionNames = [dictFunctionalities[func['ID']] for func in functionList]
        functionNames.sort()
        dataTable.append([recordName, ', '.join(functionNames)])

    dataTable.sort(key=lambda x: x[0])
    return dataTable

def saveSetting(settingX, valueX):
    try:
        with open(jsonSettingsFilePath, 'r') as fileZ:
            dataX = json.load(fileZ)
    except FileNotFoundError:
        dataX = {}
    dataX[settingX] = valueX
    with open(jsonSettingsFilePath, 'w') as file:
        json.dump(dataX, file, indent=4)

def getSetting(settingX):
    try:
        with open(jsonSettingsFilePath, 'r') as fileX:
            dataX = json.load(fileX)

        if settingX in dataX:
            return dataX[settingX]
        else:
            return "N/A"
    except:
        return "N/A"


def getAvailableFunctionalities():
    recordIDs = [int(id.strip()) for id in getSetting("TestRecordIDs").split(',')]
    dataRecords = loadJSON(jsonRecordsFilePath)
    funcUnique = set()

    for recordX in dataRecords['RECORDS']:
        if recordX['ID'] in recordIDs:
            setFuncs = recordX['Functions']
            for funcX in setFuncs:
                funcUnique.add(funcX['ID'])
    sortedIDs = sorted(funcUnique)
    if not sortedIDs:
        return "0"
    
    return sortedIDs

def printFunctionalityChoices():
    dataFunctionalities = loadJSON(jsonFunctionalitiesFilePath)
    funcIDs = getAvailableFunctionalities()
    dictFunctionality = {funcX['ID']: funcX['Name'] for funcX in dataFunctionalities['FUNCTIONS']}
    for funcID in funcIDs:
        if funcID in dictFunctionality:
            if funcID < 10:
                print(f"{funcID}.  {dictFunctionality[funcID]}")
            else:
                print(f"{funcID}. {dictFunctionality[funcID]}")