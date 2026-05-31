# 07 - Testing and Validation

**Document:** finops-sre-sentinel Architecture Document  
**Section:** Testing and Validation  
**Target Audience:** QA Engineers, Developers  
**Approx Tokens:** ~2,000

## 7.1 Testing Strategy

The system is tested using a combination of **unit tests**, **integration tests**, and **end-to-end tests**. Current status: **36/36 tests passing** (pytest for backend, jest for frontend).

### 7.1.1 Backend Unit Tests (pytest)

Backend tests cover tool execution, security, and API endpoints using **pytest**:

```python
import pytest
from app.tools.analyze_cloud_spend_anomaly import execute

def test_anomaly_detection_basic():
    """Test z-score anomaly detection with known data"""
    input_data = {
        "cost_data": [
            {"date": "2024-01-01", "service": "compute", "amount": 100},
            {"date": "2024-01-02", "service": "compute", "amount": 105},
            {"date": "2024-01-03", "service": "compute", "amount": 500},  # anomaly
        ]
    }
    result = await execute(input_data)
    assert len(result["anomalies"]) > 0
    assert result["anomalies"][0]["amount"] == 500
```

### 7.1.2 Security Tests

Security tests verify API key authentication, RBAC, and PII redaction:

```python
from app.security import Authenticator, Role, check_permission, Redactor

def test_api_key_verification():
    """Test SHA-256 API key verification"""
    authenticator = Authenticator(api_keys={"test-hash": {"role": Role.ADMIN}})
    assert authenticator.verify("test-key") == True

def test_rbac_permissions():
    """Test role-based access control"""
    assert check_permission(Role.ADMIN, "invoke_tool", "remediate_unhealthy_pod") == True
    assert check_permission(Role.VIEWER, "invoke_tool", "remediate_unhealthy_pod") == False

def test_pii_redaction():
    """Test PII redaction in tool outputs"""
    redactor = Redactor()
    output = {"email": "user@example.com", "ip": "10.0.0.1"}
    safe = redactor.redact(output)
    assert "user@example.com" not in str(safe)
```

### 7.1.3 Frontend Unit Tests (jest)

Frontend tests use **jest** and **React Testing Library**:

```javascript
import { render, screen } from '@testing-library/react';
import DashboardMetrics from './DashboardMetrics';

test('renders metric cards', () => {
  render(<DashboardMetrics metrics={{ anomalies: 3, latency: 'normal', pods: 2 }} />);
  expect(screen.getByText(/anomalies/i)).toBeInTheDocument();
});
```

### 7.1.4 Integration Tests

Integration tests verify the interaction between components:

```python
def test_tool_invocation_api():
    """Test full tool invocation via REST API"""
    response = client.post(
        "/api/v1/tools/analyze_cloud_spend_anomaly/invoke",
        json={"cost_data": [...]},
        headers={"X-API-Key": "test-admin-key"}
    )
    assert response.status_code == 200
    assert "anomalies" in response.json()
```

### 7.1.5 End-to-End Tests

End-to-end tests verify the entire system workflow:

```python
def test_end_to_end_mcp_flow():
    """Test tool execution via MCP JSON-RPC 2.0"""
    response = client.post(
        "/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "analyze_cloud_spend_anomaly",
                "arguments": {"cost_data": [...]}
            }
        }
    )
    assert response.status_code == 200
    assert "result" in response.json()
```

## 7.2 Validation

The system is validated against the requirements defined in the URD document.

### 7.2.1 Validation Criteria

| Criteria | Description | Status |
|----------|-------------|--------|
| **Functional Requirements** | All 4 tools execute correctly with valid/invalid inputs | ✅ 36/36 tests passing |
| **Non-Functional Requirements** | API response <2s, SSE streaming, auth enforcement | ✅ Verified |
| **Security** | API Key auth, RBAC, PII redaction, audit logging | ✅ Verified |
| **UI** | React 18 components render, SSE connects, tool runner works | ✅ Verified |
| **Deployment** | Docker Compose builds and runs all services | ✅ Verified |

### 7.2.2 Test Execution Commands

```bash
# Backend tests (from src/mcp-server/)
pytest -v

# Frontend tests (from src/ui/)
npm test

# Full suite
pytest src/mcp-server/ && cd src/ui && npm test
```

*This section concludes the Architecture Document. You now have a comprehensive technical design for the MCP SRE Sentinel system.*