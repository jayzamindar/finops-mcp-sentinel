# 05 - Security Architecture

**Document:** finops-sre-sentinel Architecture Document  
**Section:** Security Architecture  
**Target Audience:** Security Team, Compliance Officers  
**Approx Tokens:** ~3,000

## 5.1 Security Measures

The system implements various security measures to protect sensitive data and ensure compliance.

### 5.1.1 Authentication

The system uses **API Key authentication with SHA-256 hashing** (NOT JWT). API keys are passed via the `X-API-Key` HTTP header.

```python
from app.security import Authenticator

# API keys are stored as SHA-256 hashes
authenticator = Authenticator(api_keys={
    "admin-key-hash": {"role": Role.ADMIN},
    "operator-key-hash": {"role": Role.OPERATOR},
    "viewer-key-hash": {"role": Role.VIEWER},
})

async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key via X-API-Key header"""
    if not authenticator.verify(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
```

### 5.1.2 Authorization

The system uses **role-based access control (RBAC)** with three roles:

| Role | Permissions |
|------|-------------|
| **ADMIN** | Full access: invoke all tools, manage keys, view audit logs |
| **OPERATOR** | Invoke tools (except destructive), view results |
| **VIEWER** | Read-only: view tool list, read results |

```python
from app.security import Role, check_permission

# Tool-level permission checks
check_permission(Role.ADMIN, "invoke_tool", "remediate_unhealthy_pod")  # True
check_permission(Role.VIEWER, "invoke_tool", "remediate_unhealthy_pod")  # False
check_permission(Role.OPERATOR, "invoke_tool", "analyze_cloud_spend_anomaly")  # True
```

### 5.1.3 PII Redaction

The **Redactor** class automatically masks sensitive data in tool outputs before returning to clients:

```python
from app.security import Redactor

redactor = Redactor()
safe_output = redactor.redact(tool_output)
# Masks: email addresses, IP addresses, account IDs, credit card numbers
```

## 5.2 Compliance

The system is designed to comply with multiple regulatory standards.

| Standard | Requirements Covered | Verification Method | Frequency |
|----------|---------------------|-------------------|-----------|
| **PCI-DSS** | Encryption, Access Control, Audit Trails | Automated tool + manual | Quarterly |
| **SOC 2** | Security, Availability, Confidentiality | Audit log export + review | Annual |
| **GDPR** | Data privacy, Right to explanation | PII redaction | Continuous |

## 5.3 Audit Trails

The system maintains **immutable audit logs** for all tool executions with the `AuditEvent` data model.

```python
from app.security import create_audit_event

audit_event = create_audit_event(
    event_type="tool_invocation",
    user="operator-1",
    resource="remediate_unhealthy_pod",
    details={"pod_name": "payment-service-abc123", "action": "restart"}
)
# Stored with SHA-256 checksum for integrity verification
```

### 5.3.1 Audit Event Schema

| Field | Type | Description |
|-------|------|-------------|
| `event_type` | string | Type of event (tool_invocation, auth_failure, approval_request) |
| `user` | string | API key identifier (hashed) |
| `resource` | string | Tool or resource accessed |
| `details` | object | Action-specific details |
| `timestamp` | ISO 8601 | When the event occurred |
| `checksum` | string | SHA-256 hash for integrity verification |

## 5.4 Security Flow

```
Client Request
    │
    ▼
┌─────────────────────────────────┐
│  1. Extract X-API-Key header     │
│  2. Hash key with SHA-256        │
│  3. Look up key in store         │
│  4. Verify role permissions      │
│  5. Execute tool                 │
│  6. Redact PII from output       │
│  7. Create audit log entry       │
│  8. Return sanitized response    │
└─────────────────────────────────┘
```

*This section defines the security architecture of the system. For scalability and performance details, proceed to Section 06.*