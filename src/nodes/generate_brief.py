"""Generate research brief from user query."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.state import ResearchState


BRIEF_GENERATION_PROMPT = """You are a research planning assistant. Your job is to create a focused research brief.

User query: {query}

Create a research brief that includes:
1. A clear, focused research question
2. Key sub-topics to investigate (3-5 specific areas)
3. The type of information needed

Respond with JSON in this format:
{{
    "research_question": "clear, focused research question",
    "sub_topics": ["topic1", "topic2", "topic3", ...],
    "information_needed": "brief description of what information to find"
}}

Respond ONLY with valid JSON."""


def generate_brief_node(state: ResearchState) -> Dict[str, Any]:
    """Generate a focused research brief from the query.

    Args:
        state: Current research state

    Returns:
        Updated state with research brief and sub-topics
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    messages = [
        SystemMessage(content="You are a research planning expert."),
        HumanMessage(content=BRIEF_GENERATION_PROMPT.format(query=state["query"]))
    ]

    response = llm.invoke(messages)

    # Parse JSON response
    import json
    result = json.loads(response.content)

    research_brief = f"""Research Question: {result['research_question']}

Information Needed: {result['information_needed']}

Sub-topics to investigate:
{chr(10).join(f"- {topic}" for topic in result['sub_topics'])}
"""

    return {
        "research_brief": research_brief,
        "sub_topics": result["sub_topics"],
        "next_action": "research"
    }
