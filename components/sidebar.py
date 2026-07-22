import streamlit as st


def sidebar():

    with st.sidebar:

        st.title("AI Data Analyst")

        file = st.file_uploader(
            "Upload CSV",
            type=["csv"]
        )

        st.divider()

        st.markdown(
            """
### Example Questions

- Executive Summary
- Dataset Overview
- Sales by Region
- Profit Analysis
- KPI Dashboard
- Correlation
- Missing Values
            """
        )

    return file