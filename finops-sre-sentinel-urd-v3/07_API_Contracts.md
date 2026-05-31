# 07 - API Contracts

**Document:** finops-sre-sentinel URD v3.0  
**Section:** API Contracts  
**Target Audience:** Integration Engineers, Backend Developers  
**Approx Tokens:** ~2,000

---

## 7.1 MCP Protocol Endpoints

The MCP server communicates via **JSON-RPC over SSE (Server-Sent Events)** and **STDIO** for local development.

### 7.1.1 SSE Streaming Endpoint

```
GET /api/v1/stream?client_id={client_id}&events={event_types}
```

**Event Types:**
| Event | Description |
|-------|-------------|
| `tool:execution` | Real-time tool execution progress |
| `tool:result` | Tool execution output |
| `approval:request` | New approval request notification |
| `approval:response` | Approval decision result |
| `audit:event` | New audit log entry |
| `system:status` | Server health and status updates |
| `token:usage` | Real-time token burn rate update |

**Example SSE Stream:**
```
event: tool:execution
data: {"tool_name": "diagnose_transaction_latency", "status": "running", "progress": 45}

event: tool:result
data: {"tool_name": "diagnose_transaction_latency", "status": "completed", "result": {...}}

event: approval:request
data: {"approval_id": "apr_x1y2z3", "risk_score": 7, "action": "restart_pod", "requester": "oncall-sre"}
```

### 7.1.2 Tool Execution

```
POST /api/v1/tools/{tool_name}/execute
Content-Type: application/json
X-API-Key: {api_key}
```

**Request Body:** Tool-specific input schema (see Section 03 - Functional Requirements)

**Response Codes:**
| Code | Description |
|------|-------------|
| **202 Accepted** | Tool execution started (async via SSE) |
| **400 Bad Request** | Invalid input parameters |
| **401 Unauthorized** | Missing or invalid API key |
| **403 Forbidden** | Insufficient RBAC permissions |
| **429 Too Many Requests** | Rate limit exceeded |
| **503 Service Unavailable** | Kill switch active or system in safe mode |

### 7.1.3 Approval Management

```
GET /api/v1/approvals/pending
X-API-Key: {api_key}

POST /api/v1/approvals/{approval_id}
Content-Type: application/json
X-API-Key: {api_key}
```

**POST Request Body:**
```json
{
  "decision": "approve",
  "comments": "Reviewed the impact assessment. Proceed with restart during maintenance window.",
  "reasoning": "Pod is non-critical, replicas healthy, low user impact."
}
```

**Response:**
```json
{
  "approval_id": "apr_x1y2z3",
  "status": "approved",
  "responded_by": "user_marcus_chen",
  "responded_at": "2026-04-27T10:03:00Z",
  "tool_execution_initiated": true
}
```

### 7.1.4 Health Check

```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "uptime_seconds": 86400,
  "active_connections": 5,
  "pending_approvals": 2,
  "tools_registered": 4,
  "registered_tools": [
    "diagnose_transaction_latency",
    "analyze_cloud_spend_anomaly",
    "remediate_unhealthy_pod",
    "verify_compliance_drift"
  ],
  "last_kill_switch": null,
  "audit_log_integrity": "verified",
  "timestamp": "2026-04-27T10:00:00Z"
}
```

### 7.1.5 Kill Switch

```
POST /api/v1/kill-switch/activate
X-API-Key: {api_key}
Content-Type: application/json
```

**Request Body:**
```json
{
  "reason": "Suspicious AI behavior detected - investigating",
  "initiated_by": "user_marcus_chen"
}
```

**Response:**
```json
{
  "status": "activated",
  "terminated_connections": 5,
  "cancelled_executions": 2,
  "timestamp": "2026-04-27T10:05:00.123Z"
}
```

### 7.1.6 Token Usage

```
GET /api/v1/tokens/usage?timeframe={today|week|month}&granularity={per_tool|per_session|per_user}
X-API-Key: {api_key}
```

**Response:**
```json
{
  "timeframe": "today",
  "total_tokens_used": 45600,
  "total_tokens_wasted": 3200,
  "waste_percentage": 7.0,
  "breakdown": {
    "per_tool": {
      "diagnose_transaction_latency": { "used": 15000, "wasted": 800, "waste_reason": "retry_on_timeout" },
      "analyze_cloud_spend_anomaly": { "used": 12000, "wasted": 1200, "waste_reason": "over_query_on_large_dataset" },
      "remediate_unhealthy_pod": { "used": 8600, "wasted": 600, "waste_reason": "approval_wait_loop" },
      "verify_compliance_drift": { "used": 10000, "wasted": 600, "waste_reason": "full_scan_every_call" }
    },
    "per_session": {
      "sess_xyz789": { "used": 22000, "wasted": 1500 },
      "sess_abc123": { "used": 23600, "wasted": 1700 }
    }
  },
  "optimization_recommendations": [
    {
      "issue": "Retry on timeout causing token waste",
      "suggestion": "Implement exponential backoff with max 2 retries",
      "estimated_savings": "15%"
    },
    {
      "issue": "Full compliance scan every call",
      "suggestion": "Cache compliance results for 5 minutes",
      "estimated_savings": "10%"
    },
    {
      "issue": "Approval wait loop polling",
      "suggestion": "Use SSE push instead of polling",
      "estimated_savings": "5%"
    }
  ]
}
```

## 7.2 Error Codes

| Code | Name | HTTP Status | Description |
|------|------|-------------|-------------|
| `TOOL_001` | Tool Not Found | 404 | Requested tool does not exist in registry |
| `TOOL_002` | Execution Timeout | 408 | Tool exceeded maximum execution time (30s) |
| `TOOL_003` | Invalid Parameters | 400 | Input failed JSON Schema validation |
| `AUTH_001` | Invalid API Key | 401 | API key is missing, malformed, or not recognized |
| `AUTH_002` | Insufficient Role | 403 | User role cannot execute this tool |
| `RBAC_001` | Permission Denied | 403 | User lacks required permission for action |
| `PII_001` | Redaction Failure | 500 | PII redaction engine encountered an error |
| `APPR_001` | Approval Required | 202 | Action blocked pending human approval |
| `APPR_002` | Approval Timeout | 408 | Approval SLA exceeded, action auto-escalated |
| `KS_001` | Kill Switch Active | 503 | System in safe mode, no tool execution allowed |
| `MODEL_001` | Model Unavailable | 503 | AI model not reachable, fallback failed |
| `RATE_001` | Rate Limited | 429 | Too many requests, try again later |
| `TOKEN_001` | Budget Exceeded | 403 | Daily token budget exhausted, system in read-only mode |

## 7.3 API Versioning

| Version | Status | Notes |
|---------|--------|-------|
| v1 | Current | This document defines v1 API contracts |
| v2 | Not started | Reserved for future use |

- API version is prefixed in URL path: `/api/v1/...`
- Breaking changes require new version (v2)
- Non-breaking changes (new fields, new endpoints) do not require version bump

*All API endpoints documented here are subject to integration testing before release.*