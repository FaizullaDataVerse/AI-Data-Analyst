import streamlit as st
import pandas as pd

from graph.workflow import graph

from components.styles import load_css
from components.kpi_cards import show_kpis
from components.data_preview import preview
from components.chat import ask


# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()


# ----------------------------------------------------
# Session State
# ----------------------------------------------------

if "df" not in st.session_state:
    st.session_state.df = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "kpis" not in st.session_state:
    st.session_state.kpis = {}

if "filename" not in st.session_state:
    st.session_state.filename = None


# ----------------------------------------------------
# Top Navigation
# ----------------------------------------------------

nav1, nav2 = st.columns([5, 1])

with nav1:

    st.markdown(
        """
        <div style="padding-top:10px;padding-bottom:10px;">
            <h2 style="margin:0;">
                📊 AI Data Analyst
            </h2>

            
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav2:

    uploaded_file = st.file_uploader(
        "",
        type=["csv"],
        label_visibility="collapsed",
    )


# ----------------------------------------------------
# Load Dataset
# ----------------------------------------------------

if uploaded_file is not None:

    if (
        st.session_state.df is None
        or uploaded_file.name != st.session_state.filename
    ):

        df = pd.read_csv(uploaded_file)

        st.session_state.df = df

        st.session_state.filename = uploaded_file.name

        st.session_state.messages = []

        st.session_state.kpis = {
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing": int(df.isnull().sum().sum()),
            "Duplicates": int(df.duplicated().sum()),
        }


# ----------------------------------------------------
# Empty Screen
# ----------------------------------------------------

if st.session_state.df is None:

    
    c1, c2, c3 = st.columns([1, 2, 1])

    with c2:

        st.markdown(
            """
            <div class="dataset-card">

            <h3 style="margin-top:0;">Getting Started</h3>

            <br>

            📂 Upload a CSV using the uploader in the top-right corner.

            <br><br>

            Then ask questions like:

            <ul>
                <li>Total Sales</li>
                <li>Sales by Region</li>
                <li>Profit Analysis</li>
                <li>Dashboard</li>
                <li>Full Report</li>
            </ul>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.stop()


# ----------------------------------------------------
# Dataset Information
# ----------------------------------------------------

st.markdown(
    f"""
<div class="dataset-card">

### 📁 {st.session_state.filename}

**{len(st.session_state.df):,} Rows**
&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;
**{len(st.session_state.df.columns)} Columns**
&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;
✅ Ready for Analysis

</div>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------
# KPI Cards
# ----------------------------------------------------

show_kpis(st.session_state.kpis)


# ----------------------------------------------------
# Quick Prompts
# ----------------------------------------------------

st.markdown("### 🚀 Quick Questions")

q1, q2, q3, q4, q5 = st.columns(5)

with q1:
    st.button("💰 KPI")

with q2:
    st.button("📊 Dashboard")

with q3:
    st.button("📈 Sales")

with q4:
    st.button("📄 Report")

with q5:
    st.button("🌍 Region")


st.divider()


# ----------------------------------------------------
# Main Tabs
# ----------------------------------------------------

tab1, tab2 = st.tabs(
    [
        "🤖 AI Assistant",
        "📄 Dataset Explorer",
    ]
)


# ====================================================
# AI Assistant
# ====================================================

with tab1:

    st.markdown(
        """
        <div class="hero" style="padding:25px;margin-bottom:15px;">
            <h2 style="margin:0;">🤖 AI Business Assistant</h2>
            <p style="margin-top:8px;">
                Ask questions in natural language and generate reports,
                dashboards, KPI summaries and business insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---------------------------------------------
    # Chat History
    # ---------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    # ---------------------------------------------
    # Chat Input
    # ---------------------------------------------

    prompt = ask()

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.spinner("🤖 AI is analyzing your dataset..."):

            result = graph.invoke(
                {
                    "query": prompt,
                    "df": st.session_state.df,

                    "route": "",

                    "analysis": "",
                    "report": "",

                    "kpis": {},
                    "tables": {},

                    "dashboard": None,
                    "charts": [],

                    "chart": None,
                    "chart_path": "",
                    "chart_suggestion": "",

                    "response": "",
                }
            )

        response = result.get(
            "response",
            "No response generated."
        )

        with st.chat_message("assistant"):

            st.markdown(response)

            # =================================================
            # KPI SECTION
            # =================================================

            if result.get("kpis"):

                st.divider()

                st.markdown("## 📌 Business KPIs")

                kpis = result["kpis"]

                cols = st.columns(4)

                for i, (key, value) in enumerate(kpis.items()):

                    with cols[i % 4]:

                        st.markdown(
                            f"""
                            <div class="kpi">

                            <p>{key}</p>

                            <h2>{value}</h2>

                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

            # =================================================
            # DASHBOARD
            # =================================================

            if result.get("dashboard"):

                st.divider()

                st.markdown("## 📊 Interactive Dashboard")

                charts = list(result["dashboard"].items())

                for i in range(0, len(charts), 2):

                    c1, c2 = st.columns(2)

                    with c1:

                        st.markdown(
                            f"#### {charts[i][0]}"
                        )

                        st.plotly_chart(
                            charts[i][1],
                            use_container_width=True,
                        )

                    if i + 1 < len(charts):

                        with c2:

                            st.markdown(
                                f"#### {charts[i+1][0]}"
                            )

                            st.plotly_chart(
                                charts[i+1][1],
                                use_container_width=True,
                            )

            elif result.get("chart") is not None:

                st.divider()

                st.markdown("## 📈 Visualization")

                st.plotly_chart(
                    result["chart"],
                    use_container_width=True,
                )

            # =================================================
            # REPORT TABLES
            # =================================================

            if result.get("tables"):

                st.divider()

                st.markdown("## 📋 Analysis Tables")

                tabs = st.tabs(
                    list(result["tables"].keys())
                )

                for tab, (title, table) in zip(
                    tabs,
                    result["tables"].items()
                ):

                    with tab:

                        st.dataframe(
                            table,
                            use_container_width=True,
                        )

            # =================================================
            # Suggested Chart
            # =================================================

            if result.get("chart_suggestion"):

                st.info(
                    f"💡 Suggested Visualization: **{result['chart_suggestion'].title()} Chart**"
                )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


# ====================================================
# Dataset Explorer
# ====================================================

with tab2:

    st.markdown(
        """
        <div class="hero" style="padding:25px;margin-bottom:20px;">
            <h2 style="margin:0;">📄 Dataset Explorer</h2>
            <p style="margin-top:8px;">
                Explore your uploaded dataset, inspect statistics,
                and understand the structure before analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =================================================
    # Dataset Overview
    # =================================================

    rows = len(st.session_state.df)

    cols = len(st.session_state.df.columns)

    memory = (
        st.session_state.df.memory_usage(deep=True).sum()
        / 1024 ** 2
    )

    missing = int(
        st.session_state.df.isnull().sum().sum()
    )

    duplicates = int(
        st.session_state.df.duplicated().sum()
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:

        st.metric(
            "Rows",
            f"{rows:,}"
        )

    with c2:

        st.metric(
            "Columns",
            cols
        )

    with c3:

        st.metric(
            "Memory",
            f"{memory:.2f} MB"
        )

    with c4:

        st.metric(
            "Missing",
            missing
        )

    with c5:

        st.metric(
            "Duplicates",
            duplicates
        )

    st.divider()

    # =================================================
    # Tabs
    # =================================================

    overview_tab, preview_tab, stats_tab = st.tabs(
        [
            "📋 Dataset Info",
            "👀 Preview",
            "📊 Statistics",
        ]
    )

    # ---------------------------------------------
    # Dataset Info
    # ---------------------------------------------

    with overview_tab:

        left, right = st.columns([2, 1])

        with left:

            st.markdown("### Dataset Details")

            info = pd.DataFrame(
                {
                    "Column": st.session_state.df.columns,
                    "Data Type": st.session_state.df.dtypes.astype(str),
                    "Missing": st.session_state.df.isnull().sum().values,
                    "Unique": [
                        st.session_state.df[col].nunique()
                        for col in st.session_state.df.columns
                    ],
                }
            )

            st.dataframe(
                info,
                use_container_width=True,
                hide_index=True,
            )

        with right:

            st.markdown("### Quick Summary")

            st.info(
                f"""
**Dataset:** {st.session_state.filename}

**Rows:** {rows:,}

**Columns:** {cols}

**Memory:** {memory:.2f} MB

**Missing Values:** {missing}

**Duplicate Rows:** {duplicates}
"""
            )

    # ---------------------------------------------
    # Preview
    # ---------------------------------------------

    with preview_tab:

        st.markdown("### First 20 Rows")

        st.dataframe(
            st.session_state.df.head(20),
            use_container_width=True,
        )

    # ---------------------------------------------
    # Statistics
    # ---------------------------------------------

    with stats_tab:

        st.markdown("### Statistical Summary")

        st.dataframe(
            st.session_state.df.describe(
                include="all"
            ),
            use_container_width=True,
        )

        with st.expander("Column Names"):

            st.write(
                list(
                    st.session_state.df.columns
                )
            )

        with st.expander("Data Types"):

            dtype_df = pd.DataFrame(
                {
                    "Column": st.session_state.df.columns,
                    "Type": st.session_state.df.dtypes.astype(str),
                }
            )

            st.dataframe(
                dtype_df,
                use_container_width=True,
                hide_index=True,
            )

        with st.expander("Missing Values"):

            miss = pd.DataFrame(
                {
                    "Column": st.session_state.df.columns,
                    "Missing": st.session_state.df.isnull().sum().values,
                }
            )

            st.dataframe(
                miss,
                use_container_width=True,
                hide_index=True,
            )

    st.divider()

    st.success(
        "✅ Dataset loaded successfully and ready for AI analysis."
    )