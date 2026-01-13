"""Research sub-agent for investigating specific topics."""

from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.tools.tavily_search import search_web


RESEARCH_AGENT_PROMPT = """You are a research agent investigating a specific topic.

Research Brief: {research_brief}

Your assigned topic: {topic}

Your task:
1. Generate 2-3 targeted search queries for this topic
2. You'll receive search results for each query
3. Extract key findings with proper citations
4. Summarize the most important information

Respond with JSON containing your search queries:
{{
    "search_queries": ["query1", "query2", "query3"]
}}

Respond ONLY with valid JSON."""


SYNTHESIS_PROMPT = """You are synthesizing research findings for a specific topic.

Topic: {topic}
Research Brief: {research_brief}

Search Results:
{search_results}

Extract and synthesize the key findings:
- Focus on factual information with citations
- Include source URLs for verification
- Highlight contradictions or multiple perspectives if present
- Keep findings concise but comprehensive

Respond with JSON:
{{
    "key_findings": [
        {{
            "finding": "specific finding text",
            "source": "source URL",
            "relevance": "why this matters for the research"
        }},
        ...
    ],
    "summary": "brief 2-3 sentence summary of findings for this topic"
}}

Respond ONLY with valid JSON."""


async def research_sub_agent(topic: str, research_brief: str) -> Dict[str, Any]:
    """Execute research for a specific sub-topic.

    Args:
        topic: The sub-topic to research
        research_brief: The overall research brief for context

    Returns:
        Research findings with citations
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    # Step 1: Generate search queries
    messages = [
        SystemMessage(content="You are a research expert."),
        HumanMessage(content=RESEARCH_AGENT_PROMPT.format(
            research_brief=research_brief,
            topic=topic
        ))
    ]

    response = llm.invoke(messages)

    import json
    queries_result = json.loads(response.content)
    search_queries = queries_result["search_queries"]

    # Step 2: Execute searches
    all_results = []
    sources = []

    for query in search_queries:
        results = search_web(query, max_results=5)
        for result in results:
            all_results.append({
                "query": query,
                "content": result.get("content", ""),
                "url": result.get("url", ""),
                "title": result.get("title", "")
            })
            if result.get("url"):
                sources.append(result["url"])

    # Step 3: Synthesize findings
    search_results_text = "\n\n".join([
        f"Query: {r['query']}\nTitle: {r['title']}\nURL: {r['url']}\nContent: {r['content'][:500]}..."
        for r in all_results
    ])

    synthesis_messages = [
        SystemMessage(content="You are a research synthesis expert."),
        HumanMessage(content=SYNTHESIS_PROMPT.format(
            topic=topic,
            research_brief=research_brief,
            search_results=search_results_text
        ))
    ]

    synthesis_response = llm.invoke(synthesis_messages)
    findings = json.loads(synthesis_response.content)

    return {
        "topic": topic,
        "search_queries": search_queries,
        "findings": findings,
        "sources": list(set(sources))  # Deduplicate sources
    }
