# 09 - Testing Scenarios

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Testing Scenarios  
**Target Audience:** QA Engineers, Developers  
**Approx Tokens:** ~3,000

---

## 9.1 Unit Tests

Unit tests verify individual components of the MCP server.

### 9.1.1 Test Scenarios

| Test ID | Description | Expected Result |
|---------|-------------|------------------|
| `UT-001` | Authentication middleware validates API key | Valid key accepted, invalid rejected |
| `UT-002` | RBAC middleware enforces role-based permissions | Correct access based on role |
| `UT-003` | PII redaction masks sensitive data correctly | All sensitive data redacted |
| `UT-004` | Audit log entry creation | Log entry contains all required fields |
| `UT-005` | Tool execution success/failure handling | Correct output/result handling |

### 9.1.2 Test Implementation

```python
import pytest
from fastapi.testclient import TestClient
from mcp_server.main import app

client = TestClient(app)

def test_auth_middleware():
    # Test valid API key
    api_key = generate_valid_api_key()
    response = client.get("/api/v1/stream", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    
    # Test invalid API key
    invalid_key = "invalid_key"
    response = client.get("/api/v1/stream", headers={"X-API-Key": invalid_key})
    assert response.status_code == 401

def test_rbac_middleware():
    # Test role-based access control
    api_key = generate_api_key_for_role("sre")
    response = client.post("/api/v1/tools/diagnose_transaction_latency/execute", headers={"X-API-Key": api_key})
    assert response.status_code == 200
    
    api_key = generate_api_key_for_role("viewer")
    response = client.post("/api/v1/tools/diagnose_transaction_latency/execute", headers={"X-API-Key": api_key})
    assert response.status_code == 403  # Forbidden

def test_pii_redaction():
    # Test PII redaction
    input_text = "Card number: 4111-1111-1111-1111"
    redacted_text = redact_pii(input_text)
    assert "4111-XXXX-XXXX-1111" in redacted_text

def test_audit_log():
    # Test audit log entry creation
    log_entry = create_audit_log_entry("tool_execution", "user_xyz", "diagnose_transaction_latency")
    assert log_entry["event_type"] == "tool_execution"
    assert log_entry["actor"]["id"] == "user_xyz"
    assert log_entry["resource"]["id"] == "diagnose_transaction_latency"
```

## 9.2 Integration Tests

Integration tests verify the interaction between different components.

| Test ID | Description | Expected Result |
|---------|-------------|------------------|
| `IT-005` | Tool execution failure handling | Correct error handling and logging |
| `IT-006` | Approval workflow timeout | Escalation to senior SRE |
| `IT-007` | Audit log verification for tool execution | Log entry contains all required fields |


### 9.2.1 Test Scenarios

| Test ID | Description | Expected Result |
|---------|-------------|------------------|
| `IT-001` | End-to-end tool execution via SSE | Results streamed in < 2s |
| `IT-002` | Approval workflow completion | Status updated, notifications sent |
| `IT-003` | Audit log immutability | Checksum matches, no modifications |
| `IT-004` | Prometheus mock query | Returns expected latency data |

### 9.2.2 Test Implementation

```python
def test_tool_execution_sse():
    # Test end-to-end tool execution
    api_key = generate_valid_api_key()
    response = client.post("/api/v1/tools/diagnose_transaction_latency/execute", headers={"X-API-Key": api_key}, json={"service_name": "payment-gateway"})
    assert response.status_code == 200
    
    # Check SSE stream for results
    sse_response = client.get("/api/v1/stream?client_id=test_client&events=tool,approval,audit")
    assert sse_response.status_code == 200
    
    events = list(sse_response.iter_lines())
    assert len(events) > 0
    assert any("tool:result" in event.decode() for event in events)

def test_approval_workflow():
    # Test approval workflow
    api_key = generate_api_key_for_role("admin")
    response = client.post("/api/v1/tools/remediate_unhealthy_pod/execute", headers={"X-API-Key": api_key}, json={"pod_name": "test-pod", "reason": "test"})
    assert response.status_code == 200
    
    approval_id = response.json()["approval_id"]
    response = client.post(f"/api/v1/approvals/{approval_id}", headers={"X-API-Key": api_key}, json={"decision": "approve"})
    assert response.status_code == 200
    
    # Verify approval status updated
    response = client.get(f"/api/v1/approvals/pending", headers={"X-API-Key": api_key})
    assert response.json()["status"] == "approved"

def test_audit_log_immutability():
    # Test audit log immutability
    log_entry = create_audit_log_entry("test_event", "test_user", "test_resource")
    stored_checksum = log_entry["checksum"]
    
    # Attempt to tamper with log entry
    log_entry["outcome"]["status"] = "failure"
    tampered_checksum = calculate_checksum(log_entry)
    
    assert stored_checksum != tampered_checksum

def test_prometheus_mock_query():
    # Test Prometheus mock query
    response = client.post("/api/v1/tools/diagnose_transaction_latency/execute", headers={"X-API-Key": generate_valid_api_key()}, json={"service_name": "test-service"})
    assert response.status_code == 200
    
    # Verify results contain expected data
    sse_response = client.get("/api/v1/stream?client_id=test_client&events=tool:result")
    events = list(sse_response.iter_lines())
    result = json.loads(events[-1].decode().split("data: ")[1])
    assert "latency_p95_ms" in result
    assert "anomalies" in result
```

## 9.3 Security Tests

Security tests verify the security features of the system.

### 9.3.1 Test Scenarios

| Test ID | Description | Expected Result |
|---------|-------------|------------------|
| `ST-001` | Unauthorized tool execution | 403 Forbidden returned |
| `ST-002` | PII in tool output | All sensitive data redacted |
| `ST-003` | High-risk action without approval | Execution blocked |
| `ST-004` | Audit log tampering | Checksum mismatch detected |

### 9.3.2 Test Implementation

```python
def test_unauthorized_tool_execution():
    # Test unauthorized tool execution
    api_key = generate_api_key_for_role("viewer")
    response = client.post("/api/v1/tools/remediate_unhealthy_pod/execute", headers={"X-API-Key": api_key}, json={"pod_name": "test-pod"})
    assert response.status_code == 403  # Forbidden

def test_pii_in_tool_output():
    # Test PII in tool output
    input_data = {"service_name": "payment-gateway", "time_range": {"start": "2025-01-01T00:00:00Z", "end": "2025-01-01T01:00:00Z"}}
    response = client.post("/api/v1/tools/diagnose_transaction_latency/execute", headers={"X-API-Key": generate_valid_api_key()}, json=input_data)
    result = response.json()
    
    # Verify PII redaction
    for anomaly in result["anomalies"]:
        assert "4111-XXXX-XXXX-1111" in anomaly["trace_id"]  # Assuming trace_id might contain card numbers

def test_high_risk_action_without_approval():
    # Test high-risk action without approval
    api_key = generate_api_key_for_role("sre")
    response = client.post("/api/v1/tools/remediate_unhealthy_pod/execute", headers={"X-API-Key": api_key}, json={"pod_name": "critical-pod", "reason": "test", "risk_score": 10})
    assert response.status_code == 200
    
    approval_id = response.json()["approval_id"]
    response = client.get(f"/api/v1/approvals/pending", headers={"X-API-Key": api_key})
    assert response.json()["status"] == "pending"

def test_audit_log_tampering():
    # Test audit log tampering detection
    log_entry = create_audit_log_entry("test_event", "test_user", "test_resource")
    original_checksum = log_entry["checksum"]
    
    # Attempt to tamper
    log_entry["outcome"]["status"] = "failure"
    tampered_checksum = calculate_checksum(log_entry)
    
    assert original_checksum != tampered_checksum
    assert verify_audit_log_integrity(log_entry) is False
```

*This section defines the testing strategy for the system. For success metrics, proceed to Section 10.*