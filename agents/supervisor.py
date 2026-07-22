from utils.llm import invoke_llm
from utils.prompts import SUPERVISOR_PROMPT


class SupervisorAgent:
    """
    Routes the user's request to the appropriate agent.

    Possible routes:
    - ANALYST
    - VISUALIZER
    - BOTH
    - REPORT
    """

    def __init__(self):
        pass

    def route(self, user_query: str) -> str:

        query = user_query.lower().strip()

        # ======================================================
        # FULL REPORT KEYWORDS
        # ======================================================

        report_keywords = [
            "full report",
            "complete report",
            "full analysis",
            "complete analysis",
            "analyse fully",
            "analyze fully",
            "business report",
            "executive report",
            "dashboard report",
            "analyze everything",
            "analyse everything",
        ]

        if any(keyword in query for keyword in report_keywords):
            return "REPORT"
        if query.strip() == "dashboard":
            return "REPORT"

        # ======================================================
        # VISUALIZATION KEYWORDS
        # ======================================================

        visualization_keywords = [
            "chart",
            "graph",
            "plot",
            "pie",
            "bar",
            "line",
            "scatter",
            "histogram",
            "heatmap",
            "box",
            "dashboard",
            "visualize",
            "visualization",
            "trend",
        ]

        # ======================================================
        # ANALYSIS KEYWORDS
        # ======================================================

        analysis_keywords = [
            "analyze",
            "analysis",
            "summary",
            "statistics",
            "describe",
            "insight",
            "insights",
            "recommend",
            "recommendation",
            "prediction",
            "forecast",
            "correlation",
            "average",
            "mean",
            "maximum",
            "minimum",
            "total",
            "highest",
            "lowest",
            "sales",
            "profit",
            "region",
            "category",
            "product",
            "quantity",
            "kpi",
            "kpis",
            "metric",
            "metrics",
        ]

        has_visual = any(word in query for word in visualization_keywords)
        has_analysis = any(word in query for word in analysis_keywords)

        # ======================================================
        # SMART ROUTING
        # ======================================================

        # Requests that should always return text + chart
        if (
            ("sales" in query and "region" in query)
            or ("sales" in query and "category" in query)
            or ("sales" in query and "product" in query)
            or ("profit" in query and "region" in query)
            or ("profit" in query and "category" in query)
            or ("profit" in query and "product" in query)
            or ("correlation" in query)
            or ("trend" in query)
        ):
            return "BOTH"

        if has_visual and has_analysis:
            return "BOTH"

        if has_visual:
            return "VISUALIZER"

        if has_analysis:
            return "ANALYST"

        # ======================================================
        # LLM FALLBACK
        # ======================================================

        prompt = f"""
{SUPERVISOR_PROMPT}

User Request:
{user_query}

Return ONLY one word.

ANALYST
VISUALIZER
BOTH
REPORT
"""

        response = invoke_llm(prompt).strip().upper()

        if response not in [
            "ANALYST",
            "VISUALIZER",
            "BOTH",
            "REPORT",
        ]:
            return "ANALYST"

        return response