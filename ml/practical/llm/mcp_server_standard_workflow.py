"""
============================================================
MCP Server (Model Context Protocol) — Standard Workflow
============================================================
MCP is an open standard (Anthropic, 2024) that lets any MCP-compatible
AI client (Claude Desktop, Cursor, Zed, custom agents) discover and call
your server's tools, resources, and prompts — no custom integration per client.

Architecture:
  Client (Claude / agent)  ←──── MCP protocol (JSON-RPC over stdio/SSE) ────→  MCP Server
                                                                                   ├── Tools     (functions agent can call)
                                                                                   ├── Resources (read-only data agent can fetch)
                                                                                   └── Prompts   (reusable prompt templates)

WHY MCP over a custom REST API:
  - Self-describing: server advertises available tools with typed schemas.
  - Client-agnostic: one server works with any MCP-compatible client.
  - Standardised error handling and capability negotiation.
  - Transport-agnostic: stdio (local), SSE (remote), WebSocket.
============================================================

# ============================================================
# Standard MCP Server Workflow
# ============================================================
# 1. Initialise server   — FastMCP("server-name") or low-level Server()
# 2. Register Tools      — @mcp.tool()   functions the LLM can invoke
# 3. Register Resources  — @mcp.resource("uri") read-only data the LLM can read
# 4. Register Prompts    — @mcp.prompt() reusable prompt templates
# 5. Add Middleware      — auth, rate-limiting, logging
# 6. Choose Transport    — stdio (local dev / Claude Desktop) or SSE (remote)
# 7. Run                 — mcp.run() or uvicorn for SSE
# ============================================================
"""

import json
import sqlite3
from datetime import datetime

# pip install mcp
from mcp.server.fastmcp import FastMCP


# ------------------------------------------------------------
# Config (plain constants)
# ------------------------------------------------------------
SERVER_NAME  = "interview-demo-server"
DB_PATH      = ":memory:"   # replace with real path in production
MAX_ROWS     = 100          # cap SQL result set size
ALLOWED_HTTP = {"GET"}      # restrict HTTP tool to read-only verbs


# ------------------------------------------------------------
# Server initialisation
# ------------------------------------------------------------
mcp = FastMCP(
    name=SERVER_NAME,
    # version="1.0.0",      # optional; surfaced to clients
    # description="...",    # optional; shown in Claude Desktop
)


# ============================================================
# TOOLS  — functions the LLM agent can call
# ============================================================
# Rules for good tools:
#   1. One clear action per tool (single responsibility).
#   2. Return JSON strings (easy for LLM to parse).
#   3. Validate inputs and return structured errors (never crash).
#   4. Read-only by default; make writes explicit and confirm-gated.
#   5. Include units/formats in docstrings — the LLM reads them.

@mcp.tool()
def search_knowledge_base(query: str, top_k: int = 5) -> str:
    """Search the internal knowledge base by semantic similarity.

    Args:
        query: Natural-language search query.
        top_k: Number of results to return (1–20).

    Returns:
        JSON list of {title, snippet, score} objects, ranked by relevance.
    """
    # In production: call your vector DB (Chroma, Pinecone, etc.)
    top_k = max(1, min(top_k, 20))     # clamp: never trust LLM-provided numbers
    results = [
        {"title": "Q3 Earnings Report", "snippet": f"Content matching '{query}'...", "score": 0.92},
        {"title": "Product FAQ",         "snippet": f"Answer about '{query}'...",    "score": 0.87},
        {"title": "API Documentation",   "snippet": f"Docs for '{query}'...",        "score": 0.81},
    ]
    return json.dumps(results[:top_k])


@mcp.tool()
def run_sql(query: str) -> str:
    """Execute a read-only SQL SELECT query against the analytics database.

    Args:
        query: A SQL SELECT statement. INSERT/UPDATE/DELETE are rejected.

    Returns:
        JSON object with 'columns' and 'rows', or 'error' on failure.

    WHY read-only: agent should never be able to write/delete data.
    """
    # Guard: only allow SELECT
    if not query.strip().upper().startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})

    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.execute(query)
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchmany(MAX_ROWS)      # cap rows to avoid context overflow
        return json.dumps({"columns": columns, "rows": rows})
    except sqlite3.Error as e:
        return json.dumps({"error": str(e)})
    finally:
        con.close()


@mcp.tool()
def get_current_time(timezone: str = "UTC") -> str:
    """Return the current date and time in ISO 8601 format.

    Args:
        timezone: IANA timezone string (e.g. 'America/New_York'). Default: UTC.

    Returns:
        JSON object with 'datetime', 'timezone', 'unix_timestamp'.
    """
    # Simple UTC-only implementation; use pytz/zoneinfo for real timezones.
    now = datetime.utcnow()
    return json.dumps({
        "datetime":       now.isoformat() + "Z",
        "timezone":       timezone,
        "unix_timestamp": int(now.timestamp()),
    })


@mcp.tool()
def http_get(url: str) -> str:
    """Fetch the text content of a public URL via HTTP GET.

    Args:
        url: The URL to fetch. Must start with https://.

    Returns:
        JSON with 'status_code' and 'body' (first 2000 chars).

    WHY https-only: prevent SSRF against internal services.
    """
    import urllib.request
    import urllib.error

    if not url.startswith("https://"):
        return json.dumps({"error": "Only https:// URLs are allowed (SSRF prevention)."})

    try:
        with urllib.request.urlopen(url, timeout=5) as resp:     # type: ignore[arg-type]
            body = resp.read(2000).decode("utf-8", errors="replace")
            return json.dumps({"status_code": resp.status, "body": body})
    except urllib.error.URLError as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write text content to a file (whitelist-controlled).

    Args:
        path: Relative file path (e.g. 'output/report.txt').
        content: Text to write.

    Returns:
        JSON with 'success' or 'error'.

    WHY whitelist: prevent agent from writing to arbitrary system paths.
    """
    import os

    ALLOWED_DIR = "./agent_output"      # only write inside this dir
    safe_path = os.path.realpath(os.path.join(ALLOWED_DIR, path))

    if not safe_path.startswith(os.path.realpath(ALLOWED_DIR)):
        return json.dumps({"error": "Path traversal detected — write refused."})

    os.makedirs(os.path.dirname(safe_path), exist_ok=True)
    with open(safe_path, "w") as f:
        f.write(content)
    return json.dumps({"success": True, "path": safe_path})


# ============================================================
# RESOURCES  — read-only data the agent can fetch by URI
# ============================================================
# Resources are passive (agent reads them); tools are active (agent calls them).
# Use resources for configuration, static data, and persistent state.

@mcp.resource("config://model-settings")
def get_model_settings() -> str:
    """Current LLM configuration surfaced as a resource.
    URI: config://model-settings
    """
    return json.dumps({
        "model":      "gpt-4o",
        "temperature": 0,
        "max_tokens":  2048,
        "top_p":       1.0,
    })


@mcp.resource("data://schema/tables")
def get_db_schema() -> str:
    """Database schema — agent reads this to construct valid SQL queries.
    URI: data://schema/tables
    """
    schema = {
        "users":   ["id INT", "name TEXT", "email TEXT", "plan TEXT", "created_at TIMESTAMP"],
        "orders":  ["id INT", "user_id INT", "amount FLOAT", "status TEXT", "created_at TIMESTAMP"],
        "metrics": ["date DATE", "revenue FLOAT", "dau INT", "churn_rate FLOAT"],
    }
    return json.dumps(schema, indent=2)


@mcp.resource("docs://readme")
def get_readme() -> str:
    """Server README — tells the agent what this server does and how.
    URI: docs://readme
    """
    return """
    # Interview Demo MCP Server

    ## Tools
    - search_knowledge_base: semantic search over internal docs
    - run_sql: read-only SQL queries
    - get_current_time: current UTC time
    - http_get: fetch public URLs (https only)
    - write_file: write to ./agent_output/ only

    ## Resources
    - config://model-settings: current LLM config
    - data://schema/tables: database table schemas
    - docs://readme: this document

    ## Prompts
    - analyze_dataset: structured data analysis prompt
    - summarize_documents: document summarization prompt
    """


# ============================================================
# PROMPTS  — reusable prompt templates the agent can use
# ============================================================
# Prompts are templates with named parameters.
# The client renders them into a message list before sending to the LLM.

@mcp.prompt()
def analyze_dataset(dataset_name: str, goal: str = "identify trends and anomalies") -> str:
    """Generate a structured data analysis prompt.

    Args:
        dataset_name: Name of the dataset or table to analyse.
        goal: What the analysis should focus on.
    """
    return f"""Analyse the dataset '{dataset_name}'.

Your goal: {goal}

Structure your response as:
1. **Summary** — 2–3 sentences on what the data contains.
2. **Key Trends** — top 3 patterns observed.
3. **Anomalies** — any outliers, missing data, or unexpected values.
4. **Recommendations** — 2–3 actionable next steps.

Be specific and quantify where possible."""


@mcp.prompt()
def summarize_documents(documents: str, max_bullets: int = 5) -> str:
    """Generate a document summarization prompt.

    Args:
        documents: Newline-separated document texts or titles to summarise.
        max_bullets: Maximum bullet points in the summary.
    """
    return f"""Summarise the following documents in {max_bullets} bullet points or fewer.
Be concise. Use plain language. Preserve key facts and numbers.

Documents:
{documents}

Summary:"""


# ============================================================
# Transport + startup
# ============================================================
# stdio  — for local tools (Claude Desktop, Cursor):
#   Add to ~/.config/claude/claude_desktop_config.json:
#   {
#     "mcpServers": {
#       "demo": {
#         "command": "python",
#         "args": ["/path/to/mcp_standard_workflow.py"]
#       }
#     }
#   }
#
# SSE  — for remote/multi-client access:
#   mcp = FastMCP("demo", transport="sse", host="0.0.0.0", port=8000)
#   Run with: python mcp_standard_workflow.py
#   Client connects to: http://localhost:8000/sse

if __name__ == "__main__":
    mcp.run()   # defaults to stdio; set transport="sse" in FastMCP() for remote


# ============================================================
# INTERVIEW EXPLANATION
# ============================================================
# What is MCP?
#   Open protocol (JSON-RPC 2.0) for AI clients to discover and call server
#   capabilities (tools/resources/prompts). Analogous to USB-C: one standard
#   plug that works with any device.
#
# MCP vs REST API:
#   - REST: client must know the API in advance; no self-description.
#   - MCP: server advertises capabilities; client auto-discovers tools.
#   - REST: each AI client needs custom integration code.
#   - MCP: one server works with Claude Desktop, Cursor, Zed, any agent.
#
# MCP vs Function Calling (OpenAI):
#   - Function calling: tool definitions live in the prompt; single-LLM scope.
#   - MCP: tools live in a persistent server; any client can connect.
#   - MCP is framework-agnostic; function calling is OpenAI-specific.
#
# Security checklist (critical for production MCP servers):
#   [ ] Input validation on ALL tool parameters (never trust LLM-generated values).
#   [ ] Read-only DB tools by default; explicit user confirmation for writes.
#   [ ] Whitelist allowed paths for file tools (prevent path traversal).
#   [ ] https-only for HTTP tools (prevent SSRF).
#   [ ] Rate limiting per tool.
#   [ ] Authentication middleware (API key or OAuth).
#   [ ] Audit log all tool calls (what was called, with what args, by whom).
#
# Common follow-up questions:
#   - What is the MCP lifecycle? (init → list_tools → call_tool → shutdown)
#   - Why return JSON strings from tools? (LLMs parse JSON reliably; avoids parsing ambiguity)
#   - How do you handle tool errors? (return {"error": "..."} in JSON; never raise)
#   - stdio vs SSE transport? (stdio = local, single client; SSE = remote, multi-client)
#   - How would you add auth? (middleware that checks Authorization header before routing)
# ============================================================


# ============================================================
# VARIATIONS
# ============================================================
# Low-level MCP (without FastMCP) — for custom control:
#   from mcp.server import Server
#   from mcp.types import Tool, TextContent
#   server = Server("demo")
#   @server.list_tools()
#   async def handle_list_tools() -> list[Tool]: ...
#   @server.call_tool()
#   async def handle_call_tool(name, arguments) -> list[TextContent]: ...
#
# MCP + RAG integration:
#   Expose your RAG pipeline as an MCP tool (search_knowledge_base above).
#   The agent decides when to call it — no hardcoded retrieval.
#
# Streaming responses:
#   Use SSE transport + async generators for long-running tools
#   (e.g., streaming SQL results, progressive file reads).
#
# Multi-server composition:
#   Clients can connect to multiple MCP servers simultaneously.
#   Each server owns a domain (DB server, search server, calendar server).
# ============================================================


# ============================================================
# SUMMARY
# ============================================================
# Use when: exposing tools/data to any MCP-compatible AI client (Claude, Cursor, etc.).
# Core primitives: Tools (actions), Resources (read-only data), Prompts (templates).
# Transport: stdio for local; SSE for remote multi-client.
# Security: validate inputs, read-only by default, whitelist paths, audit logs.
# vs REST: self-describing, client-agnostic, standardised error handling.
# Common mistakes:
#   - Returning unstructured strings (hard for LLM to parse reliably).
#   - No input validation (LLM can hallucinate any parameter value).
#   - Allowing write tools without confirmation gates.
#   - Using stdio transport for a multi-client production server (use SSE).
# ============================================================
