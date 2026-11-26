"""
LLM USE CASE: MCP Server (Model Context Protocol)
Examples: expose your DB, APIs, or files as tools any MCP-compatible agent can use

WHY MCP: standard protocol so Claude/Cursor/any agent can discover + call your tools.
WHY not custom API: reusable across clients; self-describing tool schemas.
"""

import json
from mcp.server.fastmcp import FastMCP

# pip install mcp

mcp = FastMCP("interview-demo-server")


# --- Tools: functions the LLM agent can invoke ---
@mcp.tool()
def search_documents(query: str, top_k: int = 5) -> str:
    """Search internal document store by semantic similarity."""
    # Wire to your vector DB (Chroma, Pinecone, etc.)
    results = [
        {"title": "Q3 Report", "snippet": f"Content matching '{query}'...", "score": 0.92},
        {"title": "Product FAQ", "snippet": f"Answer about '{query}'...", "score": 0.87},
    ]
    return json.dumps(results[:top_k])


@mcp.tool()
def get_customer(customer_id: str) -> str:
    """Fetch customer record from CRM by ID."""
    return json.dumps({"id": customer_id, "name": "Acme Corp", "plan": "enterprise"})


@mcp.tool()
def run_sql(query: str) -> str:
    """Execute read-only SQL against analytics database. SELECT only."""
    # WHY read-only: prevent agent from destructive writes
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries allowed"})
    return json.dumps({"rows": [{"metric": "revenue", "value": 1_200_000}]})


# --- Resources: read-only data the agent can fetch ---
@mcp.resource("config://model-settings")
def get_model_settings() -> str:
    """Return current model configuration."""
    return json.dumps({"model": "gpt-4o", "temperature": 0, "max_tokens": 2048})


# --- Prompts: reusable prompt templates ---
@mcp.prompt()
def analyze_data(dataset_name: str) -> str:
    """Generate a data analysis prompt for a given dataset."""
    return f"Analyze the dataset '{dataset_name}'. Summarize key trends, anomalies, and recommendations."


# Run server:
#   mcp run llm/09_mcp_server.py
# Or: python -m mcp.server.fastmcp llm/09_mcp_server.py
#
# Client connects via stdio or SSE:
#   Claude Desktop / Cursor → add to mcp.json:
#   {"mcpServers": {"demo": {"command": "python", "args": ["llm/09_mcp_server.py"]}}}

if __name__ == "__main__":
    mcp.run()
