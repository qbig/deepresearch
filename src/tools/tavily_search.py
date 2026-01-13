"""Tavily search tool for web research."""

from typing import List, Dict, Any
from langchain_tavily import TavilySearchResults


def create_tavily_tool(max_results: int = 5) -> TavilySearchResults:
    """Create a Tavily search tool.

    Args:
        max_results: Maximum number of search results to return

    Returns:
        TavilySearchResults tool instance
    """
    return TavilySearchResults(
        max_results=max_results,
        include_answer=True,
        include_raw_content=True,
        include_images=False,
    )


def search_web(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Execute a web search using Tavily.

    Args:
        query: Search query
        max_results: Maximum number of results to return

    Returns:
        List of search results with content and metadata
    """
    tool = create_tavily_tool(max_results=max_results)
    results = tool.invoke({"query": query})
    return results
