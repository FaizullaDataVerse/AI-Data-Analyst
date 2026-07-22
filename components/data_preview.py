import streamlit as st


def preview(df):

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )