import streamlit as st
import pandas as pd

st.markdown("""
    <style>
    .stMarkdown {
        font-size: 18px;
    }
    h1 {
        color: #1E88E5;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    h2 {
        color: #424242;
        font-weight: 500;
        font-size: 1.5rem;
        margin-top: 1rem;
    }
    h3 {
        color: #616161;
        font-weight: 400;
        font-size: 1.1rem;
        margin: 0.5rem 0;
    }
    .period-header {
        padding: 0 0 0 0.5rem;  
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    .period-header h2 {
        font-size: 1.6rem;
        margin: 0;
        font-weight: 500;
    }
    .class-info {
        padding: 0 0 0 0.5rem;  
        color: #666;
        font-weight: 400;
    }
    .label {
        color: #888;
        font-size: 1.3rem;
        font-weight: 400;
    }
    .value {
        color: #2c3e50;
        font-size: 1.6rem;
        font-weight: 500;
    }
    .divider {
        margin: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)


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
        st.markdown(f"<h3 style='font-weight: 400; color: #2c3e50;'>👋 Here Is Your Schedule, {teacherName.capitalize()}!</h3>", unsafe_allow_html=True)
    else:
        st.error("❌ No Information Found!")
        st.markdown("<h3 style='font-weight: 400;'>💡 Please enter your name as it appears in the schedule file</h3>", unsafe_allow_html=True)
    
    st.markdown(f"<h1>Total Classes Today: {len(myData)}</h1>", unsafe_allow_html=True)
    for indexAC, assignedClass in enumerate(myData):
        with st.container():
            # Period and Time together at the top
            st.markdown(
                f"""<div class='period-header'>
                    <h2>Period {assignedClass['period']} | ⏰ {assignedClass['startTime']}</h2>
                </div>""", 
                unsafe_allow_html=True
            )

            # Rest of information in two columns
            col1, col2 = st.columns(2)
            with col1:
                if assignedClass["level"].strip() != "R&D":
                    st.markdown(f"""
                        <div class='class-info'>
                            <div class='label'>Level</div>
                            <div class='value'>📝 {assignedClass['level']}</div>
                        </div>
                        <div style='height: 12px'></div>
                        <div class='class-info'>
                            <div class='label'>Subject</div>
                            <div class='value'>📚 {assignedClass['subject']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            with col2:
                if assignedClass["level"].strip() != "R&D":
                    st.markdown(f"""
                        <div class='class-info'>
                            <div class='label'>Room</div>
                            <div class='value'>🏫 {assignedClass['roomNumber']}</div>
                        </div>
                    """, unsafe_allow_html=True)
            if assignedClass["level"].strip() == "R&D":
                st.markdown("<div class='value' style='text-align: center;'>R&D Period</div>", unsafe_allow_html=True)
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            
            if indexAC + 1 < len(myData):
                if int(myData[indexAC + 1]["period"]) - int(myData[indexAC]["period"]) > 1:
                    periodsEmpty = [str(i) for i in range(
                        int(myData[indexAC]["period"]) + 1,
                        int(myData[indexAC + 1]["period"]),
                    )]
                    periodLabel = "Period" if len(periodsEmpty) == 1 else "Periods"
                    periodTextValue = ", ".join(periodsEmpty)
                    st.markdown(f"""
                        <div style='text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 8px;'>
                            <div class='label'>{periodLabel}: {periodTextValue}</div>
                            <div class='value' style='color: #666;'>{"No Class Assigned" if len(periodsEmpty) == 1 else "No Classes Assigned"}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)


st.markdown("<h1 style='margin-bottom: 2rem;'>My Schedule 🍎</h1>", unsafe_allow_html=True)
teacherName = st.text_input("Your Name", placeholder="Enter your name here...")
if not teacherName:
    st.markdown("### 💡 Please enter your name as it appears in the schedule file")

uploaded_file = st.file_uploader(
    label="Upload Today's Work Schedule",
    accept_multiple_files=False,
    label_visibility="visible",
    type=["xlsx"],
)
if (uploaded_file is not None) & (teacherName != ""):
    with st.spinner(f"Getting Information For {teacherName}..."):
        processFile(teacherName, uploaded_file)
