"""Supervisor agent that coordinates research sub-agents."""

from typing import Dict, Any, List
from langgraph.types import Command
from src.state import ResearchState
from src.agents.research_agent import research_sub_agent
import asyncio


async def supervisor_agent(state: ResearchState) -> Command:
    """Supervisor that delegates research to sub-agents.

    This agent:
    1. Takes the sub-topics from the research brief
    2. Spawns parallel research sub-agents for each topic
    3. Aggregates findings from all sub-agents
    4. Decides when research is complete

    Args:
        state: Current research state

    Returns:
        Command to update state with all findings
    """
    sub_topics = state.get("sub_topics", [])
    research_brief = state.get("research_brief", "")

    if not sub_topics:
        # No topics to research, move to report
        return Command(
            update={
                "next_action": "write_report"
            }
        )

    # Execute research for all sub-topics in parallel
    research_tasks = [
        research_sub_agent(topic, research_brief)
        for topic in sub_topics
    ]

    results = await asyncio.gather(*research_tasks)

    # Aggregate all findings and sources
    all_findings = []
    all_sources = []

    for result in results:
        all_findings.append(result)
        all_sources.extend(result.get("sources", []))

    # Return Command to update state
    return Command(
        update={
            "findings": all_findings,
            "sources": all_sources,
            "next_action": "write_report"
        }
    )
