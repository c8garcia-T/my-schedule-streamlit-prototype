import pandas as pd
from helperFunctions.find_period_and_time import findPeriodAndTime


def findMyData(teacherName, fileUploaded):
    teacherName = teacherName.strip().lower()
    rawData = pd.read_excel(fileUploaded, sheet_name=0, header=None, dtype=str)
    myData = []
    periodNotFoundCounter = 0
    for rowIndex, row in enumerate(rawData.itertuples(index=False)):
        rowStandardized = [i.strip().lower() if type(i) == str else i for i in row]
        if teacherName in rowStandardized:
            targetColumnIndex = rowStandardized.index(teacherName)
            expectedTargetData = rawData.iloc[
                rowIndex - 3 : rowIndex + 2, targetColumnIndex
            ]
            # Find the "Period Integer" & Start Time Cell
            try:
                expectedRowIndexForPeriod = rowIndex - 3
                expectedRowForPeriod = (
                    rawData.iloc[expectedRowIndexForPeriod]
                    .fillna("MISSING_VALUE")
                    .tolist()
                )
                periodAndTimeData = findPeriodAndTime(
                    expectedRowForPeriod, targetColumnIndex
                )
                assignedClassData = {
                    "period": periodAndTimeData[0],
                    "teacher": expectedTargetData[rowIndex],
                    "startTime": periodAndTimeData[1],
                    "level": expectedTargetData[rowIndex - 3],
                    "roomNumber": expectedTargetData[rowIndex - 2],
                    "subject": expectedTargetData[rowIndex + 1],
                    "originalTeacher": expectedTargetData[rowIndex - 1],
                }
                myData.append(assignedClassData)
            except:
                periodNotFoundCounter += 1
    print(periodNotFoundCounter)
    return myData, periodNotFoundCounter
