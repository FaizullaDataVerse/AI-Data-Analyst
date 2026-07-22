from tools.chart_tool import ChartTool
from utils.prompts import VISUALIZER_PROMPT
from utils.llm import invoke_llm
import pandas as pd


class VisualizerAgent:

    def __init__(self):
        self.chart_tool = ChartTool()

    # ==========================================================
    # Dashboard Generator
    # ==========================================================

    def _generate_dashboard(self, df):

        dashboard = {}
        charts = []

        # ---------------- Sales by Region ----------------

        if {"Region", "Sales"}.issubset(df.columns):

            data = (
                df.groupby("Region")["Sales"]
                .sum()
                .reset_index()
            )

            fig = self.chart_tool.bar_chart(
                data,
                x="Region",
                y="Sales",
                title="Sales by Region"
            )["figure"]

            dashboard["Sales by Region"] = fig
            charts.append(fig)

        # ---------------- Sales by Category ----------------

        if {"Category", "Sales"}.issubset(df.columns):

            data = (
                df.groupby("Category")["Sales"]
                .sum()
                .reset_index()
            )

            fig = self.chart_tool.pie_chart(
                data,
                names="Category",
                values="Sales",
                title="Sales by Category"
            )["figure"]

            dashboard["Sales by Category"] = fig
            charts.append(fig)

        # ---------------- Profit by Product ----------------

        if {"Product", "Profit"}.issubset(df.columns):

            data = (
                df.groupby("Product")["Profit"]
                .sum()
                .reset_index()
            )

            fig = self.chart_tool.bar_chart(
                data,
                x="Product",
                y="Profit",
                title="Profit by Product"
            )["figure"]

            dashboard["Profit by Product"] = fig
            charts.append(fig)

        # ---------------- Correlation ----------------

        numeric = df.select_dtypes(include="number")

        if numeric.shape[1] >= 2:

            corr = numeric.corr()

            fig = self.chart_tool.heatmap(
                corr,
                title="Correlation Heatmap"
            )["figure"]

            dashboard["Correlation"] = fig
            charts.append(fig)

        return {
            "dashboard": dashboard,
            "charts": charts,
            "figure": None,
            "path": "",
            "suggestion": "",
        }

    # ==========================================================
    # Main Visualization
    # ==========================================================

    def visualize(self, df: pd.DataFrame, user_query: str):

        if df is None or df.empty:

            return {
                "figure": None,
                "dashboard": None,
                "charts": [],
                "path": "",
                "suggestion": "Dataset is empty.",
            }

        query = user_query.lower()

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

        # ======================================================
        # FULL REPORT / DASHBOARD
        # ======================================================

        report_keywords = [
            "dashboard",
            "full report",
            "complete report",
            "full analysis",
            "complete analysis",
            "executive report",
            "business report",
        ]

        if any(k in query for k in report_keywords):

            return self._generate_dashboard(df)

        # ======================================================
        # SALES BY REGION
        # ======================================================

        if (
            "sales" in query
            and "region" in query
            and {"Region", "Sales"}.issubset(df.columns)
        ):

            data = (
                df.groupby("Region")["Sales"]
                .sum()
                .reset_index()
            )

            return self.chart_tool.bar_chart(
                data,
                x="Region",
                y="Sales",
                title="Sales by Region"
            )

        # ======================================================
        # SALES BY PRODUCT
        # ======================================================

        if (
            "sales" in query
            and "product" in query
            and {"Product", "Sales"}.issubset(df.columns)
        ):

            data = (
                df.groupby("Product")["Sales"]
                .sum()
                .reset_index()
            )

            return self.chart_tool.bar_chart(
                data,
                x="Product",
                y="Sales",
                title="Sales by Product"
            )

        # ======================================================
        # PROFIT BY PRODUCT
        # ======================================================

        if (
            "profit" in query
            and "product" in query
            and {"Product", "Profit"}.issubset(df.columns)
        ):

            data = (
                df.groupby("Product")["Profit"]
                .sum()
                .reset_index()
            )

            return self.chart_tool.bar_chart(
                data,
                x="Product",
                y="Profit",
                title="Profit by Product"
            )

        # ======================================================
        # CORRELATION
        # ======================================================

        if "correlation" in query:

            if len(numeric_cols) >= 2:

                corr = df[numeric_cols].corr()

                return self.chart_tool.heatmap(
                    corr,
                    title="Correlation Heatmap"
                )

        # ======================================================
        # AUTO CHART
        # ======================================================

        if any(word in query for word in [
            "chart",
            "graph",
            "plot",
            "visualize",
        ]):

            if categorical_cols and numeric_cols:

                data = (
                    df.groupby(categorical_cols[0])[numeric_cols[0]]
                    .sum()
                    .reset_index()
                )

                return self.chart_tool.bar_chart(
                    data,
                    x=categorical_cols[0],
                    y=numeric_cols[0],
                    title=f"{numeric_cols[0]} by {categorical_cols[0]}"
                )

        # ======================================================
        # LLM FALLBACK
        # ======================================================

        prompt = f"""
{VISUALIZER_PROMPT}

User Request:

{user_query}
"""

        suggestion = invoke_llm(prompt).strip().lower()

        if suggestion not in {
            "bar",
            "line",
            "pie",
            "scatter",
            "histogram",
            "box",
            "heatmap",
        }:

            suggestion = "bar"

        return {
            "figure": None,
            "dashboard": None,
            "charts": [],
            "path": "",
            "suggestion": suggestion,
        }