import streamlit as st
import pandas as pd

def processFile(teacherNameParam, fileParam):
    teacherNameParam = teacherNameParam.strip().lower()
    rawData = pd.read_excel(fileParam, sheet_name=0, header=None, dtype=str)

    myData = []

    for rowIndex, row in enumerate(rawData.itertuples(index=False, name="NthRow")):
        rowValues = [i.strip().lower() if type(i) == str else i for i in row]
        if teacherNameParam in rowValues:
            columnIndex = rowValues.index(teacherNameParam)
            sliceOfData = rawData.iloc[rowIndex - 3 : rowIndex + 2, columnIndex]
            # Validate Data
            missingValuesCount = sliceOfData.isna().sum()
            validateDataTypes = sliceOfData.tolist()
            assert missingValuesCount <= 1, "Data is Not as Expected"
            if missingValuesCount == 1:
                assert (
                    sliceOfData.isna().tolist()[2] == True
                ), "Missing Value is not where expected!"
                validateDataTypes.pop(2)
            dataTypesOfSlice = [0 if type(i) == str else 1 for i in validateDataTypes]
            assert sum(dataTypesOfSlice) == 0, "Unexpected Data Types Found"
            # Find the "Period Integer"
            rowIndexToTraverse = rowIndex - 3
            rowWithDroppedMissingValues = (
                rawData.iloc[rowIndexToTraverse].fillna("MISSING_VALUE").tolist()
            )
            matchesOfPeriods = []
            for nthColumn in range(columnIndex, -1, -1):
                currentCell = rowWithDroppedMissingValues[nthColumn]
                if currentCell.isdigit():
                    matchesOfPeriods.append(currentCell)
            assert (
                len(matchesOfPeriods) == 1
            ), "Cannot Determine Period. Multiple or No Matches Found"
            assert (
                0 < int(matchesOfPeriods[0]) < 10
            ), "Period Found Is Out Of Expected Range."
            timeColumnIndex = rowWithDroppedMissingValues.index(matchesOfPeriods[0]) + 1
            timeColumnSlice = (
                rawData.iloc[rowIndex - 3 : rowIndex + 2, timeColumnIndex]
                .dropna()
                .tolist()
            )
            assert len(timeColumnSlice) == 2, "Time Column Not Formatted As Expected"
            assignedClassData = {
                "period": matchesOfPeriods[0],
                "teacher": sliceOfData[rowIndex],
                "startTime": timeColumnSlice[0],
                "endTime": timeColumnSlice[1],
                "level": sliceOfData[rowIndex - 3],
                "roomNumber": sliceOfData[rowIndex - 2],
                "subject": sliceOfData[rowIndex + 1],
            }
            myData.append(assignedClassData)
    if myData:
        st.success("Here Is Your Schedule")
    else:
        st.error("❌ No Information Found!")
        st.info("💡 Please enter your name as it appears in the schedule file")

    for assignedClass in myData:
        with st.container():
            # Period and Time together at the top
            st.markdown(
                f"**Period {assignedClass['period']}** | ⏰ {assignedClass['startTime']} - {assignedClass['endTime']}"
            )

            # Rest of information in two columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"📚 Subject: {assignedClass['subject']}")
                st.markdown(f"📝 Level: {assignedClass['level']}")
            with col2:
                st.markdown(f"🏫 Room: {assignedClass['roomNumber']}")
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
