import streamlit as st


def show_chart(fig):

    if fig is not None:

        st.plotly_chart(
            fig,
            use_container_width=True
        )