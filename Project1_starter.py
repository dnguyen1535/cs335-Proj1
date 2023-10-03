what is the step count for this code:
import ast

def convertToMinutes(timeStr):
    hours, minutes = map(int, timeStr.split(':'))
    return hours * 60 + minutes

def convertToStr(minutes):
    hours, minutes = divmod(minutes, 60)
    return f'{hours:02d}:{minutes:02d}'

def addMinutesToTime(timeStr, minutes):
    time = convertToMinutes(timeStr)
    newTime = time + minutes
    return convertToStr(newTime)

def mergeSchedule(busySchedule, workingHours):
    mergedSchedule = []
    startOfDay = convertToMinutes(workingHours[0])
    endOfDay = convertToMinutes(workingHours[1])
    
    if busySchedule:
        if startOfDay < convertToMinutes(busySchedule[0][0]):
            mergedSchedule.append((startOfDay, convertToMinutes(busySchedule[0][0])))
        for i in range(len(busySchedule) - 1):
            mergedSchedule.append((convertToMinutes(busySchedule[i][1]), convertToMinutes(busySchedule[i+1][0])))
        if endOfDay > convertToMinutes(busySchedule[-1][1]):
            mergedSchedule.append((convertToMinutes(busySchedule[-1][1]), endOfDay))
    else:
        mergedSchedule.append((startOfDay, endOfDay))
    
    return mergedSchedule

def intersectSchedules(schedule1, schedule2):
    i, j = 0, 0
    intersection = []
    while i < len(schedule1) and j < len(schedule2):
        start = max(schedule1[i][0], schedule2[j][0])
        end = min(schedule1[i][1], schedule2[j][1])
        if start < end:
            intersection.append((start, end))
        if schedule1[i][1] < schedule2[j][1]:
            i += 1
        else:
            j += 1
    return intersection

def groupScheduleMatching(busySchedules, workingPeriods, duration):
    mergedSchedules = [mergeSchedule(busySchedules[i], workingPeriods[i]) for i in range(len(busySchedules))]

    commonSlots = mergedSchedules[0]
    for i in range(1, len(mergedSchedules)):
        commonSlots = intersectSchedules(commonSlots, mergedSchedules[i])
    
    availableSlots = []
    for slot in commonSlots:
        if slot[1] - slot[0] >= duration:
            availableSlots.append([convertToStr(slot[0]), convertToStr(slot[1])])

    return availableSlots

def readFile(fileName,testCase):
    input = open(fileName, "r")
    inputLines = input.readlines()
    i = testCase  * 6
    busySchedules = []
    workingPeriods = []
    
    busySchedules.append(ast.literal_eval(inputLines[i]))
    busySchedules.append(ast.literal_eval(inputLines[i+2]))

    workingPeriods.append(ast.literal_eval(inputLines[i+1]))
    workingPeriods.append(ast.literal_eval(inputLines[i+3]))

    durationOfMeeting = ast.literal_eval(inputLines[i+4]) 
    input.close()

    return busySchedules,workingPeriods,durationOfMeeting

outputFile = open("output.txt", "w")

for x in range(4):
    busySchedules,workingPeriods,durationOfMeeting = readFile("input.txt",x)
    availableTimes = groupScheduleMatching(busySchedules, workingPeriods, durationOfMeeting)
    print(availableTimes)
    outputFile.write("Test case "+ str(x+1) + ": " )
    for items in availableTimes:
        outputFile.write('%s' %items)
    outputFile.write("\n")
outputFile.close()
