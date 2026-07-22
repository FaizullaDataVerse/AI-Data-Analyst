from graph.state import AgentState

from agents.supervisor import SupervisorAgent
from agents.analyst import AnalystAgent
from agents.visualizer import VisualizerAgent


supervisor = SupervisorAgent()
analyst = AnalystAgent()
visualizer = VisualizerAgent()


# ======================================================
# Supervisor Node
# ======================================================

def supervisor_node(state: AgentState):

    state["route"] = supervisor.route(state["query"])

    return state


# ======================================================
# Analyst Node
# ======================================================

def analyst_node(state: AgentState):

    analysis = analyst.analyze(
        state["df"],
        state["query"]
    )

    if isinstance(analysis, dict):

        state["analysis"] = analysis.get("report", "")

        state["report"] = analysis.get("report", "")

        state["kpis"] = analysis.get("kpis", {})

        state["tables"] = analysis.get("tables", {})

    else:

        state["analysis"] = analysis

        state["report"] = ""

        state["kpis"] = {}

        state["tables"] = {}

    return state


# ======================================================
# Visualizer Node
# ======================================================

def visualizer_node(state: AgentState):

    query = state["query"]

    if state["route"] == "REPORT":
        query = "dashboard"

    result = visualizer.visualize(
        state["df"],
        query
    )

    # Reset defaults
    state["chart"] = None
    state["dashboard"] = None
    state["charts"] = []
    state["chart_path"] = ""
    state["chart_suggestion"] = ""

    if isinstance(result, dict):

        state["chart"] = result.get("figure")

        state["dashboard"] = result.get("dashboard")

        state["charts"] = result.get("charts", [])

        state["chart_path"] = result.get("path", "")

        state["chart_suggestion"] = result.get(
            "suggestion",
            ""
        )

    return state


# ======================================================
# Final Node
# ======================================================

def final_node(state: AgentState):

    route = state["route"]

    # ----------------------------------------
    # Analyst Only
    # ----------------------------------------

    if route == "ANALYST":

        state["response"] = state["analysis"]

    # ----------------------------------------
    # Visualizer Only
    # ----------------------------------------

    elif route == "VISUALIZER":

        if state["dashboard"]:

            state["response"] = "Dashboard generated successfully."

        elif state["chart"] is not None:

            state["response"] = "Chart generated successfully."

        elif state["chart_suggestion"]:

            state["response"] = (
                f"No chart generated.\n\n"
                f"Suggested chart: {state['chart_suggestion']}"
            )

        else:

            state["response"] = "Unable to generate chart."

    # ----------------------------------------
    # Analysis + Chart
    # ----------------------------------------

    elif route == "BOTH":

        response = state["analysis"]

        if state["dashboard"]:

            response += "\n\n📊 Dashboard generated successfully."

        elif state["chart"] is not None:

            response += "\n\n📈 Chart generated successfully."

        elif state["chart_suggestion"]:

            response += (
                "\n\nSuggested Chart: "
                f"{state['chart_suggestion']}"
            )

        state["response"] = response

    # ----------------------------------------
    # Full Report
    # ----------------------------------------

    elif route == "REPORT":

        state["response"] = state["report"]

    # ----------------------------------------
    # Unknown Route
    # ----------------------------------------

    else:

        state["response"] = "Unable to process request."

    return state