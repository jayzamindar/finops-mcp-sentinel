# 04 - Data Flow

**Document:** finops-sre-sentinel Architecture Document  
**Section:** Data Flow  
**Target Audience:** Technical Stakeholders, Developers  
**Approx Tokens:** ~2,500

## 4.1 Data Sources

The system collects data from Kubernetes and cloud provider APIs:

1. **Kubernetes API**: Pod status, resource usage, restart counts
2. **Prometheus Metrics**: Transaction latency (P50/P90/P95/P99), pod health metrics
3. **Cloud Provider APIs**: Daily spend data, billing records, compliance status

## 4.2 Request Flow

### 4.2.1 REST API Flow

```
Client (Browser/CLI)
    │
    ▼
┌─────────────────────────────────────────────────┐
│  FastAPI Server (main.py)                       │
│                                                  │
│  1. X-API-Key header → Authenticator.verify()   │
│  2. RBAC check → check_permission()             │
│  3. ToolRegistry.get_tool(tool_name)             │
│  4. tool.execute(input_data)                     │
│  5. Redactor.redact(output) → PII masked         │
│  6. JSON response to client                      │
└─────────────────────────────────────────────────┘
```

### 4.2.2 SSE Streaming Flow

```
Client (React UI)
    │
    ▼  GET /api/v1/stream/insights
┌─────────────────────────────────────────────────┐
│  SSE Endpoint                                    │
│                                                  │
│  1. Authenticate via X-API-Key                   │
│  2. Open SSE connection                          │
│  3. Stream periodic insights:                    │
│     - Anomaly alerts from spend analysis         │
│     - Latency threshold breaches                 │
│     - Pod health status changes                  │
│     - Compliance drift findings                  │
│  4. Client receives real-time updates            │
└─────────────────────────────────────────────────┘
```

### 4.2.3 MCP JSON-RPC 2.0 Flow

```
MCP Client (e.g., Claude Desktop, Cursor)
    │
    ▼  POST /mcp
┌─────────────────────────────────────────────────┐
│  MCP JSON-RPC 2.0 Handler                       │
│                                                  │
│  1. Parse JSON-RPC 2.0 request                   │
│  2. Route by method:                             │
│     - tools/list → return tool schemas           │
│     - tools/call → execute tool via registry     │
│  3. Return JSON-RPC 2.0 response                 │
└─────────────────────────────────────────────────┘
```

## 4.3 Tool Data Processing

Each tool processes data using deterministic algorithms:

### 4.3.1 Cloud Spend Anomaly Detection

```
Input: Daily cost records (date, service, amount)
    │
    ▼
┌──────────────────────────────┐
│  Z-score statistical analysis │
│  threshold = 2.0              │
│  confidence = 0.95            │
└──────────────────────────────┘
    │
    ▼
Output: { anomalies: [...], summary: { ... } }
```

### 4.3.2 Transaction Latency Diagnosis

```
Input: Transaction latency data (ms)
    │
    ▼
┌──────────────────────────────┐
│  Percentile calculations      │
│  P50, P90, P95, P99           │
│  Classification thresholds    │
└──────────────────────────────┘
    │
    ▼
Output: { percentiles: {...}, classification: "normal|degraded|critical" }
```

### 4.3.3 Pod Remediation Flow

```
Input: Pod health data from Kubernetes API
    │
    ▼
┌──────────────────────────────┐
│  Health status evaluation     │
│  Risk scoring                 │
│  Human approval gate          │
│  Safe restart with rollback   │
└──────────────────────────────┘
    │
    ▼
Output: { action_taken: "restart|rollback|none", details: {...} }
```

### 4.3.4 Compliance Drift Check

```
Input: Cloud compliance data (configs, policies)
    │
    ▼
┌──────────────────────────────┐
│  Rule-based compliance checks │
│  Framework: SOC2, HIPAA, etc. │
│  Drift classification         │
└──────────────────────────────┘
    │
    ▼
Output: { compliant: true/false, findings: [...], recommendations: [...] }
```

## 4.4 Data Storage

The system operates primarily in memory with optional external storage:

1. **In-Memory**: Tool execution results, session data, SSE connections
2. **Prometheus**: Historical metrics for latency and pod health queries
3. **Kubernetes API**: Live pod status and resource data
4. **Cloud Provider APIs**: Spend data, compliance status

*This section defines how data flows through the system. For security architecture details, proceed to Section 05.*