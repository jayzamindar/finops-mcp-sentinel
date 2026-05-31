# 02 - MCP Server Prompts

**Document:** finops-sre-sentinel Prompts
**Section:** MCP Server Prompts
**Target Audience:** Code Generation AI (or human developers)

## 2.1 MCP Server Core (main.py)

The MCP server uses **FastAPI** with a lifespan-managed `ToolRegistry`. There is no `fastmcp` library — the server exposes MCP-compatible JSON-RPC 2.0 endpoints directly.

### 2.1.1 Prompt

```python
# Generate or modify MCP server core code
# Stack: FastAPI + uvicorn (NOT fastmcp)
# Key patterns:
#   - Lifespan context manager initializes ToolRegistry on startup
#   - REST endpoints: GET /health, GET /api/v1/tools, POST /api/v1/tools/{name}/invoke
#   - MCP protocol: POST /mcp (JSON-RPC 2.0: initialize, tools/list, tools/call)
#   - SSE stream: GET /api/v1/stream/insights
#   - Security: X-API-Key header required on all endpoints except /health

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from app.tool_registry import ToolRegistry
from app.security import verify_api_key, redact_text

tool_registry: ToolRegistry = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global tool_registry
    tool_registry = ToolRegistry()
    yield

app = FastAPI(title="FinOps SRE Sentinel MCP Server", lifespan=lifespan)
```

## 2.2 Tool Registry (tool_registry.py)

The `ToolRegistry` dynamically discovers tool modules in `app/tools/`, extracts metadata (name, description, inputSchema), and supports `list_tools()` and `call_tool()`.

### 2.2.1 Prompt

```python
# Generate or modify tool registry code
# Key patterns:
#   - Dynamic discovery: scan app/tools/*.py for Tool subclasses
#   - Each tool module exports: tool_name, tool_description, input_schema (JSON Schema dict), execute(args)
#   - ToolRegistry.__init__() discovers and registers all tools
#   - list_tools() returns MCP-compatible tool definitions
#   - call_tool(name, args) executes and returns result

class ToolRegistry:
    def __init__(self):
        self.tools: dict[str, dict] = {}
        self._discover_tools()

    def _discover_tools(self):
        # Scan app/tools/ directory for modules with tool_name, execute
        ...

    def list_tools(self) -> list[dict]:
        # Return MCP tools/list format
        ...

    async def call_tool(self, name: str, arguments: dict) -> dict:
        # Execute tool and return result
        ...
```

## 2.3 Individual Tool Pattern

All 4 tools follow the same pattern: module-level metadata + async `execute()` function. Tools are NOT classes — they are plain modules.

### 2.3.1 Prompt

```python
# Generate a new tool following the existing pattern
# Required module-level exports: tool_name, tool_description, input_schema, execute
# execute() is async, takes a dict, returns a dict with 'content' list

tool_name = "tool_name_here"
tool_description = "MCP-compatible tool description"
input_schema = {
    "type": "object",
    "properties": {
        "param1": {"type": "string", "description": "..."},
    },
    "required": ["param1"],
}

async def execute(args: dict) -> dict:
    param1 = args.get("param1", "default")
    # Business logic here
    return {
        "content": [
            {"type": "text", "text": "Result description"},
            {"type": "text", "text": "Key: Value\nKey2: Value2"},
        ]
    }
```

### 2.3.2 Existing Tools (verify these exist before referencing)

| Tool | Module | Purpose |
|------|--------|---------|
| `analyze_cloud_spend_anomaly` | `tools/analyze_cloud_spend_anomaly.py` | Detect spend anomalies with z-score analysis |
| `diagnose_transaction_latency` | `tools/diagnose_transaction_latency.py` | Classify latency (NORMAL/WARN/CRITICAL) with P50–P99 |
| `remediate_unhealthy_pod` | `tools/remediate_unhealthy_pod.py` | Safe pod restart with confirmation + rollback |
| `verify_compliance_drift` | `tools/verify_compliance_drift.py` | Audit cloud resources against compliance rules |

## 2.4 SSE Stream Endpoint

Real-time insights are pushed to connected UI clients via Server-Sent Events at `GET /api/v1/stream/insights`.

### 2.4.1 Prompt

```python
# Generate SSE endpoint for real-time insights
# Key patterns:
#   - Uses StreamingResponse with text/event-stream media type
#   - Pushes JSON events every 5 seconds
#   - Event types: spend_alert, latency_alert, pod_health, compliance_status

from fastapi.responses import StreamingResponse
import json, asyncio

@app.get("/api/v1/stream/insights")
async def stream_insights(api_key: str = Depends(verify_api_key)):
    async def event_generator():
        while True:
            event_data = {"type": "health_check", "status": "ok", "timestamp": "..."}
            yield f"data: {json.dumps(event_data)}\n\n"
            await asyncio.sleep(5)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

*For UI component prompts, proceed to Section 03.*