"""Report generation node for synthesizing research findings."""

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.state import ResearchState
import json


REPORT_WRITING_PROMPT = """You are an expert research report writer. Create a comprehensive research report.

Research Brief:
{research_brief}

Research Findings:
{findings}

Sources:
{sources}

Create a well-structured research report in Markdown format that includes:

1. **Executive Summary**: 2-3 paragraph overview of key findings
2. **Main Findings**: Organized by topic with detailed information
3. **Analysis**: Synthesis of findings, patterns, and insights
4. **Conclusion**: Summary of what was learned
5. **Sources**: Numbered list of all sources cited

Format requirements:
- Use proper Markdown headings (##, ###)
- Include inline citations as [1], [2], etc.
- Be comprehensive but concise
- Highlight contradictions or multiple perspectives when present
- Ensure all claims are properly cited

Write the complete report in Markdown format."""


def write_report_node(state: ResearchState) -> Dict[str, Any]:
    """Generate final research report from all findings.

    Args:
        state: Current research state with all findings

    Returns:
        Updated state with final report
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    research_brief = state.get("research_brief", "No research brief provided")
    findings = state.get("findings", [])
    sources = state.get("sources", [])

    # Format findings for the prompt
    findings_text = ""
    for i, finding in enumerate(findings, 1):
        topic = finding.get("topic", "Unknown")
        findings_data = finding.get("findings", {})
        summary = findings_data.get("summary", "")
        key_findings = findings_data.get("key_findings", [])

        findings_text += f"\n\n### Topic {i}: {topic}\n"
        findings_text += f"Summary: {summary}\n\n"
        findings_text += "Key Findings:\n"

        for kf in key_findings:
            findings_text += f"- {kf.get('finding', '')}\n"
            findings_text += f"  Source: {kf.get('source', '')}\n"
            findings_text += f"  Relevance: {kf.get('relevance', '')}\n"

    # Format sources
    sources_text = "\n".join([f"{i+1}. {url}" for i, url in enumerate(set(sources))])

    messages = [
        SystemMessage(content="You are an expert research report writer."),
        HumanMessage(content=REPORT_WRITING_PROMPT.format(
            research_brief=research_brief,
            findings=findings_text,
            sources=sources_text
        ))
    ]

    response = llm.invoke(messages)
    final_report = response.content

    return {
        "final_report": final_report,
        "next_action": "end"
    }
