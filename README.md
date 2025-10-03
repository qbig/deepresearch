# DeepResearch Clone

An open-source deep research agent built with **LangGraph**, **OpenAI**, and **Tavily**, inspired by OpenAI's DeepResearch and Google's Gemini Deep Research.

This agent conducts multi-step web research, synthesizes findings from multiple sources, and generates comprehensive research reports with proper citations.

## 🌟 Features

- **Multi-Agent Architecture**: Supervisor coordinates parallel research sub-agents
- **Intelligent Query Planning**: Automatically breaks down complex queries into focused sub-topics
- **Web Search Integration**: Uses Tavily API for real-time web research
- **Citation Tracking**: All findings include proper source attribution
- **Comprehensive Reports**: Generates well-structured markdown reports
- **Visual Debugging**: Built-in LangGraph Studio support for development
- **Full Observability**: LangSmith tracing for monitoring and optimization

## 🏗️ Architecture

The system uses a **3-phase multi-agent workflow**:

### Phase 1: Scope
1. **Clarification**: Analyzes query and identifies if clarification is needed
2. **Brief Generation**: Creates focused research plan with sub-topics

### Phase 2: Research
3. **Supervisor Agent**: Delegates sub-topics to research agents
4. **Research Sub-Agents**: Execute in parallel, each:
   - Generates targeted search queries
   - Searches the web via Tavily
   - Extracts and synthesizes findings with citations
   - Maintains isolated context to prevent "context clash"

### Phase 3: Report
5. **Report Generator**: Synthesizes all findings into comprehensive markdown report

### Workflow Diagram
```
START → clarify → generate_brief → research (supervisor + sub-agents) → write_report → END
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- API Keys:
  - [OpenAI API Key](https://platform.openai.com/api-keys)
  - [Tavily API Key](https://app.tavily.com/)
  - [LangSmith API Key](https://smith.langchain.com/) (optional, for tracing)

### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd deepresearch

# Install dependencies
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Run Example

```bash
python example_usage.py
```

This will run a sample research query and display the complete report.

### 4. Use with LangGraph Studio

For visual debugging and development:

```bash
# Install LangGraph CLI
pip install -U langgraph-cli

# Start development server
langgraph dev
```

Then open the provided URL (typically `http://localhost:8123`) to access LangGraph Studio.

See [studio_instructions.md](studio_instructions.md) for detailed Studio usage.

## 📁 Project Structure

```
deepresearch/
├── src/
│   ├── agents/
│   │   ├── supervisor.py          # Supervisor agent (coordinates sub-agents)
│   │   └── research_agent.py      # Research sub-agent (topic investigation)
│   ├── nodes/
│   │   ├── clarify.py             # Query clarification node
│   │   ├── generate_brief.py      # Research brief generation
│   │   └── write_report.py        # Report synthesis node
│   ├── tools/
│   │   └── tavily_search.py       # Tavily search integration
│   ├── graph.py                   # Main LangGraph definition
│   └── state.py                   # Shared state schema
├── langgraph.json                 # LangGraph configuration
├── pyproject.toml                 # Dependencies
├── .env.example                   # Environment template
├── example_usage.py               # Example script
└── studio_instructions.md         # LangGraph Studio guide
```

## 🔧 Configuration

### Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Tavily (web search)
TAVILY_API_KEY=tvly-...

# LangSmith (optional - for tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2-...
LANGCHAIN_PROJECT=deepresearch-clone
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

### Customization

**Change Models**:
Edit `src/nodes/*.py` and `src/agents/*.py` to use different OpenAI models:
- `gpt-4o`: Best quality (default for research)
- `gpt-4o-mini`: Faster, cheaper (default for clarification)
- `gpt-4-turbo`: Alternative high-quality option

**Adjust Search Depth**:
Modify `max_results` in `src/tools/tavily_search.py` to get more/fewer search results per query.

**Add More Agents**:
Create new agent files in `src/agents/` and integrate them into the supervisor pattern.

## 🎯 Usage Examples

### Programmatic Usage

```python
import asyncio
from src.graph import graph

async def research(query: str):
    initial_state = {
        "query": query,
        "messages": [],
        "needs_clarification": False,
        "clarification_questions": [],
        "research_brief": "",
        "sub_topics": [],
        "findings": [],
        "sources": [],
        "final_report": "",
    }

    result = await graph.ainvoke(initial_state)
    return result["final_report"]

# Run research
report = asyncio.run(research("What are the latest AI breakthroughs in 2025?"))
print(report)
```

### Sample Queries

- "What are the latest developments in quantum computing in 2025?"
- "How has climate change impacted global agriculture in the past 5 years?"
- "What are the most promising renewable energy technologies emerging in 2025?"
- "Analyze the current state of autonomous vehicle regulation worldwide"

## 📊 Monitoring with LangSmith

When LangSmith tracing is enabled:

1. All runs are automatically traced
2. View detailed execution at https://smith.langchain.com/
3. Monitor:
   - Token usage and costs
   - Agent performance
   - Search query effectiveness
   - Error patterns

## 🛠️ Development

### Adding New Features

1. **New Node**: Create in `src/nodes/`, add to graph in `src/graph.py`
2. **New Agent**: Create in `src/agents/`, integrate with supervisor
3. **New Tool**: Create in `src/tools/`, use in research agents

### Testing Changes

```bash
# Start dev server with auto-reload
langgraph dev

# Test in Studio UI or run example
python example_usage.py
```

### Debugging

- **Visual**: Use LangGraph Studio's graph visualization
- **Traces**: Check LangSmith for detailed execution traces
- **Logs**: Add print statements or use Python debugger

## 🔍 How It Works

1. **User submits query** → System analyzes if clarification is needed
2. **Research brief generated** → Query decomposed into 3-5 sub-topics
3. **Supervisor spawns agents** → Each agent investigates one sub-topic in parallel
4. **Agents search the web** → 2-3 targeted searches per topic via Tavily
5. **Findings synthesized** → Each agent extracts key findings with citations
6. **Report generated** → All findings combined into comprehensive markdown report

## 📈 Performance

- **Typical Runtime**: 2-5 minutes depending on query complexity
- **Search Volume**: 10-50+ web searches per research task
- **Sources**: 20-100+ unique sources consulted
- **Cost**: ~$0.50-$2.00 per research task (varies by model and search volume)

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional search providers (Bing, SerpAPI, etc.)
- PDF/document ingestion
- Multi-language support
- Advanced citation formatting
- Report export formats (PDF, DOCX)
- Evaluation benchmarks

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) by LangChain
- Inspired by OpenAI's DeepResearch and Google's Gemini Deep Research
- Powered by [Tavily](https://www.tavily.com/) for agentic web search

---

**Built by Terragon Labs**
