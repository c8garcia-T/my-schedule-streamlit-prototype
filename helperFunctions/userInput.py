import streamlit as st

def userInput():
    st.markdown(
        "<h1 style='margin-bottom: 2rem;'>My Schedule 🍎</h1>", unsafe_allow_html=True
    )
    teacherName = st.text_input("Your Name", placeholder="Enter your name here...")
    if not teacherName:
        st.markdown("### 💡 Please enter your name as it appears in the schedule file")
    return teacherName
