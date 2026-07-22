import pandas as pd

from tools.python_tool import PythonTool
from utils.llm import invoke_llm
from utils.prompts import ANALYST_PROMPT


class AnalystAgent:
    """
    AI Business Analyst

    Responsibilities
    ----------------
    ✔ Dataset Exploration
    ✔ KPI Generation
    ✔ Business Analytics
    ✔ Executive Reports
    ✔ Natural Language Q&A
    """

    def __init__(self):
        self.python_tool = PythonTool()

    # ==========================================================
    # DATASET SUMMARY
    # ==========================================================

    def _dataset_summary(self, df: pd.DataFrame):

        return {
            "Rows": len(df),
            "Columns": len(df.columns),
            "Column Names": list(df.columns),
            "Data Types": df.dtypes.astype(str).to_dict(),
            "Missing Values": df.isnull().sum().to_dict(),
            "Duplicate Rows": int(df.duplicated().sum()),
            "Memory Usage (MB)": round(
                df.memory_usage(deep=True).sum() / (1024 ** 2),
                2,
            ),
        }

    # ==========================================================
    # DATASET STATISTICS
    # ==========================================================

    def _dataset_statistics(self, df):

        return df.describe(include="all")

    # ==========================================================
    # DATA QUALITY
    # ==========================================================

    def _data_quality(self, df):

        return {
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum()),
            "Numeric Columns": list(
                df.select_dtypes(include="number").columns
            ),
            "Categorical Columns": list(
                df.select_dtypes(exclude="number").columns
            ),
        }

    # ==========================================================
    # KPI EXTRACTION
    # ==========================================================

    def _extract_kpis(self, df):

        kpis = {
            "Rows": len(df),
            "Columns": len(df.columns),
            "Missing Values": int(df.isnull().sum().sum()),
            "Duplicate Rows": int(df.duplicated().sum()),
            "Memory (MB)": round(
                df.memory_usage(deep=True).sum() / (1024 ** 2),
                2,
            ),
        }

        if "Sales" in df.columns:

            kpis["Total Sales"] = round(df["Sales"].sum(), 2)
            kpis["Average Sales"] = round(df["Sales"].mean(), 2)
            kpis["Highest Sale"] = round(df["Sales"].max(), 2)
            kpis["Lowest Sale"] = round(df["Sales"].min(), 2)

        if "Profit" in df.columns:

            kpis["Total Profit"] = round(df["Profit"].sum(), 2)
            kpis["Average Profit"] = round(df["Profit"].mean(), 2)

        if "Quantity" in df.columns:

            kpis["Total Quantity"] = int(df["Quantity"].sum())

        if {"Region", "Sales"}.issubset(df.columns):

            kpis["Top Region"] = (
                df.groupby("Region")["Sales"]
                .sum()
                .idxmax()
            )

        if {"Category", "Sales"}.issubset(df.columns):

            kpis["Top Category"] = (
                df.groupby("Category")["Sales"]
                .sum()
                .idxmax()
            )

        if {"Product", "Sales"}.issubset(df.columns):

            kpis["Top Product"] = (
                df.groupby("Product")["Sales"]
                .sum()
                .idxmax()
            )

        return kpis

    # ==========================================================
    # FULL REPORT DATA
    # ==========================================================

    def _full_analysis(self, df):

        dataset_summary = self._dataset_summary(df)
        statistics = self._dataset_statistics(df)
        data_quality = self._data_quality(df)
        kpis = self._extract_kpis(df)

        sales = self._sales_analysis(df)
        profit = self._profit_analysis(df)
        region = self._region_analysis(df)
        category = self._category_analysis(df)
        product = self._product_analysis(df)
        correlation = self._correlation_analysis(df)

        report_data = {

            "Dataset Summary": dataset_summary,

            "Statistics": statistics.to_string(),

            "Data Quality": data_quality,

            "KPIs": kpis,

            "Sales Analysis": sales,

            "Profit Analysis": profit,

            "Region Analysis": str(region),

            "Category Analysis": str(category),

            "Product Analysis": str(product),

            "Correlation Analysis": str(correlation),
        }

        report = self._generate_response(
            "Complete Dataset Analysis",
            report_data,
        )

        return {
            "report": report,
            "kpis": kpis,
            "tables": {
                "Statistics": statistics,
                "Region": region,
                "Category": category,
                "Product": product,
                "Correlation": correlation,
            },
        }

    # ==========================================================
    # AI RESPONSE
    # ==========================================================

    def _generate_response(
        self,
        user_query: str,
        result,
    ):

        prompt = f"""
{ANALYST_PROMPT}

User Question:
{user_query}

Analysis Result:

{result}

Instructions:

If the user requested a FULL REPORT:

Return:

# Executive Summary

# Dataset Overview

# KPI Summary

# Sales Analysis

# Profit Analysis

# Region Analysis

# Product Analysis

# Category Analysis

# Correlation Analysis

# Data Quality

# Business Insights

# Recommendations

# Risks

# Conclusion

If the user asked a simple question,
answer only that question.

If the user requested a specific analysis,
answer only that analysis.

Never invent data.
Use only the supplied analysis.
"""

        return invoke_llm(prompt).strip()

    # ==========================================================
    # SIMPLE QUESTIONS
    # ==========================================================

    def _simple_questions(
        self,
        df,
        query,
    ):

        if (
            "total sales" in query
            and "Sales" in df.columns
        ):
            return f"💰 Total Sales: ${df['Sales'].sum():,.2f}"

        if (
            "average sales" in query
            and "Sales" in df.columns
        ):
            return f"📊 Average Sales: ${df['Sales'].mean():,.2f}"

        if (
            "highest sale" in query
            and "Sales" in df.columns
        ):
            return f"⬆ Highest Sale: ${df['Sales'].max():,.2f}"

        if (
            "lowest sale" in query
            and "Sales" in df.columns
        ):
            return f"⬇ Lowest Sale: ${df['Sales'].min():,.2f}"

        if (
            "total profit" in query
            and "Profit" in df.columns
        ):
            return f"💵 Total Profit: ${df['Profit'].sum():,.2f}"

        if (
            "average profit" in query
            and "Profit" in df.columns
        ):
            return f"📈 Average Profit: ${df['Profit'].mean():,.2f}"

        if "rows" in query:
            return f"The dataset contains {len(df)} rows."

        if "columns" in query:
            return f"The dataset contains {len(df.columns)} columns."

        return None

    # ==========================================================
    # SALES ANALYSIS
    # ==========================================================

    def _sales_analysis(self, df):

        if "Sales" not in df.columns:
            return "Sales column not found."

        sales = df["Sales"]

        result = {
            "Total Sales": round(sales.sum(), 2),
            "Average Sales": round(sales.mean(), 2),
            "Median Sales": round(sales.median(), 2),
            "Highest Sale": round(sales.max(), 2),
            "Lowest Sale": round(sales.min(), 2),
            "Standard Deviation": round(sales.std(), 2),
        }

        if "Region" in df.columns:

            result["Best Region"] = (
                df.groupby("Region")["Sales"]
                .sum()
                .idxmax()
            )

        if "Category" in df.columns:

            result["Best Category"] = (
                df.groupby("Category")["Sales"]
                .sum()
                .idxmax()
            )

        if "Product" in df.columns:

            result["Best Product"] = (
                df.groupby("Product")["Sales"]
                .sum()
                .idxmax()
            )

        return result

    # ==========================================================
    # PROFIT ANALYSIS
    # ==========================================================

    def _profit_analysis(self, df):

        if "Profit" not in df.columns:
            return "Profit column not found."

        profit = df["Profit"]

        result = {
            "Total Profit": round(profit.sum(), 2),
            "Average Profit": round(profit.mean(), 2),
            "Median Profit": round(profit.median(), 2),
            "Highest Profit": round(profit.max(), 2),
            "Lowest Profit": round(profit.min(), 2),
            "Standard Deviation": round(profit.std(), 2),
        }

        if "Region" in df.columns:

            result["Most Profitable Region"] = (
                df.groupby("Region")["Profit"]
                .sum()
                .idxmax()
            )

        if "Category" in df.columns:

            result["Most Profitable Category"] = (
                df.groupby("Category")["Profit"]
                .sum()
                .idxmax()
            )

        if "Product" in df.columns:

            result["Most Profitable Product"] = (
                df.groupby("Product")["Profit"]
                .sum()
                .idxmax()
            )

        return result

    # ==========================================================
    # REGION ANALYSIS
    # ==========================================================

    def _region_analysis(self, df):

        if not {"Region", "Sales"}.issubset(df.columns):
            return "Region or Sales column not found."

        agg = {
            "Sales": ["sum", "mean", "count"]
        }

        if "Profit" in df.columns:
            agg["Profit"] = "sum"

        region = (
            df.groupby("Region")
            .agg(agg)
        )

        region.columns = [
            "_".join(col).strip("_")
            for col in region.columns.values
        ]

        region = region.rename(
            columns={
                "Sales_sum": "Total Sales",
                "Sales_mean": "Average Sales",
                "Sales_count": "Transactions",
                "Profit_sum": "Total Profit",
            }
        )

        return region.round(2).sort_values(
            by="Total Sales",
            ascending=False,
        )

    # ==========================================================
    # CATEGORY ANALYSIS
    # ==========================================================

    def _category_analysis(self, df):

        if not {"Category", "Sales"}.issubset(df.columns):
            return "Category or Sales column not found."

        agg = {
            "Sales": ["sum", "mean", "count"]
        }

        if "Profit" in df.columns:
            agg["Profit"] = "sum"

        category = (
            df.groupby("Category")
            .agg(agg)
        )

        category.columns = [
            "_".join(col).strip("_")
            for col in category.columns.values
        ]

        category = category.rename(
            columns={
                "Sales_sum": "Total Sales",
                "Sales_mean": "Average Sales",
                "Sales_count": "Transactions",
                "Profit_sum": "Total Profit",
            }
        )

        return category.round(2).sort_values(
            by="Total Sales",
            ascending=False,
        )

    # ==========================================================
    # PRODUCT ANALYSIS
    # ==========================================================

    def _product_analysis(self, df):

        if not {"Product", "Sales"}.issubset(df.columns):
            return "Product or Sales column not found."

        agg = {
            "Sales": ["sum", "mean", "count"]
        }

        if "Profit" in df.columns:
            agg["Profit"] = "sum"

        product = (
            df.groupby("Product")
            .agg(agg)
        )

        product.columns = [
            "_".join(col).strip("_")
            for col in product.columns.values
        ]

        product = product.rename(
            columns={
                "Sales_sum": "Total Sales",
                "Sales_mean": "Average Sales",
                "Sales_count": "Transactions",
                "Profit_sum": "Total Profit",
            }
        )

        return product.round(2).sort_values(
            by="Total Sales",
            ascending=False,
        )

    # ==========================================================
    # CORRELATION ANALYSIS
    # ==========================================================

    def _correlation_analysis(self, df):

        numeric_df = df.select_dtypes(include="number")

        if numeric_df.shape[1] < 2:
            return "Not enough numeric columns."

        return numeric_df.corr().round(3)

    # ==========================================================
    # PYTHON EXECUTION
    # ==========================================================

    def _python_execution(
        self,
        df,
        user_query,
    ):

        prompt = f"""
Convert the following user request into ONE valid pandas expression.

Rules:

- DataFrame variable name is df.
- Return ONLY the pandas expression.
- No explanation.
- No markdown.

User Request:

{user_query}
"""

        expression = invoke_llm(prompt).strip()

        try:

            return self.python_tool.execute(
                expression,
                df
            )

        except Exception as e:

            return f"Unable to execute generated expression.\n\n{e}"

    # ==========================================================
    # MAIN ANALYSIS
    # ==========================================================

    def analyze(
        self,
        df: pd.DataFrame,
        user_query: str,
    ):

        if df is None:
            return "No dataset loaded."

        query = user_query.lower().strip()

        # ======================================================
        # SIMPLE QUESTIONS
        # ======================================================

        simple_answer = self._simple_questions(df, query)

        if simple_answer is not None:
            return simple_answer

        # ======================================================
        # FULL REPORT
        # ======================================================

        report_keywords = [
            "full report",
            "complete report",
            "full analysis",
            "complete analysis",
            "analyse fully",
            "analyze fully",
            "dataset analysis",
            "analyse everything",
            "analyze everything",
            "executive report",
            "business report",
        ]

        if any(keyword in query for keyword in report_keywords):

            return self._full_analysis(df)

        # ======================================================
        # DATASET SUMMARY
        # ======================================================

        if any(keyword in query for keyword in [
            "summary",
            "overview",
            "dataset summary",
            "dataset overview",
        ]):

            result = self._dataset_summary(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # STATISTICS
        # ======================================================

        if any(keyword in query for keyword in [
            "statistics",
            "describe",
            "statistical",
        ]):

            result = self._dataset_statistics(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # DATA QUALITY
        # ======================================================

        if any(keyword in query for keyword in [
            "quality",
            "missing",
            "duplicate",
            "duplicates",
            "null",
            "clean",
        ]):

            result = self._data_quality(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # KPI
        # ======================================================

        if any(keyword in query for keyword in [
            "kpi",
            "kpis",
            "metrics",
            "dashboard metrics",
        ]):

            result = self._extract_kpis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # SALES
        # ======================================================

        if "sales" in query:

            if "region" in query:

                result = self._region_analysis(df)

            elif "category" in query:

                result = self._category_analysis(df)

            elif "product" in query:

                result = self._product_analysis(df)

            else:

                result = self._sales_analysis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # PROFIT
        # ======================================================

        if "profit" in query:

            result = self._profit_analysis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # REGION
        # ======================================================

        if "region" in query:

            result = self._region_analysis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # CATEGORY
        # ======================================================

        if "category" in query:

            result = self._category_analysis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # PRODUCT
        # ======================================================

        if "product" in query:

            result = self._product_analysis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # CORRELATION
        # ======================================================

        if any(keyword in query for keyword in [
            "correlation",
            "relationship",
            "correlate",
        ]):

            result = self._correlation_analysis(df)

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # BUSINESS INSIGHTS
        # ======================================================

        if any(keyword in query for keyword in [
            "business",
            "insight",
            "insights",
            "recommend",
            "recommendation",
            "risk",
            "opportunity",
            "executive",
        ]):

            result = {
                "KPIs": self._extract_kpis(df),
                "Sales": self._sales_analysis(df),
                "Profit": self._profit_analysis(df),
                "Data Quality": self._data_quality(df),
            }

            return self._generate_response(
                user_query,
                result,
            )

        # ======================================================
        # PYTHON FALLBACK
        # ======================================================

        result = self._python_execution(
            df,
            user_query,
        )

        return self._generate_response(
            user_query,
            result,
        )
    