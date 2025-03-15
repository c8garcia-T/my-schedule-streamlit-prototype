import streamlit as st
import pandas as pd


def validatePeriodData(periodDataParam):
    missingValuesCount = periodDataParam.isna().sum()
    assert (
        missingValuesCount <= 3
    ), "Unexpected Error, Found More than 3 missing values."
    validateDataTypes = periodDataParam.tolist()
    if missingValuesCount == 1:  # Substitute Case
        validateDataTypes.pop(2)
    if missingValuesCount == 2:  # Catch 2 missing value case
        validateDataTypes.pop(-1)
        validateDataTypes.pop(2)
    if missingValuesCount == 3:  # R&D Case
        validateDataTypes.pop(1)
        validateDataTypes.pop(1)
        validateDataTypes.pop(-1)
    dataTypesOfSlice = [0 if type(i) == str else 1 for i in validateDataTypes]
    assert sum(dataTypesOfSlice) == 0, "Unexpected Data Types Found"


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


def processFile(nameParam, fileParam):
    name = nameParam.strip().lower()
    rawData = pd.read_excel(fileParam, sheet_name=0, header=None, dtype=str)
    myData = []
    for rowIndex, row in enumerate(rawData.itertuples(index=False, name="NthRow")):
        rowValues = [i.strip().lower() if type(i) == str else i for i in row]
        if name in rowValues:
            columnIndex = rowValues.index(name)
            periodData = rawData.iloc[rowIndex - 3 : rowIndex + 2, columnIndex]
            # Validate Data
            validatePeriodData(periodData)
            # Find the "Period Integer" & Start Time Cell
            expectedPeriod_RowIndex = rowIndex - 3
            rowValuesForPeriodAndTimeSearch = (
                rawData.iloc[expectedPeriod_RowIndex].fillna("MISSING_VALUE").tolist()
            )
            periodAndTimeData = findPeriodAndTime(
                rowValuesForPeriodAndTimeSearch, columnIndex
            )
            assignedClassData = {
                "period": periodAndTimeData[0],
                "teacher": periodData[rowIndex],
                "startTime": periodAndTimeData[1],
                "level": periodData[rowIndex - 3],
                "roomNumber": periodData[rowIndex - 2],
                "subject": periodData[rowIndex + 1],
            }
            myData.append(assignedClassData)
    if myData:
        st.success(f"Here Is Your Schedule, {teacherName}!")
    else:
        st.error("❌ No Information Found!")
        st.info("💡 Please enter your name as it appears in the schedule file")
    st.title(f"Total Classes Today: {len(myData)}")
    for indexAC, assignedClass in enumerate(myData):
        with st.container():
            # Period and Time together at the top
            st.subheader(
                f"**Period {assignedClass['period']}** | ⏰ {assignedClass['startTime']}"
            )

            # Rest of information in two columns
            col1, col2 = st.columns(2)
            with col1:
                if assignedClass["level"].strip() != "R&D":
                    st.markdown(f"📝 Level: {assignedClass['level']}")
                    st.markdown(f"📚 Subject: {assignedClass['subject']}")
            with col2:
                if assignedClass["level"].strip() != "R&D":
                    st.markdown(f"🏫 Room: {assignedClass['roomNumber']}")
            if assignedClass["level"].strip() == "R&D":
                st.text("R&D")
            st.divider()
            if indexAC + 1 < len(myData):
                if (
                    int(myData[indexAC + 1]["period"]) - int(myData[indexAC]["period"])
                ) > 1:
                    periodsEmpty = [
                        str(i)
                        for i in range(
                            int(myData[indexAC]["period"]) + 1,
                            int(myData[indexAC + 1]["period"]),
                        )
                    ]
                    periodLabel = "Period" if len(periodsEmpty) == 1 else "Periods"
                    periodTextValue = ", ".join(periodsEmpty)
                    st.subheader(f"{periodLabel}: {periodTextValue}")
                    st.text(
                        "No Class Assigned"
                        if len(periodsEmpty) == 1
                        else "No Classes Assigned"
                    )
                    st.divider()


st.title("My Schedule 🍎")
teacherName = st.text_input("Your Name")
if not teacherName:
    st.info("💡 Please enter your name as it appears in the schedule file")

uploaded_file = st.file_uploader(
    label="Upload Today's Work Schedule",
    accept_multiple_files=False,
    label_visibility="visible",
    type=["xlsx"],
)
if (uploaded_file is not None) & (teacherName != ""):
    with st.spinner(f"Getting Information For {teacherName}..."):
        processFile(teacherName, uploaded_file)
