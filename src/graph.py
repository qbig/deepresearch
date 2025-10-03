"""Main LangGraph definition for DeepResearch agent."""

from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import ResearchState
from src.nodes.clarify import clarify_node
from src.nodes.generate_brief import generate_brief_node
from src.agents.supervisor import supervisor_agent
from src.nodes.write_report import write_report_node


def route_after_clarify(state: ResearchState) -> Literal["generate_brief"]:
    """Route after clarification (always to brief generation)."""
    return "generate_brief"


def route_after_brief(state: ResearchState) -> Literal["research"]:
    """Route after brief generation (always to research)."""
    return "research"


def route_after_research(state: ResearchState) -> Literal["write_report"]:
    """Route after research (always to report writing)."""
    return "write_report"


def route_after_report(state: ResearchState) -> Literal["__end__"]:
    """Route after report (always to end)."""
    return "__end__"


# Build the graph
builder = StateGraph(ResearchState)

# Add nodes
builder.add_node("clarify", clarify_node)
builder.add_node("generate_brief", generate_brief_node)
builder.add_node("research", supervisor_agent)
builder.add_node("write_report", write_report_node)

# Add edges
builder.add_edge("__start__", "clarify")
builder.add_conditional_edges(
    "clarify",
    route_after_clarify,
    {"generate_brief": "generate_brief"}
)
builder.add_conditional_edges(
    "generate_brief",
    route_after_brief,
    {"research": "research"}
)
builder.add_conditional_edges(
    "research",
    route_after_research,
    {"write_report": "write_report"}
)
builder.add_conditional_edges(
    "write_report",
    route_after_report,
    {"__end__": END}
)

# Compile the graph
graph = builder.compile()
