# ============================================================
# FinOps-SRE Sentinel — MCP Server Entry Point
# ============================================================
# Generated based: [Arch_Section_03], [URD_Section_07]
# Target Path: src/mcp-server/app/main.py
# ============================================================

from __future__ import annotations

import asyncio
import hashlib
import json
import random
import time
import uuid
from datetime import datetime, timezone

import structlog
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from app.tool_registry import ToolRegistry

logger = structlog.get_logger(__name__)

# ------------------------------------------------------------------
# Application
# ------------------------------------------------------------------

app = FastAPI(
    title="FinOps-SRE Sentinel MCP Server",
    version="1.0.0",
    description="AI-powered SRE platform — MCP tool execution gateway",
)

# CORS — allow UI on port 3001
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tool registry (auto-discovers tools from app/tools/)
tool_registry = ToolRegistry()

# ------------------------------------------------------------------
# Mock Approval Queue (in-memory for demo)
# ------------------------------------------------------------------

_SEED = int(hashlib.sha256(b"finops-approvals").hexdigest()[:8], 16)

_MOCK_APPROVALS = [
    {
        "id": "apr-001",
        "tool": "remediate_unhealthy_pod",
        "action": "rollback",
        "target": "payment-gateway-7f3a9b2c (payments namespace)",
        "risk_score": 75,
        "risk_label": "high",
        "reason": "CrashLoopBackOff — Application error in payment validator",
        "proposed_command": "kubectl rollout undo deployment/payment-gateway -n payments",
        "requested_by": "sentinel-ai",
        "requested_at": "2025-05-29T22:15:00Z",
        "status": "pending",
    },
    {
        "id": "apr-002",
        "tool": "remediate_unhealthy_pod",
        "action": "scale",
        "target": "event-processor (data namespace)",
        "risk_score": 55,
        "risk_label": "medium",
        "reason": "Insufficient CPU — cluster autoscaler at capacity",
        "proposed_command": "kubectl scale deployment/event-processor -n data --replicas=7",
        "requested_by": "sentinel-ai",
        "requested_at": "2025-05-29T22:18:30Z",
        "status": "pending",
    },
    {
        "id": "apr-003",
        "tool": "verify_compliance_drift",
        "action": "remediate",
        "target": "S3 bucket analytics-raw-events (GDPR-32)",
        "risk_score": 45,
        "risk_label": "medium",
        "reason": "HTTP access allowed — add bucket policy to deny non-TLS requests",
        "proposed_command": "aws s3api put-bucket-policy --bucket analytics-raw-events --policy file://enforce-tls.json",
        "requested_by": "sentinel-ai",
        "requested_at": "2025-05-29T22:22:00Z",
        "status": "pending",
    },
]


# ------------------------------------------------------------------
# Mock SSE Event Stream Data
# ------------------------------------------------------------------

_EVENT_TEMPLATES = [
    {"type": "alert", "severity": "critical", "service": "payment-gateway",
     "message": "Transaction latency p99 exceeded 900ms threshold — 3 occurrences in last 5 minutes",
     "source": "diagnose_transaction_latency"},
    {"type": "alert", "severity": "high", "service": "fraud-detection-engine",
     "message": "Pod fraud-detection-engine-8c4d2e1f restarted 4 times in 10 minutes (CrashLoopBackOff)",
     "source": "remediate_unhealthy_pod"},
    {"type": "cost", "severity": "warning", "service": "Amazon EC2",
     "message": "EC2 spend anomaly detected — 50.7% above baseline in us-east-1",
     "source": "analyze_cloud_spend_anomaly"},
    {"type": "compliance", "severity": "high", "service": "PCI-DSS",
     "message": "PCI-6.3.2 FAIL: CVE-2025-1234 patch overdue by 15 days on payment-gateway",
     "source": "verify_compliance_drift"},
    {"type": "event", "severity": "info", "service": "kubernetes",
     "message": "Node ip-10-0-42-17 cordoned — disk pressure detected, pods rescheduling",
     "source": "remediate_unhealthy_pod"},
    {"type": "cost", "severity": "info", "service": "Amazon RDS",
     "message": "RDS read replica scale-out completed — 2 new replicas in us-east-1c",
     "source": "analyze_cloud_spend_anomaly"},
    {"type": "alert", "severity": "medium", "service": "kyc-verification",
     "message": "Plaid API response time degraded — p95 at 3.2s (SLA: 2s)",
     "source": "diagnose_transaction_latency"},
    {"type": "compliance", "severity": "warning", "service": "SOC 2",
     "message": "GuardDuty disabled in ap-northeast-1 — CC7.2 drift detected",
     "source": "verify_compliance_drift"},
    {"type": "event", "severity": "info", "service": "deployment",
     "message": "auth-service v2.4.1 rollout completed — 3/3 pods healthy",
     "source": "remediate_unhealthy_pod"},
    {"type": "cost", "severity": "info", "service": "AWS Lambda",
     "message": "Lambda cold start optimization applied — avg latency reduced 40%",
     "source": "analyze_cloud_spend_anomaly"},
]


# ------------------------------------------------------------------
# Middleware — Request Logging
# ------------------------------------------------------------------


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "http_request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=duration_ms,
    )
    return response


# ------------------------------------------------------------------
# Health & Readiness
# ------------------------------------------------------------------


@app.get("/", tags=["System"])
async def root():
    return {
        "service": "FinOps-SRE Sentinel MCP Server",
        "version": "1.0.0",
        "mode": "mock",
        "docs": "/docs",
        "mcp_endpoint": "/mcp",
    }


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "mode": "mock",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tools_registered": len(tool_registry.list_tools()),
    }


@app.get("/ready", tags=["System"])
async def readiness():
    return {"status": "ready", "tools_registered": len(tool_registry.list_tools())}


# ------------------------------------------------------------------
# Tool Listing
# ------------------------------------------------------------------


@app.get("/api/v1/tools", tags=["Tools"])
async def list_tools():
    """List all registered MCP tools."""
    return {"tools": tool_registry.list_tools()}


# ------------------------------------------------------------------
# Tool Execution
# ------------------------------------------------------------------


@app.post("/api/v1/tools/{tool_name}/execute", tags=["Tools"])
async def execute_tool(tool_name: str, input_data: dict):
    """
    Execute a registered MCP tool by name.
    """
    tool = tool_registry.get_tool(tool_name)
    if tool is None:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

    try:
        result = await tool.execute(input_data)
        return {"tool": tool_name, "result": result, "executed_at": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        logger.error("tool_execution_failed", tool=tool_name, error=str(exc))
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {exc}") from exc


# ------------------------------------------------------------------
# SSE Event Stream
# ------------------------------------------------------------------


async def _event_generator():
    """Yield SSE events with mock infrastructure telemetry."""
    rng = random.Random()
    idx = 0
    while True:
        event = dict(_EVENT_TEMPLATES[idx % len(_EVENT_TEMPLATES)])
        event["id"] = str(uuid.uuid4())[:8]
        event["timestamp"] = datetime.now(timezone.utc).isoformat()
        yield f"data: {json.dumps(event)}\n\n"
        idx += 1
        await asyncio.sleep(rng.uniform(3.0, 7.0))


@app.get("/api/v1/stream", tags=["SSE"])
async def event_stream():
    """Server-Sent Events endpoint — streams real-time infrastructure events."""
    return StreamingResponse(
        _event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ------------------------------------------------------------------
# Approval Queue
# ------------------------------------------------------------------


@app.get("/api/v1/approvals/pending", tags=["Approvals"])
async def get_pending_approvals():
    """Get all pending approval requests."""
    pending = [a for a in _MOCK_APPROVALS if a["status"] == "pending"]
    return {
        "total_pending": len(pending),
        "approvals": pending,
    }


@app.post("/api/v1/approvals/{approval_id}", tags=["Approvals"])
async def handle_approval(approval_id: str, body: dict):
    """Approve or reject a remediation request."""
    action = body.get("action", "approve")  # "approve" or "reject"
    for approval in _MOCK_APPROVALS:
        if approval["id"] == approval_id:
            if approval["status"] != "pending":
                raise HTTPException(status_code=400, detail=f"Approval {approval_id} already {approval['status']}")
            approval["status"] = "approved" if action == "approve" else "rejected"
            approval["resolved_at"] = datetime.now(timezone.utc).isoformat()
            approval["resolved_by"] = body.get("user", "demo-user")
            return {
                "id": approval_id,
                "status": approval["status"],
                "message": f"Approval {action}d successfully",
            }
    raise HTTPException(status_code=404, detail=f"Approval {approval_id} not found")


# ------------------------------------------------------------------
# Dashboard Summary
# ------------------------------------------------------------------


@app.get("/api/v1/dashboard/summary", tags=["Dashboard"])
async def dashboard_summary():
    """Aggregated dashboard metrics for the overview panel."""
    now = datetime.now(timezone.utc)
    return {
        "uptime_percent": 99.97,
        "monthly_cost_usd": 45_200,
        "cost_trend_percent": -2.3,
        "active_incidents": 3,
        "resolved_today": 12,
        "compliance_score": 63.6,
        "compliance_trend": "stable",
        "total_tools_available": len(tool_registry.list_tools()),
        "tools_executed_today": 47,
        "pending_approvals": len([a for a in _MOCK_APPROVALS if a["status"] == "pending"]),
        "services_monitored": 8,
        "pods_healthy": 28,
        "pods_unhealthy": 5,
        "cluster_nodes": 12,
        "cluster_cpu_percent": 67,
        "cluster_memory_percent": 72,
        "generated_at": now.isoformat(),
    }


# ------------------------------------------------------------------
# MCP JSON-RPC 2.0 Protocol Endpoint
# ------------------------------------------------------------------

_MCP_METHODS: dict[str, Any] = {}


@app.post("/mcp", tags=["MCP"])
async def mcp_endpoint(request_body: dict):
    """MCP JSON-RPC 2.0 compatible endpoint."""
    jsonrpc = request_body.get("jsonrpc", "2.0")
    method = request_body.get("method", "")
    req_id = request_body.get("id")
    params = request_body.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": jsonrpc,
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "finops-sre-sentinel",
                    "version": "1.0.0",
                },
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                },
            },
        }

    if method == "tools/list":
        tools = tool_registry.list_tools()
        mcp_tools = []
        for t in tools:
            tool_obj = tool_registry.get_tool(t["name"])
            mcp_tools.append({
                "name": t["name"],
                "description": t["description"],
                "inputSchema": {"type": "object", "properties": {}},
            })
        return {
            "jsonrpc": jsonrpc,
            "id": req_id,
            "result": {"tools": mcp_tools},
        }

    if method == "tools/call":
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        tool = tool_registry.get_tool(tool_name)
        if tool is None:
            return {
                "jsonrpc": jsonrpc,
                "id": req_id,
                "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"},
            }
        try:
            result = await tool.execute(arguments)
            return {
                "jsonrpc": jsonrpc,
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, default=str)}],
                },
            }
        except Exception as exc:
            return {
                "jsonrpc": jsonrpc,
                "id": req_id,
                "error": {"code": -32000, "message": str(exc)},
            }

    return {
        "jsonrpc": jsonrpc,
        "id": req_id,
        "error": {"code": -32601, "message": f"Method '{method}' not found"},
    }


# ------------------------------------------------------------------
# Audit Trail (in-memory for demo)
# ------------------------------------------------------------------

_AUDIT_LOG: list[dict[str, Any]] = []


def _record_audit(action: str, detail: dict[str, Any]) -> None:
    _AUDIT_LOG.append({
        "action": action,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **detail,
    })
    # Keep last 500 entries
    if len(_AUDIT_LOG) > 500:
        _AUDIT_LOG.pop(0)


@app.get("/api/v1/audit/trail", tags=["Audit"])
async def audit_trail(limit: int = 50):
    """Get recent audit trail entries."""
    return {"entries": _AUDIT_LOG[-limit:], "total": len(_AUDIT_LOG)}


@app.get("/api/v1/dashboard/health-history", tags=["Dashboard"])
async def health_history():
    """Last 24 hours of health data points for charting."""
    rng = random.Random(42)
    now = datetime.now(timezone.utc)
    points = []
    for i in range(24):
        hour = (now.hour - 23 + i) % 24
        base_uptime = 99.95 + rng.uniform(0, 0.05)
        # Simulate one incident hour
        if hour == 14:
            base_uptime = 99.72
        points.append({
            "hour": f"{hour:02d}:00",
            "uptime_percent": round(base_uptime, 2),
            "requests_count": rng.randint(12000, 45000),
            "error_count": rng.randint(0, 15) if hour != 14 else rng.randint(45, 120),
            "avg_latency_ms": rng.randint(45, 120) if hour != 14 else rng.randint(800, 2400),
        })
    return {"history": points, "period": "last_24_hours"}


# ------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)