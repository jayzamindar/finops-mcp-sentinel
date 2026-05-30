# 🧪 Testing Instructions — FinOps-SRE Sentinel

Comprehensive testing guide for the FinOps-SRE Sentinel MCP Server. This document covers automated test suites, manual testing procedures, expected results, and troubleshooting steps.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Automated Test Suite](#automated-test-suite)
3. [Expected Test Results](#expected-test-results)
4. [Manual API Testing](#manual-api-testing)
5. [MCP Protocol Testing](#mcp-protocol-testing)
6. [Dashboard UI Testing](#dashboard-ui-testing)
7. [Docker Integration Testing](#docker-integration-testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.11+ | Backend runtime |
| Node.js | 18+ | Frontend runtime |
| Docker | 24+ | Container runtime (optional) |
| Docker Compose | 2.20+ | Multi-container orchestration (optional) |
| pip | 23+ | Python package manager |
| npm | 9+ | Node.js package manager |

### Verify Prerequisites

```bash
python --version    # Should show 3.11+
node --version      # Should show 18+
docker --version    # Should show 24+
docker compose version  # Should show 2.20+
```

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/jayzamindar/finops-mcp-sentinel.git
cd finops-mcp-sentinel

# Copy environment template
cp .env.example .env
```

---

## Automated Test Suite

### Running All Tests

```bash
cd src/mcp-server

# Create and activate virtual environment (if not done)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run all tests with verbose output
python -m pytest app/tests/ -v -o "addopts="
```

### Running Individual Test Suites

```bash
# API endpoint tests only (22 tests)
python -m pytest app/tests/test_api_endpoints.py -v

# Tool unit tests only (14 tests)
python -m pytest app/tests/test_tools.py -v
```

### Running Specific Test Classes

```bash
# Health check tests
python -m pytest app/tests/test_api_endpoints.py::TestHealthEndpoints -v

# MCP protocol tests
python -m pytest app/tests/test_api_endpoints.py::TestMCPProtocol -v

# Approval flow tests
python -m pytest app/tests/test_api_endpoints.py::TestApprovalEndpoints -v

# Cloud spend tool tests
python -m pytest app/tests/test_tools.py::TestAnalyzeCloudSpendAnomaly -v
```

### Running with Coverage (Optional)

```bash
pip install pytest-cov
python -m pytest app/tests/ -v --cov=app --cov-report=term-missing
```

---

## Expected Test Results

### Successful Run — 36/36 Tests Pass

```
========================================= test session starts ==========================================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: finops-sre-sentinel
plugins: anyio-4.13.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO

app/tests/test_api_endpoints.py::TestHealthEndpoints::test_health_check          PASSED  [  2%]
app/tests/test_api_endpoints.py::TestHealthEndpoints::test_root                   PASSED  [  5%]
app/tests/test_api_endpoints.py::TestHealthEndpoints::test_readiness              PASSED  [  8%]
app/tests/test_api_endpoints.py::TestToolEndpoints::test_list_tools               PASSED  [ 11%]
app/tests/test_api_endpoints.py::TestToolEndpoints::test_execute_cloud_spend      PASSED  [ 13%]
app/tests/test_api_endpoints.py::TestToolEndpoints::test_execute_latency          PASSED  [ 16%]
app/tests/test_api_endpoints.py::TestToolEndpoints::test_execute_pod_remediation  PASSED  [ 19%]
app/tests/test_api_endpoints.py::TestToolEndpoints::test_execute_compliance       PASSED  [ 22%]
app/tests/test_api_endpoints.py::TestToolEndpoints::test_unknown_tool             PASSED  [ 25%]
app/tests/test_api_endpoints.py::TestApprovalEndpoints::test_pending_approvals    PASSED  [ 27%]
app/tests/test_api_endpoints.py::TestApprovalEndpoints::test_approve_request      PASSED  [ 30%]
app/tests/test_api_endpoints.py::TestApprovalEndpoints::test_reject_request       PASSED  [ 33%]
app/tests/test_api_endpoints.py::TestApprovalEndpoints::test_invalid_approval     PASSED  [ 36%]
app/tests/test_api_endpoints.py::TestDashboardEndpoints::test_dashboard_summary   PASSED  [ 38%]
app/tests/test_api_endpoints.py::TestDashboardEndpoints::test_health_history      PASSED  [ 41%]
app/tests/test_api_endpoints.py::TestAuditEndpoints::test_audit_trail             PASSED  [ 44%]
app/tests/test_api_endpoints.py::TestSSEStream::test_stream_endpoint_exists       PASSED  [ 47%]
app/tests/test_api_endpoints.py::TestMCPProtocol::test_mcp_initialize             PASSED  [ 50%]
app/tests/test_api_endpoints.py::TestMCPProtocol::test_mcp_tools_list             PASSED  [ 52%]
app/tests/test_api_endpoints.py::TestMCPProtocol::test_mcp_tool_call              PASSED  [ 55%]
app/tests/test_api_endpoints.py::TestMCPProtocol::test_mcp_unknown_method         PASSED  [ 58%]
app/tests/test_api_endpoints.py::TestMCPProtocol::test_mcp_unknown_tool_call      PASSED  [ 61%]
app/tests/test_tools.py::TestAnalyzeCloudSpendAnomaly::test_returns_required_fields    PASSED [63%]
app/tests/test_tools.py::TestAnalyzeCloudSpendAnomaly::test_deterministic_output       PASSED [66%]
app/tests/test_tools.py::TestAnalyzeCloudSpendAnomaly::test_forecasts_included         PASSED [69%]
app/tests/test_tools.py::TestAnalyzeCloudSpendAnomaly::test_forecasts_excluded         PASSED [72%]
app/tests/test_tools.py::TestAnalyzeCloudSpendAnomaly::test_top_charges_sorted_by_delta PASSED [75%]
app/tests/test_tools.py::TestDiagnoseTransactionLatency::test_returns_required_fields  PASSED [77%]
app/tests/test_tools.py::TestDiagnoseTransactionLatency::test_deterministic_output     PASSED [80%]
app/tests/test_tools.py::TestDiagnoseTransactionLatency::test_percentile_ordering      PASSED [83%]
app/tests/test_tools.py::TestRemediateUnhealthyPod::test_returns_required_fields       PASSED [86%]
app/tests/test_tools.py::TestRemediateUnhealthyPod::test_high_risk_needs_approval      PASSED [88%]
app/tests/test_tools.py::TestRemediateUnhealthyPod::test_deterministic_output          PASSED [91%]
app/tests/test_tools.py::TestVerifyComplianceDrift::test_returns_required_fields       PASSED [94%]
app/tests/test_tools.py::TestVerifyComplianceDrift::test_specific_frameworks           PASSED [97%]
app/tests/test_tools.py::TestVerifyComplianceDrift::test_deterministic_output          PASSED [100%]

=========================================== warnings summary ===========================================
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
==================================== 36 passed, 1 warning in 0.25s =====================================
```

### What Each Test Validates

#### `test_api_endpoints.py` — 22 Tests

| Test Class | Test | What It Validates |
|------------|------|-------------------|
| **TestHealthEndpoints** (3) | `test_health_check` | `GET /health` returns status 200 with health fields |
| | `test_root` | `GET /` returns welcome message |
| | `test_readiness` | `GET /ready` returns readiness status |
| **TestToolEndpoints** (6) | `test_list_tools` | `GET /api/v1/tools` returns tool array with schemas |
| | `test_execute_cloud_spend` | Execute `analyze_cloud_spend_anomaly` via REST |
| | `test_execute_latency` | Execute `diagnose_transaction_latency` via REST |
| | `test_execute_pod_remediation` | Execute `remediate_unhealthy_pod` via REST |
| | `test_execute_compliance` | Execute `verify_compliance_drift` via REST |
| | `test_unknown_tool` | Unknown tool returns 404 |
| **TestApprovalEndpoints** (4) | `test_pending_approvals` | `GET /api/v1/approvals/pending` returns array |
| | `test_approve_request` | Approve a pending request updates status |
| | `test_reject_request` | Reject a pending request updates status |
| | `test_invalid_approval` | Invalid approval ID returns error |
| **TestDashboardEndpoints** (2) | `test_dashboard_summary` | `GET /api/v1/dashboard/summary` returns metrics |
| | `test_health_history` | Health history endpoint returns data |
| **TestAuditEndpoints** (1) | `test_audit_trail` | `GET /api/v1/audit/trail` returns audit entries |
| **TestSSEStream** (1) | `test_stream_endpoint_exists` | `GET /api/v1/stream` route is registered |
| **TestMCPProtocol** (5) | `test_mcp_initialize` | MCP `initialize` method returns capabilities |
| | `test_mcp_tools_list` | MCP `tools/list` returns 4 tools |
| | `test_mcp_tool_call` | MCP `tools/call` executes tool successfully |
| | `test_mcp_unknown_method` | Unknown MCP method returns error |
| | `test_mcp_unknown_tool_call` | Unknown tool call returns error |

#### `test_tools.py` — 14 Tests

| Test Class | Test | What It Validates |
|------------|------|-------------------|
| **TestAnalyzeCloudSpendAnomaly** (5) | `test_returns_required_fields` | Output has all required fields |
| | `test_deterministic_output` | Same inputs → identical outputs (excluding timestamps) |
| | `test_forecasts_included` | `include_forecasts=true` adds forecast fields |
| | `test_forecasts_excluded` | `include_forecasts=false` omits forecast fields |
| | `test_top_charges_sorted_by_delta` | Charges sorted by absolute delta descending |
| **TestDiagnoseTransactionLatency** (3) | `test_returns_required_fields` | Output has all required fields |
| | `test_deterministic_output` | Same inputs → identical outputs |
| | `test_percentile_ordering` | P50 ≤ P95 ≤ P99 |
| **TestRemediateUnhealthyPod** (3) | `test_returns_required_fields` | Output has all required fields |
| | `test_high_risk_needs_approval` | High-risk pods require approval |
| | `test_deterministic_output` | Same inputs → identical outputs |
| **TestVerifyComplianceDrift** (3) | `test_returns_required_fields` | Output has all required fields |
| | `test_specific_frameworks` | Requesting PCI-DSS/SOC2 returns those frameworks |
| | `test_deterministic_output` | Same inputs → identical outputs |

---

## Manual API Testing

### Start the Server

```bash
cd src/mcp-server
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Health Checks

```bash
# Root endpoint
curl http://localhost:8080/
# Expected: {"message": "FinOps-SRE Sentinel MCP Server", "version": "1.0.0", ...}

# Health check
curl http://localhost:8080/health
# Expected: {"status": "healthy", "timestamp": "...", ...}

# Readiness check
curl http://localhost:8080/ready
# Expected: {"ready": true, ...}
```

### List Tools

```bash
curl http://localhost:8080/api/v1/tools
# Expected: Array of 4 tools, each with name, description, input_schema
```

### Execute Tools

```bash
# Cloud spend anomaly analysis
curl -X POST http://localhost:8080/api/v1/tools/analyze_cloud_spend_anomaly/execute \
  -H "Content-Type: application/json" \
  -d '{"namespace": "production", "cost_threshold_percent": 20, "include_forecasts": true}'
# Expected: JSON with baseline_monthly_cost_usd, anomaly_detected, top_charges, etc.

# Transaction latency diagnosis
curl -X POST http://localhost:8080/api/v1/tools/diagnose_transaction_latency/execute \
  -H "Content-Type: application/json" \
  -d '{"service_name": "payment-gateway", "threshold_ms": 500, "limit": 10}'
# Expected: JSON with latency_p50_ms, latency_p95_ms, slow_traces_detail, etc.

# Pod remediation
curl -X POST http://localhost:8080/api/v1/tools/remediate_unhealthy_pod/execute \
  -H "Content-Type: application/json" \
  -d '{"auto_approve": false}'
# Expected: JSON with pods array, pending_approval count, risk scores

# Compliance verification
curl -X POST http://localhost:8080/api/v1/tools/verify_compliance_drift/execute \
  -H "Content-Type: application/json" \
  -d '{"frameworks": ["PCI-DSS", "SOC2", "GDPR"]}'
# Expected: JSON with frameworks object, findings array, overall_compliance_score
```

### Approval Flow

```bash
# Get pending approvals (run after executing remediate_unhealthy_pod)
curl http://localhost:8080/api/v1/approvals/pending
# Expected: Array of approval requests with IDs, actions, risk scores

# Approve a request
curl -X POST http://localhost:8080/api/v1/approvals/{approval-id} \
  -H "Content-Type: application/json" \
  -d '{"action": "approve", "approver": "sre-lead"}'
# Expected: {"status": "approved", ...}

# Reject a request
curl -X POST http://localhost:8080/api/v1/approvals/{approval-id} \
  -H "Content-Type: application/json" \
  -d '{"action": "reject", "approver": "sre-lead"}'
# Expected: {"status": "rejected", ...}
```

### Dashboard & Audit

```bash
# Dashboard summary
curl http://localhost:8080/api/v1/dashboard/summary
# Expected: JSON with total_executions, approval_stats, recent_events, etc.

# Audit trail
curl http://localhost:8080/api/v1/audit/trail
# Expected: Array of audit entries with tool, input, output, timestamp
```

---

## MCP Protocol Testing

### Using curl (JSON-RPC 2.0)

```bash
# Initialize MCP session
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
  }'
# Expected: {"jsonrpc": "2.0", "id": 1, "result": {"capabilities": {...}, "serverInfo": {...}}}

# List available tools
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
# Expected: {"jsonrpc": "2.0", "id": 2, "result": {"tools": [...4 tools...]}}

# Call a tool via MCP
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "verify_compliance_drift",
      "arguments": {"frameworks": ["PCI-DSS"]}
    }
  }'
# Expected: {"jsonrpc": "2.0", "id": 3, "result": {"content": [{...compliance data...}]}}
```

### Using Claude Desktop

1. Open Claude Desktop settings
2. Add to `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "finops-sre-sentinel": {
         "url": "http://localhost:8080/mcp"
       }
     }
   }
   ```
3. Restart Claude Desktop
4. The 4 tools should appear in the tool list
5. Ask Claude: *"What's our cloud spend anomaly status for production namespace?"*

---

## Dashboard UI Testing

### Start the UI

```bash
cd src/ui
npm install
REACT_APP_API_URL=http://localhost:8080 npm start
# Opens http://localhost:3001
```

### Manual UI Tests

| Tab | Test Steps | Expected Result |
|-----|-----------|-----------------|
| **Overview** | Load the page | KPI metrics cards, recent events list, pending approvals count |
| **Live Stream** | Click "Live Stream" tab | SSE event feed shows streaming events |
| **Approvals** | Click "Approvals" tab | List of pending approvals with Approve/Reject buttons |
| **Tool Runner** | Click "Tool Runner" tab | Tool selection dropdown, JSON parameter editor, Execute button |
| **Tool Runner** | Select a tool, click Execute | Results displayed in response panel |

---

## Docker Integration Testing

### Full Stack Test

```bash
# Build and start all services
docker compose up --build -d

# Wait for containers to be healthy
docker compose ps
# Expected: mcp-server (healthy), ui (healthy)

# Test MCP server
curl http://localhost:8080/health
# Expected: {"status": "healthy", ...}

# Test UI
curl http://localhost:3001
# Expected: HTML response (React app)

# Run tests inside container
docker compose exec mcp-server python -m pytest app/tests/ -v
# Expected: 36 passed

# View logs
docker compose logs mcp-server --tail=50
docker compose logs ui --tail=50

# Stop all services
docker compose down
```

---

## Troubleshooting

### Common Issues and Fixes

#### 1. `ModuleNotFoundError: No module named 'app'`

**Cause:** Running pytest from wrong directory.

**Fix:**
```bash
cd src/mcp-server
python -m pytest app/tests/ -v
```

The tests must be run from `src/mcp-server/` where `app/` is a valid Python package.

---

#### 2. `ImportError: No module named 'fastapi'`

**Cause:** Dependencies not installed.

**Fix:**
```bash
cd src/mcp-server
pip install -r requirements.txt
```

---

#### 3. `E   AssertionError` on deterministic tests

**Cause:** Test comparing timestamps that differ between runs.

**Fix:** This should not happen — the test suite strips timestamp fields before comparison. If it does:
```bash
# Update to latest code
git pull origin master
python -m pytest app/tests/test_tools.py -v
```

---

#### 4. `ConnectionRefusedError` on API tests

**Cause:** Test client can't connect to the server.

**Fix:** The tests use FastAPI's `TestClient` (in-process, no server needed). If you see this:
```bash
pip install httpx
python -m pytest app/tests/ -v
```

---

#### 5. `Port 8080 already in use`

**Cause:** Another process is using port 8080.

**Fix:**
```bash
# Find and kill the process (Windows)
netstat -ano | findstr :8080
taskkill /PID <pid> /F

# Find and kill the process (Linux/Mac)
lsof -i :8080
kill -9 <pid>
```

---

#### 6. `docker compose up` fails with build errors

**Cause:** Docker build context issues or missing files.

**Fix:**
```bash
# Clean rebuild
docker compose down
docker compose build --no-cache
docker compose up --build
```

---

#### 7. Frontend shows "Network Error" or can't reach API

**Cause:** CORS issue or API server not running.

**Fix:**
```bash
# 1. Verify API is running
curl http://localhost:8080/health

# 2. Check CORS config in main.py (should allow localhost:3001)
# 3. Verify REACT_APP_API_URL is set correctly
REACT_APP_API_URL=http://localhost:8080 npm start
```

---

#### 8. `StarletteDeprecationWarning: Using httpx with starlette.testclient`

**Cause:** Version compatibility warning between starlette and httpx.

**Fix:** This is a non-blocking warning (tests still pass). To suppress:
```bash
pip install httpx2
```
Or ignore — the tests pass regardless.

---

#### 9. pytest collects 0 tests

**Cause:** Test discovery issue.

**Fix:**
```bash
# Verify pyproject.toml exists at project root
cat pyproject.toml

# Ensure pytest-asyncio is installed
pip install pytest-asyncio

# Run with explicit path
cd src/mcp-server
python -m pytest app/tests/test_api_endpoints.py app/tests/test_tools.py -v
```

---

#### 10. MCP tools don't appear in Claude Desktop

**Cause:** Claude Desktop config not saved or server not running.

**Fix:**
```bash
# 1. Verify server is running
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'

# 2. Check Claude Desktop config file location:
#    Windows: %APPDATA%\Claude\claude_desktop_config.json
#    macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json
#    Linux:   ~/.config/Claude/claude_desktop_config.json

# 3. Restart Claude Desktop after config changes
```

---

### Getting Help

If you encounter an issue not listed here:

1. Check the [GitHub Issues](https://github.com/jayzamindar/finops-mcp-sentinel/issues)
2. Review the server logs: `docker compose logs mcp-server`
3. Open a new issue with:
   - Your Python/Node version
   - The exact error message
   - Steps to reproduce

---

## Test Architecture

### Test File Organization

```
src/mcp-server/app/tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Shared fixtures (FastAPI TestClient)
├── test_api_endpoints.py    # 22 API integration tests
└── test_tools.py            # 14 tool unit tests
```

### Test Design Principles

1. **Deterministic:** All mock data uses seed=42, so tests produce identical results every run
2. **Isolated:** Each test creates its own state, no test depends on another
3. **Fast:** Full suite runs in < 1 second (no I/O, no network, no database)
4. **Comprehensive:** Every endpoint, every tool, every error path tested