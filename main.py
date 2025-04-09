import streamlit as st
import pandas as pd
from helperFunctions.find_my_data import findMyData
from helperFunctions.render_my_data import renderMyData

# global.css equivalent
st.markdown(
    """
    <style>
    :root {
        --h1-text-color: #1E88E5;
        --h2-text-color: #424242;
        --h3-text-color: #616161;
    }
    .stMarkdown {
        font-size: 18px;
    }
    h1 {
        color: var(--h1-text-color);
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
    h2 {
        color: var(--h2-text-color);
        font-weight: 500;
        font-size: 1.5rem;
        margin-top: 1rem;
    }
    h3 {
        color: var(--h3-text-color);
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
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "<h1 style='margin-bottom: 2rem;'>My Schedule 🍎</h1>", unsafe_allow_html=True
)
teacherName = st.text_input("Your Name", placeholder="Enter your name here...")
uploaded_file = st.file_uploader(
    label="Upload Today's Work Schedule",
    accept_multiple_files=False,
    label_visibility="visible",
    type=["xlsx"],
    key="ExcelFileDataSource",
)

if (uploaded_file is not None) & (teacherName != ""):
    with st.spinner(f"Getting Information For {teacherName}..."):
        myData, errorCounter = findMyData(teacherName, uploaded_file)
        if myData:
            st.markdown(
                f"<h3 style='font-weight: 400;'>👋 Here Is Your Schedule, {teacherName.capitalize()}!</h3>",
                unsafe_allow_html=True,
            )
            st.title(f"Total Classes Today: {len(myData)}")
            renderMyData(myData)
        else:
            st.error("❌ No Information Found!")
            st.title("💡 Please enter your name as it appears in the schedule file")
