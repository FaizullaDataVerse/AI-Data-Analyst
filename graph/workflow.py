from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from graph.nodes import (
    supervisor_node,
    analyst_node,
    visualizer_node,
    final_node,
)

builder = StateGraph(AgentState)

# ======================================================
# Nodes
# ======================================================

builder.add_node("Supervisor", supervisor_node)
builder.add_node("Analyst", analyst_node)
builder.add_node("Visualizer", visualizer_node)
builder.add_node("Final", final_node)

# ======================================================
# Start
# ======================================================

builder.add_edge(START, "Supervisor")


# ======================================================
# Router
# ======================================================

def router(state: AgentState):
    return state["route"]


# ======================================================
# Supervisor Routing
# ======================================================

builder.add_conditional_edges(
    "Supervisor",
    router,
    {
        "ANALYST": "Analyst",
        "VISUALIZER": "Visualizer",
        "BOTH": "Analyst",
        "REPORT": "Analyst",
    },
)

# ======================================================
# Analyst Routing
# ======================================================

builder.add_conditional_edges(
    "Analyst",
    lambda state: state["route"],
    {
        "ANALYST": "Final",
        "BOTH": "Visualizer",
        "REPORT": "Visualizer",
    },
)

# ======================================================
# Visualizer -> Final
# ======================================================

builder.add_edge("Visualizer", "Final")

# ======================================================
# Final -> END
# ======================================================

builder.add_edge("Final", END)

# ======================================================
# Compile Graph
# ======================================================

graph = builder.compile()