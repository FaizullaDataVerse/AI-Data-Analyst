import streamlit as st


def show_kpis(kpis):

    cols = st.columns(len(kpis))

    for col, (name, value) in zip(cols, kpis.items()):

        with col:

            st.markdown(
                f"""
                <div class="kpi">
                    <p>{name}</p>
                    <h2>{value}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )