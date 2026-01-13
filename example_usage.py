"""Example usage of the DeepResearch agent."""

import asyncio
import os
from dotenv import load_dotenv
from src.graph import graph


async def main():
    """Run the DeepResearch agent with an example query."""

    # Load environment variables
    load_dotenv()

    # Check for required API keys
    required_keys = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]

    if missing_keys:
        print(f"❌ Missing required API keys: {', '.join(missing_keys)}")
        print("Please set them in your .env file")
        return

    # Example research query
    query = "What are the latest developments in quantum computing in 2025?"

    print("🔬 DeepResearch Agent")
    print("=" * 60)
    print(f"Query: {query}")
    print("=" * 60)

    # Initial state
    initial_state = {
        "query": query,
        "messages": [],
        "needs_clarification": False,
        "clarification_questions": [],
        "research_brief": "",
        "sub_topics": [],
        "current_topic": "",
        "search_queries": [],
        "findings": [],
        "sources": [],
        "final_report": "",
        "next_action": "clarify"
    }

    print("\n🚀 Starting research process...\n")

    # Run the graph
    final_state = await graph.ainvoke(initial_state)

    # Display results
    print("\n" + "=" * 60)
    print("📋 RESEARCH BRIEF")
    print("=" * 60)
    print(final_state.get("research_brief", "No brief generated"))

    print("\n" + "=" * 60)
    print("📊 RESEARCH FINDINGS")
    print("=" * 60)
    findings = final_state.get("findings", [])
    print(f"Investigated {len(findings)} sub-topics")
    print(f"Consulted {len(set(final_state.get('sources', [])))} unique sources")

    print("\n" + "=" * 60)
    print("📝 FINAL REPORT")
    print("=" * 60)
    print(final_state.get("final_report", "No report generated"))

    print("\n" + "=" * 60)
    print("✅ Research complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
