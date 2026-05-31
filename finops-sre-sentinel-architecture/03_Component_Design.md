# 03 - Component Design

**Document:** finops-sre-sentinel Architecture Document  
**Section:** Component Design  
**Target Audience:** Developers, Technical Stakeholders  
**Approx Tokens:** ~3,000

## 3.1 MCP Server Component

The MCP server is the core component of the system, responsible for handling MCP JSON-RPC 2.0 requests, REST API endpoints, and SSE streaming.

### 3.1.1 MCP Server Architecture

The MCP server is built using **FastAPI** and **Python 3.11+**, served by **uvicorn**.

```python
from fastapi import FastAPI

app = FastAPI(title="MCP SRE Sentinel")

# MCP endpoint at /mcp for JSON-RPC 2.0 requests
# REST API at /api/v1/ for direct tool invocation
```

### 3.1.2 Tool Registry and Execution

The MCP server discovers and executes tools via a **ToolRegistry** that dynamically loads tool modules from `src/mcp-server/app/tools/`.

```python
from app.tool_registry import ToolRegistry

registry = ToolRegistry()
registry.discover_tools("app/tools")  # Auto-discovers all tool modules

@app.post("/api/v1/tools/{tool_name}/invoke")
async def invoke_tool(tool_name: str, request: ToolInvokeRequest):
    tool = registry.get_tool(tool_name)
    if tool:
        return await tool.execute(request.input_data)
    else:
        return {"error": "Tool not found", "code": 404}
```

### 3.1.3 Tool Modules

Each tool is a plain Python module (not a class) with an `execute()` function:

- `analyze_cloud_spend_anomaly.py` — Z-score anomaly detection on daily cost data
- `diagnose_transaction_latency.py` — P50/P90/P95/P99 latency classification
- `remediate_unhealthy_pod.py` — Safe pod restart with automatic rollback
- `verify_compliance_drift.py` — Cloud compliance rule-based audit

## 3.2 Security Layer Component

The security layer provides authentication, authorization, and PII redaction.

### 3.2.1 Authentication

The system uses **API Key authentication with SHA-256 hashing** (NOT JWT).

```python
from app.security import Authenticator

authenticator = Authenticator(api_keys=API_KEY_STORE)

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key via X-API-Key header"""
    if not authenticator.verify(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
```

### 3.2.2 Authorization

The system uses **role-based access control (RBAC)** with role enums:

```python
from app.security import Role, check_permission

# Roles: ADMIN, OPERATOR, VIEWER
check_permission(Role.ADMIN, "invoke_tool", "remediate_unhealthy_pod")  # True
check_permission(Role.VIEWER, "invoke_tool", "remediate_unhealthy_pod")  # False
```

### 3.2.3 PII Redaction

The **Redactor** class masks sensitive data in tool outputs:

```python
from app.security import Redactor

redactor = Redactor()
safe_output = redactor.redact(tool_output)  # Masks emails, IPs, account IDs
```

## 3.3 UI Layer Component

The UI layer presents real-time insights and manages approvals.

### 3.3.1 UI Technology Stack

The UI is built using **React 18 (JavaScript, NOT TypeScript)** with the modern `createRoot` API.

```javascript
// src/ui/src/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const root = createRoot(document.getElementById('root'));
root.render(<App />);
```

### 3.3.2 Key Components

| Component | File | Responsibility |
|-----------|------|----------------|
| **DashboardMetrics** | `DashboardMetrics.js` | Real-time metric cards (anomalies, latency, pods, compliance) |
| **ToolRunner** | `ToolRunner.js` | Tool selection, input forms, result display |
| **RealTimeInsights** | `RealTimeInsights.js` | SSE stream for live alerts and insights |
| **ApprovalRequest** | `ApprovalRequest.js` | HITL approval flow for critical actions |

### 3.3.3 Real-time Insights

The UI uses **SSE (Server-Sent Events)** for real-time updates at `/api/v1/stream/insights`:

```javascript
const eventSource = new EventSource('/api/v1/stream/insights');
eventSource.onmessage = (event) => {
  const insight = JSON.parse(event.data);
  // Update dashboard with new insight
};
```

*This section defines the detailed design of individual components. For data flow details, proceed to Section 04.*