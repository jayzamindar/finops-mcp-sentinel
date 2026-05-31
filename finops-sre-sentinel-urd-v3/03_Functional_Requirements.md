# 03 - Functional Requirements

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Functional Requirements  
**Target Audience:** Developers, Product Owners  
**Approx Tokens:** ~3,000

## 3.1 Tool Capabilities

The MCP server exposes four core tools for SRE operations. Each tool has a specific purpose and strict input/output schema.

### 3.1.1 diagnose_transaction_latency

**Purpose:** Query payment/transaction logs to identify latency patterns and root causes.

**Input Schema:**
```json
{
  "time_range": {
    "start": "2025-01-10T00:00:00Z",
    "end": "2025-01-10T12:00:00Z"
  },
  "service_name": "payment-gateway",
  "threshold_ms": 500,
  "limit": 100
}
```

**Output Schema:**
```json
{
  "total_traces": 1547,
  "slow_traces": 23,
  "latency_p95_ms": 234,
  "latency_p99_ms": 891,
  "anomalies": [
    {
      "trace_id": "txn_a1b2c3d4",
      "timestamp": "2025-01-10T08:15:22Z",
      "latency_ms": 2341,
      "service": "payment-gateway",
      "root_cause": "database_connection_pool_exhaustion",
      "recommendation": "Increase connection pool size or add read replica"
    }
  ]
}
```

**User Flow:**
1. AI receives alert about transaction latency
2. Executes `diagnose_transaction_latency` tool
3. Analyzes slow traces for patterns
4. Presents findings to on-call engineer
5. Proposes remediation if root cause identified

### 3.1.2 analyze_cloud_spend_anomaly

**Purpose:** Detect and analyze unexpected cloud cost spikes.

**Input Schema:**
```json
{
  "time_range": {
    "start": "2025-01-01T00:00:00Z",
    "end": "2025-01-10T00:00:00Z"
  },
  "namespace": "production",
  "cost_threshold_percent": 20,
  "include_forecasts": true
}
```

**Output Schema:**
```json
{
  "baseline_monthly_cost_usd": 45000,
  "current_monthly_cost_usd": 67800,
  "anomaly_detected": true,
  "anomaly_percent": 50.7,
  "top_charges": [
    {
      "resource": "eks-production-nodegroup",
      "change_percent": 45,
      "likely_cause": "node_count_increase",
      "correlated_incidents": ["INC-2025-0112"]
    }
  ],
  "forecast_month_end_usd": 82000,
  "recommendations": [
    {
      "action": "rightsize_nodes",
      "estimated_savings_usd": 12000,
      "risk_level": "low"
    }
  ]
}
```

### 3.1.3 remediate_unhealthy_pod

**Purpose:** Safely restart unhealthy Kubernetes pods with approval gates.

**Input Schema:**
```json
{
  "namespace": "production",
  "pod_name": "payment-gateway-7d9f8b6c5",
  "reason": "CrashLoopBackOff detected",
  "risk_score": 7,
  "dry_run": true
}
```

**Output Schema:**
```json
{
  "action": "restart_pod",
  "risk_score": 7,
  "approval_required": true,
  "approval_status": "pending",
  "impact_assessment": {
    "affected_requests": 1250,
    "duration_seconds": 15,
    "service_impact": "minimal"
  },
  "safety_checks": {
    "replicas_healthy": true,
    "circuit_breaker_status": "closed",
    "draining_connections": true
  },
  "human_approver": "oncall-sre@company.com"
}
```

**Approval Workflow:**
- Risk Score 1-3: Auto-execute (no approval needed)
- Risk Score 4-6: On-call engineer approval (one-click)
- Risk Score 7-9: Senior SRE + manager approval
- Risk Score 10: Executive escalation required

### 3.1.4 verify_compliance_drift

**Purpose:** Check cloud resources against PCI-DSS security standards.

**Input Schema:**
```json
{
  "standard": "pci-dss-v4",
  "scope": ["eks", "rds", "s3"],
  "include_remediation": true
}
```

**Output Schema:**
```json
{
  "compliance_score": 87,
  "total_checks": 142,
  "passed": 124,
  "failed": 18,
  "critical_findings": [
    {
      "resource": "s3-prod-logs bucket",
      "rule": "s3-bucket-encryption",
      "status": "non_compliant",
      "severity": "critical",
      "remediation_steps": [
        "Enable S3 default encryption",
        "Enforce SSL for bucket access"
      ]
    }
  ],
  "last_audit_date": "2025-01-05T00:00:00Z"
}
```

## 3.2 Data Flow Architecture

The MCP server integrates with multiple data sources to provide comprehensive insights.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                 │
│   ┌─────────────────┐    ┌─────────────────┐    ┌───────────────┐  │
│   │ Claude Desktop  │    │ Cursor IDE      │    │ MCP Inspector │  │
│   │ (AI Agent)      │    │ (Developer)     │    │ (Testing)     │  │
│   └────────┬────────┘    └────────┬────────┘    └───────┬───────┘  │
└────────────┼───────────────────────┼─────────────────────┼──────────┘
             │ SSE/WebSocket         │                    │
             ▼                       ▼                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      MCP GATEWAY LAYER                              │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  Security Gateway (PII Redaction + RBAC + Auth)              │   │
│   │  ├── API Key Validation (X-API-Key header, SHA-256)           │   │
│   │  ├── Role-Based Access Control (RBAC)                         │   │
│   │  ├── PII Redaction Engine (account IDs, card numbers)         │   │
│   │  └── Rate Limiting                                            │   │
│   └─────────────────────────────────────────────────────────────┘   │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  SSE Event Streaming                                         │   │
│   │  ├── Real-time log streaming to client                       │   │
│   │  ├── Tool execution progress                                  │   │
│   │  └── Approval request push notifications                     │   │
│   └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TOOL ENGINE LAYER                              │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │  Tool Registry                                                │  │
│   │  ├── diagnose_transaction_latency (Prometheus/ES query)      │  │
│   │  ├── analyze_cloud_spend_anomaly (AWS Cost Explorer)         │  │
│   │  ├── remediate_unhealthy_pod (Kubernetes API)                │  │
│   │  └── verify_compliance_drift (AWS Config/Prowler)             │  │
│   └──────────────────────────────────────────────────────────────┘  │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │  Risk Scoring Engine                                          │  │
│   │  ├── Calculate risk score per action                          │  │
│   │  ├── Determine approval requirements                          │  │
│   │  └── Block high-risk actions without approval                │  │
│   └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    APPROVAL QUEUE LAYER                             │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │  Human-in-the-Loop (HITL) Queue                               │  │
│   │  ├── Pending approvals dashboard                              │  │
│   │  ├── Email/Slack notifications                                │  │
│   │  ├── SLA timers (escalation after X minutes)                  │  │
│   │  └── Audit logging of all approval decisions                  │  │
│   └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────┬────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   BACKING SERVICES LAYER                            │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐   │
│   │ Mock Prometheus │  │ Mock AWS/FinOps│  │ Mock Kubernetes    │   │
│   │ (Metrics)       │  │ (Cost APIs)    │  │ (Pod Management)    │   │
│   └────────────────┘  └────────────────┘  └────────────────────┘   │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐   │
│   │ Mock Elasticsearch│ │ Mock AWS Config│  │ Notification Svc   │   │
│   │ (Logs/Traces)   │  │ (Compliance)   │  │ (Email/Slack)      │   │
│   └────────────────┘  └────────────────┘  └────────────────────┘   │
└────────────────────────────────────┬────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY LAYER                              │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │ OpenTelemetry Collector                                     │  │
│   │  ├── Traces (tool execution paths)                           │  │
│   │  ├── Metrics (tool latency, success rates)                    │  │
│   │  └── Logs (structured JSON with correlation IDs)             │  │
│   └──────────────────────────────────────────────────────────────┘  │
│            │                    │                    │              │
│            ▼                    ▼                    ▼              │
│   ┌────────────────┐  ┌────────────────┐  ┌────────────────────┐     │
│   │ Prometheus     │  │ Loki/ES        │  │ Grafana            │     │
│   │ (Metrics DB)   │  │ (Log Storage)  │  │ (Dashboards)       │     │
│   └────────────────┘  └────────────────┘  └────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

*This section defines the core functional capabilities of the system. For non-functional requirements, proceed to Section 04.*