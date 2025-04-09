def findPeriodAndTime(data, columnIndex):
    periodAndTimeDataFound = []
    for nthColumn in range(columnIndex, -1, -1):
        currentCell = data[nthColumn]
        if (currentCell.isdigit()) and (":" in data[nthColumn + 1]):
            periodAndTimeDataFound.append((currentCell, data[nthColumn + 1]))
    assert (
        len(periodAndTimeDataFound) == 1
    ), "Cannot Determine Period. Multiple or No Matches Found"
    assert (
        0 < int(periodAndTimeDataFound[0][0]) < 15
    ), "Period Found Is Out Of Expected Range."
    return periodAndTimeDataFound[0]
