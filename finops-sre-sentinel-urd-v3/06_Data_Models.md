# 06 - Data Models

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Data Models  
**Target Audience:** Backend Developers, API Designers  
**Approx Tokens:** ~2,500

---

## 6.1 Core Entities

The MCP server manages several core entities that represent tool executions, approval requests, audit events, and incidents.

### 6.1.1 ToolExecution

**Purpose:** Records every invocation of an MCP tool for audit and analytics.

```json
{
  "id": "exec_a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "tool_name": "diagnose_transaction_latency",
  "invoker": {
    "user_id": "user_marcus_chen",
    "role": "senior_sre",
    "session_id": "sess_xyz789"
  },
  "input": {
    "time_range": {
      "start": "2026-04-27T10:00:00Z",
      "end": "2026-04-27T10:05:00Z"
    },
    "service_name": "payment-gateway",
    "threshold_ms": 500,
    "limit": 100
  },
  "output": {
    "total_traces": 1547,
    "slow_traces": 23,
    "latency_p95_ms": 234,
    "latency_p99_ms": 891,
    "anomalies": [
      {
        "trace_id": "txn_a1b2c3d4",
        "timestamp": "2026-04-27T10:02:15Z",
        "latency_ms": 2341,
        "service": "payment-gateway",
        "root_cause": "database_connection_pool_exhaustion",
        "recommendation": "Increase connection pool size or add read replica"
      }
    ],
    "reasoning_manifest": {
      "steps": [
        "Step 1: Query Prometheus for p99 latency metrics",
        "Step 2: Correlate with slow traces in ELK",
        "Step 3: Identify database connection pool as bottleneck"
      ],
      "confidence_score": 0.92
    }
  },
  "metadata": {
    "execution_time_ms": 1234,
    "cached": false,
    "retry_count": 0
  },
  "security": {
    "pii_redacted": true,
    "rbac_decision": "allowed",
    "risk_score": 2,
    "approval_status": "auto_approved"
  },
  "correlation_id": "corr_inc_2026_0427_001",
  "timestamp": "2026-04-27T10:05:00.123Z",
  "checksum": "sha256_abc123..."
}
```

### 6.1.2 ApprovalRequest

**Purpose:** Tracks human approval for high-risk actions.

```json
{
  "id": "apr_x1y2z3",
  "tool_execution_id": "exec_a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "requested_by": "ai_agent",
  "requested_action": {
    "tool": "remediate_unhealthy_pod",
    "parameters": {
      "namespace": "production",
      "pod_name": "payment-gateway-7d9f8b6c5",
      "action": "restart",
      "reason": "CrashLoopBackOff detected - OOM kill"
    }
  },
  "risk_assessment": {
    "score": 7,
    "impact": {
      "affected_requests": 1250,
      "downtime_seconds": 15,
      "data_integrity_risk": "none",
      "financial_impact_usd": 250
    },
    "safety_checks": {
      "replicas_healthy": true,
      "circuit_breaker_status": "closed",
      "draining_connections": true
    }
  },
  "status": "pending",
  "sla_timer_seconds": 300,
  "escalation_level": 0,
  "requested_at": "2026-04-27T10:02:00Z",
  "responded_by": null,
  "responded_at": null,
  "decision": null,
  "comments": null,
  "notification": {
    "channel": "slack",
    "sent_to": "@oncall-sre",
    "delivered": true
  }
}
```

**Approval Workflow Rules:**
- Risk Score 1-3: **Auto-execute** (no approval needed)
- Risk Score 4-6: **On-call SRE approval** (one-click in UI)
- Risk Score 7-9: **Senior SRE approval** (escalates after 5 min SLA)
- Risk Score 10: **Executive escalation** (blocks until manual override)

### 6.1.3 AuditEvent

**Purpose:** Immutable record of every system action for compliance.

```json
{
  "id": "audit_uuid_v4",
  "event_type": "tool_execution",
  "actor": {
    "id": "user_marcus_chen",
    "type": "human",
    "role": "senior_sre"
  },
  "resource": {
    "type": "tool",
    "id": "diagnose_transaction_latency",
    "action": "execute"
  },
  "context": {
    "correlation_id": "corr_inc_2026_0427_001",
    "session_id": "sess_xyz789",
    "ip_address": "127.0.0.1",
    "user_agent": "finops-sre-sentinel-ui/1.0"
  },
  "outcome": {
    "status": "success",
    "error_message": null,
    "execution_time_ms": 1234
  },
  "security": {
    "threat_detected": false,
    "input_sanitized": true,
    "pii_redacted": true
  },
  "timestamp": "2026-04-27T10:05:00.123Z",
  "previous_checksum": "sha256_prev_hash...",
  "checksum": "sha256_current_hash..."
}
```

### 6.1.4 Incident

**Purpose:** Represents a production incident from detection to resolution.

```json
{
  "id": "INC-2026-0001",
  "title": "Payment Gateway Latency Spike",
  "severity": "high",
  "status": "investigating",
  "triggered_by": "automated_anomaly_detection",
  "affected_services": ["payment-gateway", "transaction-processor"],
  "affected_users_estimate": 15000,
  "root_cause": null,
  "resolution": null,
  "timeline": [
    {
      "timestamp": "2026-04-27T10:00:00Z",
      "event": "Anomaly detected - p99 latency > 800ms"
    },
    {
      "timestamp": "2026-04-27T10:02:00Z",
      "event": "MCP tool dispatched for investigation"
    },
    {
      "timestamp": "2026-04-27T10:05:00Z",
      "event": "Root cause identified: DB connection pool exhaustion"
    }
  ],
  "related_tool_executions": ["exec_a1b2c3d4"],
  "related_approvals": [],
  "cost_attribution": {
    "estimated_downtime_cost_usd": 1250,
    "ai_token_cost_usd": 0,
    "total_incident_cost_usd": 1250
  },
  "created_at": "2026-04-27T10:00:00Z",
  "resolved_at": null
}
```

## 6.2 Enum Definitions

### 6.2.1 Tool Names

```python
class ToolName(str, Enum):
    DIAGNOSE_TRANSACTION_LATENCY = "diagnose_transaction_latency"
    ANALYZE_CLOUD_SPEND_ANOMALY = "analyze_cloud_spend_anomaly"
    REMEDIATE_UNHEALTHY_POD = "remediate_unhealthy_pod"
    VERIFY_COMPLIANCE_DRIFT = "verify_compliance_drift"
```

### 6.2.2 Event Types

```python
class EventType(str, Enum):
    TOOL_EXECUTION = "tool_execution"
    APPROVAL_REQUEST = "approval_request"
    APPROVAL_RESPONSE = "approval_response"
    USER_LOGIN = "user_login"
    CONFIG_CHANGE = "config_change"
    KILL_SWITCH = "kill_switch"
    ERROR = "error"
    SYSTEM_STARTUP = "system_startup"
    SYSTEM_SHUTDOWN = "system_shutdown"
```

### 6.2.3 Risk Scores

```python
class RiskLevel(IntEnum):
    AUTOMATIC = 1  # Auto-execute, no approval
    LOW = 2        # Auto-execute, logged
    MEDIUM = 4     # On-call SRE approval
    HIGH = 7       # Senior SRE approval
    CRITICAL = 10  # Executive escalation required
```

*These data models are the foundation for all API contracts and database schemas. Any changes must be reflected here first.*