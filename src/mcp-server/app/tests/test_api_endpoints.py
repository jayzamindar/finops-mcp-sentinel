# ============================================================
# FinOps-SRE Sentinel — API Integration Tests
# ============================================================
# Tests all REST API endpoints against the running FastAPI app.
# Run with: pytest app/tests/ -v
# ============================================================

import pytest


class TestHealthEndpoints:
    """Test health and root endpoints."""

    def test_health_check(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert data["mode"] == "mock"
        assert "timestamp" in data
        assert "version" in data
        assert "tools_registered" in data

    def test_root(self, client):
        res = client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert "service" in data
        assert data["mode"] == "mock"
        assert data["mcp_endpoint"] == "/mcp"

    def test_readiness(self, client):
        res = client.get("/ready")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ready"
        assert data["tools_registered"] == 4


class TestToolEndpoints:
    """Test MCP tool listing and execution."""

    def test_list_tools(self, client):
        res = client.get("/api/v1/tools")
        assert res.status_code == 200
        data = res.json()
        assert "tools" in data
        tools = data["tools"]
        assert len(tools) == 4
        tool_names = [t["name"] for t in tools]
        assert "analyze_cloud_spend_anomaly" in tool_names
        assert "diagnose_transaction_latency" in tool_names
        assert "remediate_unhealthy_pod" in tool_names
        assert "verify_compliance_drift" in tool_names

    def test_execute_cloud_spend(self, client):
        res = client.post("/api/v1/tools/analyze_cloud_spend_anomaly/execute", json={
            "namespace": "production",
            "cost_threshold_percent": 20,
            "include_forecasts": True,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["tool"] == "analyze_cloud_spend_anomaly"
        assert "result" in data
        assert "executed_at" in data
        assert "anomaly_detected" in data["result"]

    def test_execute_latency(self, client):
        res = client.post("/api/v1/tools/diagnose_transaction_latency/execute", json={
            "service_name": "payment-gateway",
            "threshold_ms": 500,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["tool"] == "diagnose_transaction_latency"
        assert "latency_p99_ms" in data["result"]

    def test_execute_pod_remediation(self, client):
        res = client.post("/api/v1/tools/remediate_unhealthy_pod/execute", json={
            "namespace": "production",
            "auto_approve": False,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["tool"] == "remediate_unhealthy_pod"
        assert "pods" in data["result"]

    def test_execute_compliance(self, client):
        res = client.post("/api/v1/tools/verify_compliance_drift/execute", json={})
        assert res.status_code == 200
        data = res.json()
        assert data["tool"] == "verify_compliance_drift"
        assert "frameworks" in data["result"]

    def test_unknown_tool(self, client):
        res = client.post("/api/v1/tools/nonexistent_tool/execute", json={})
        assert res.status_code == 404


class TestApprovalEndpoints:
    """Test approval queue lifecycle."""

    def test_pending_approvals(self, client):
        res = client.get("/api/v1/approvals/pending")
        assert res.status_code == 200
        data = res.json()
        assert "approvals" in data
        assert "total_pending" in data
        assert isinstance(data["approvals"], list)
        assert len(data["approvals"]) > 0

    def test_approve_request(self, client):
        # Get pending approvals
        res = client.get("/api/v1/approvals/pending")
        approvals = res.json()["approvals"]
        assert len(approvals) > 0
        aid = approvals[0]["id"]
        # Approve it
        res = client.post(f"/api/v1/approvals/{aid}", json={
            "action": "approve",
            "user": "test-operator",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "approved"
        assert data["id"] == aid

    def test_reject_request(self, client):
        # Use a fresh request - get pending, pick second one
        res = client.get("/api/v1/approvals/pending")
        approvals = res.json()["approvals"]
        # Find one that's still pending
        target = None
        for a in approvals:
            if a["status"] == "pending":
                target = a
                break
        if target:
            res = client.post(f"/api/v1/approvals/{target['id']}", json={
                "action": "reject",
                "user": "test-operator",
            })
            assert res.status_code == 200
            assert res.json()["status"] == "rejected"

    def test_invalid_approval(self, client):
        res = client.post("/api/v1/approvals/nonexistent-id", json={
            "action": "approve",
            "user": "test",
        })
        assert res.status_code == 404


class TestDashboardEndpoints:
    """Test dashboard summary and stats."""

    def test_dashboard_summary(self, client):
        res = client.get("/api/v1/dashboard/summary")
        assert res.status_code == 200
        data = res.json()
        assert "active_incidents" in data
        assert "monthly_cost_usd" in data
        assert "compliance_score" in data
        assert "uptime_percent" in data
        assert "pods_healthy" in data
        assert "pods_unhealthy" in data
        assert "cluster_cpu_percent" in data
        assert "cluster_memory_percent" in data
        assert "pending_approvals" in data

    def test_health_history(self, client):
        res = client.get("/api/v1/dashboard/health-history")
        assert res.status_code == 200
        data = res.json()
        assert "history" in data
        assert data["period"] == "last_24_hours"
        assert len(data["history"]) == 24


class TestAuditEndpoints:
    """Test audit trail endpoints."""

    def test_audit_trail(self, client):
        res = client.get("/api/v1/audit/trail")
        assert res.status_code == 200
        data = res.json()
        assert "entries" in data
        assert "total" in data


class TestSSEStream:
    """Test SSE event stream."""

    def test_stream_endpoint_exists(self):
        """Verify the SSE stream route is registered in the app."""
        # Cannot use TestClient for infinite SSE streams — httpx blocks.
        # Instead, verify the route is registered and has correct path/method.
        from app.main import app
        routes = {r.path: r for r in app.routes if hasattr(r, "path")}
        assert "/api/v1/stream" in routes
        route = routes["/api/v1/stream"]
        # Starlette FunctionRoute stores allowed methods
        assert "GET" in route.methods


class TestMCPProtocol:
    """Test MCP JSON-RPC 2.0 protocol endpoints."""

    def test_mcp_initialize(self, client):
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 1
        result = data["result"]
        assert result["protocolVersion"] == "2024-11-05"
        assert result["serverInfo"]["name"] == "finops-sre-sentinel"
        assert "capabilities" in result

    def test_mcp_tools_list(self, client):
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 2
        tools = data["result"]["tools"]
        assert len(tools) == 4
        tool_names = [t["name"] for t in tools]
        assert "analyze_cloud_spend_anomaly" in tool_names

    def test_mcp_tool_call(self, client):
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "analyze_cloud_spend_anomaly",
                "arguments": {"namespace": "production"},
            },
            "id": 3,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == 3
        assert "result" in data
        content = data["result"]["content"]
        assert len(content) > 0
        assert content[0]["type"] == "text"

    def test_mcp_unknown_method(self, client):
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "unknown/method",
            "id": 4,
        })
        assert res.status_code == 200
        data = res.json()
        assert "error" in data
        assert data["error"]["code"] == -32601

    def test_mcp_unknown_tool_call(self, client):
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": "nonexistent", "arguments": {}},
            "id": 5,
        })
        assert res.status_code == 200
        data = res.json()
        assert "error" in data
        assert data["error"]["code"] == -32601