"""Clarification node to understand user intent."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.state import ResearchState


CLARIFICATION_PROMPT = """You are a research assistant helping to clarify research requests.

Analyze the user's query and determine if it needs clarification. A query needs clarification if:
- It's too vague or broad
- The scope is unclear
- The specific information needed is ambiguous
- Key details are missing

User query: {query}

If clarification is needed, respond with:
{{
    "needs_clarification": true,
    "questions": ["question1", "question2", ...]
}}

If the query is clear enough to proceed, respond with:
{{
    "needs_clarification": false,
    "questions": []
}}

Respond ONLY with valid JSON."""


def clarify_node(state: ResearchState) -> Dict[str, Any]:
    """Determine if the query needs clarification.

    Args:
        state: Current research state

    Returns:
        Updated state with clarification info
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content="You are a helpful research assistant."),
        HumanMessage(content=CLARIFICATION_PROMPT.format(query=state["query"]))
    ]

    response = llm.invoke(messages)

    # Parse JSON response
    import json
    result = json.loads(response.content)

    return {
        "needs_clarification": result["needs_clarification"],
        "clarification_questions": result["questions"],
        "next_action": "generate_brief"  # Always move to brief generation
    }
