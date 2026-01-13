"""State schema for the DeepResearch agent."""

from typing import Annotated, List, TypedDict
from langgraph.graph import add_messages
from langchain_core.messages import AnyMessage


class ResearchState(TypedDict):
    """State for the deep research agent.

    This state is shared across all nodes in the graph and tracks
    the entire research process from initial query to final report.
    """

    # User input and clarification
    messages: Annotated[List[AnyMessage], add_messages]
    query: str
    needs_clarification: bool
    clarification_questions: List[str]

    # Research planning
    research_brief: str
    sub_topics: List[str]

    # Research execution
    current_topic: str
    search_queries: List[str]
    findings: Annotated[List[dict], lambda x, y: x + y]  # Accumulate findings
    sources: Annotated[List[str], lambda x, y: x + y]  # Accumulate sources

    # Report generation
    final_report: str

    # Control flow
    next_action: str  # "clarify", "research", "write_report", "end"
