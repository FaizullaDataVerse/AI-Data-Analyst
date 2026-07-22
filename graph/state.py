from typing import TypedDict
from plotly.graph_objs import Figure
import pandas as pd


class AgentState(TypedDict):

    # ----------------------------
    # User Input
    # ----------------------------
    query: str

    # ----------------------------
    # Shared Dataset
    # ----------------------------
    df: pd.DataFrame

    # ----------------------------
    # Supervisor Route
    # ANALYST | VISUALIZER | BOTH | REPORT
    # ----------------------------
    route: str

    # ----------------------------
    # AI Analysis
    # ----------------------------
    analysis: str

    # ----------------------------
    # Executive Report
    # ----------------------------
    report: str

    # ----------------------------
    # KPI Cards
    # ----------------------------
    kpis: dict

    # ----------------------------
    # Tables
    # ----------------------------
    tables: dict

    # ----------------------------
    # Multiple Charts
    # Used for Full Reports
    # ----------------------------
    dashboard: dict | None

    # ----------------------------
    # List of Charts
    # ----------------------------
    charts: list

    # ----------------------------
    # Single Chart
    # ----------------------------
    chart: Figure | None

    # ----------------------------
    # Saved Chart HTML
    # ----------------------------
    chart_path: str

    # ----------------------------
    # Suggested Chart
    # ----------------------------
    chart_suggestion: str

    # ----------------------------
    # Final Response
    # ----------------------------
    response: str