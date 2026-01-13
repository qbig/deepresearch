# LangGraph Studio Setup Instructions

## Prerequisites

1. **Install LangGraph CLI**:
   ```bash
   pip install -U langgraph-cli
   ```

2. **Set up API Keys**:
   - Copy `.env.example` to `.env`
   - Fill in your API keys:
     - `OPENAI_API_KEY`: Get from https://platform.openai.com/api-keys
     - `TAVILY_API_KEY`: Get from https://app.tavily.com/
     - `LANGCHAIN_API_KEY`: Get from https://smith.langchain.com/

## Running with LangGraph Studio

### Option 1: Development Mode (Recommended)

Start the development server with auto-reload:

```bash
langgraph dev
```

This will:
- Start a local LangGraph server
- Watch for file changes and auto-reload
- Provide a URL to access LangGraph Studio UI
- Enable debugging and visualization

### Option 2: Production Mode

For production-like testing:

```bash
langgraph up
```

## Using LangGraph Studio UI

1. **Open the Studio URL** provided by `langgraph dev` (typically `http://localhost:8123`)

2. **Select the Graph**: Choose `deep_research` from the dropdown

3. **Input Configuration**:
   - Enter your research query in the input field
   - The initial state will be auto-populated

4. **Run Research**:
   - Click "Submit" to start the research process
   - Watch the graph visualization as it executes

5. **View Results**:
   - **Graph View**: See the flow through nodes (clarify → generate_brief → research → write_report)
   - **State View**: Inspect the state at each step
   - **Trace Mode**: View LangSmith traces directly in Studio

## Graph Visualization

The graph will show the flow:

```
START → clarify → generate_brief → research → write_report → END
```

Each node will light up as it executes, and you can:
- Click on nodes to see their input/output
- Inspect the state changes
- View LLM calls and search results
- Debug any issues

## Tips for Development

1. **Modify Agent Logic**: Edit files in `src/` and the server will auto-reload
2. **Test Different Queries**: Use the Studio UI to quickly test various research queries
3. **Monitor Token Usage**: Check LangSmith for cost and performance metrics
4. **Debug Errors**: Use the trace view to see exactly where issues occur

## LangSmith Integration

Once `LANGCHAIN_TRACING_V2=true` is set:
- All runs are automatically traced
- View traces at https://smith.langchain.com/
- Access traces directly in Studio via "Trace Mode"
- Monitor performance, costs, and quality

## Troubleshooting

**Server won't start**:
- Ensure all dependencies are installed: `pip install -e .`
- Check that `langgraph.json` is properly configured
- Verify `.env` file exists with API keys

**Graph errors**:
- Check LangSmith traces for detailed error info
- Review individual node outputs in Studio
- Ensure API keys are valid and have sufficient credits

**Performance issues**:
- Monitor token usage in LangSmith
- Consider using `gpt-4o-mini` for faster/cheaper operations
- Adjust `max_results` in Tavily search to reduce API calls
