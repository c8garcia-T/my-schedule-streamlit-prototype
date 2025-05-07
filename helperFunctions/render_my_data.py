import streamlit as st

def renderMyData(data):
    for indexAC, assignedClass in enumerate(data):
        with st.container():
            # Period and Time together at the top
            st.markdown(
                f"""<div class='period-header'>
                    <h2>Period {assignedClass['period']} | ⏰ {assignedClass['startTime']} - {assignedClass['endTime']}</h2>
                </div>""",
                unsafe_allow_html=True,
            )

            # Rest of information in two columns
            col1, col2 = st.columns(2)
            with col1:
                if assignedClass["level"].strip() != "R&D":
                    st.markdown(
                        f"""
                        <div class='class-info'>
                            <div class='label'>Level</div>
                            <div class='value'>📝 {assignedClass['level']}</div>
                        </div>
                        <div style='height: 12px'></div>
                        <div class='class-info'>
                            <div class='label'>Subject</div>
                            <div class='value'>📚 {assignedClass['subject']}</div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
            with col2:
                if assignedClass["level"].strip() != "R&D":
                    st.markdown(
                        f"""
                        <div class='class-info'>
                            <div class='label'>Room</div>
                            <div class='value'>🏫 {assignedClass['roomNumber']}</div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
                if (
                    assignedClass["originalTeacher"]
                    and type(assignedClass["originalTeacher"]) == str
                ):
                    st.markdown(
                        f"""
                        <div class='class-info'>
                            <div class='label'>You Are Subbing For</div>
                            <div class='value'>🔄 {assignedClass['originalTeacher']}</div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
            if assignedClass["level"].strip() == "R&D":
                st.markdown(
                    "<div class='value' style='text-align: center;'>R&D Period</div>",
                    unsafe_allow_html=True,
                )
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

            if indexAC + 1 < len(data):
                if (
                    int(data[indexAC + 1]["period"]) - int(data[indexAC]["period"])
                    > 1
                ):
                    periodsEmpty = [
                        str(i)
                        for i in range(
                            int(data[indexAC]["period"]) + 1,
                            int(data[indexAC + 1]["period"]),
                        )
                    ]
                    periodLabel = "Period" if len(periodsEmpty) == 1 else "Periods"
                    periodTextValue = ", ".join(periodsEmpty)
                    st.markdown(
                        f"""
                        <div style='text-align: center; padding: 1rem; background-color: #f8f9fa; border-radius: 8px;'>
                            <div class='label'>{periodLabel}: {periodTextValue}</div>
                            <div class='value' style='color: #666;'>{"No Class Assigned" if len(periodsEmpty) == 1 else "No Classes Assigned"}</div>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)