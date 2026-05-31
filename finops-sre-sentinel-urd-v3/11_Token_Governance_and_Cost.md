# 11 - Resource Governance & Cost Analysis

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Resource Governance & Cost Analysis  
**Target Audience:** FinOps Team, Engineering Managers, CTO  
**Approx Tokens:** ~3,000

---

## 11.1 Why Resource Governance Matters

Unconstrained SRE automation can quickly become expensive. Without governance:
- A single runaway remediation loop could trigger **dozens of unnecessary pod restarts**
- Unbounded tool executions could overwhelm backing services (Prometheus, Kubernetes)
- Repeated failed executions multiply compute and operational costs

**For this project:** The MCP server uses **algorithmic tools** (z-score anomaly detection, P50-P99 latency classification, compliance rule engines) — **no external AI model API calls**. Resource governance focuses on **execution budgets, API rate limits, and operational efficiency**, not LLM token costs.

## 11.2 Deployment Cost Analysis

### 11.2.1 Infrastructure Costs

| Component | Hosting | Monthly Cost | Notes |
|-----------|---------|-------------|-------|
| **MCP Server (FastAPI)** | Self-hosted / Docker | **$0** | No external API fees |
| **React UI** | Static files served by MCP server | **$0** | Bundled with backend |
| **Prometheus** | Self-hosted / Docker | **$0** | Open-source monitoring |
| **Grafana** | Self-hosted / Docker | **$0** | Open-source dashboards |
| **Container Orchestration** | Docker Compose (local) / K8s (prod) | **$0–varies** | Depends on hosting |

**Total Monthly Cost (local dev): $0.00** — All tools are self-contained Python modules with no external API dependencies.

### 11.2.2 Cost Comparison with AI-Model-Based Alternatives

| Approach | Monthly Cost | Trade-off |
|----------|-------------|-----------|
| **FinOps SRE Sentinel (algorithmic)** | **$0** | Deterministic, explainable, no hallucination risk |
| LLM-based SRE assistant (GPT-4o) | $50–500+ | Flexible but non-deterministic, hallucination risk |
| LLM-based SRE assistant (Claude 3.5 Sonnet) | $100–1000+ | High quality but expensive at scale |
| Commercial AIOps platform | $5000+/month | Full-featured but enterprise pricing |

## 11.3 Execution Budget & Rate Limiting

### 11.3.1 What Gets Tracked

| Metric | Description | Granularity |
|--------|-------------|-------------|
| Tool executions | Total number of tool invocations | Per tool, per hour |
| Execution duration | Time taken for each tool execution (ms) | Per execution |
| API request count | Number of API requests to backing services | Per backing service |
| Failed executions | Tool executions that returned errors | Per tool, per hour |
| Approval requests | HITL approvals triggered | Per tool, per day |
| Concurrent executions | Simultaneous tool executions in progress | Real-time |

### 11.3.2 Execution Waste Categories & Prevention

| Waste Category | Description | Prevention Strategy |
|---------------|-------------|---------------------|
| **Retry Waste** | Tool retries failed backing service calls | Exponential backoff, max 2 retries |
| **Loop Waste** | Tool enters repetitive execution pattern | Max execution time limit (30s per tool) |
| **Over-Query Waste** | Tool queries more data than needed | Result limit parameters, pagination |
| **Redundant Execution** | Same tool called with identical inputs | Result caching with configurable TTL |
| **Polling Waste** | Client polling for approval status | Use SSE push instead of polling |

## 11.4 Hard Budget Caps & Throttling

### 11.4.1 Budget Configuration

```yaml
execution_budget:
  hourly_limit: 1000           # Max tool executions per hour
  daily_limit: 10000           # Max tool executions per day
  warning_threshold: 0.80      # Warn at 80% consumption
  critical_threshold: 0.95     # Critical alert at 95%
  auto_throttle: true          # Auto-throttle when budget is low
  
  per_tool_limits:
    diagnose_transaction_latency: 250
    analyze_cloud_spend_anomaly: 250
    remediate_unhealthy_pod: 150
    verify_compliance_drift: 200
    buffer: 150                # Reserve for critical operations
    
  throttle_actions:
    - threshold: 0.80
      action: "notify_admin"
    - threshold: 0.90
      action: "reduce_concurrency"
    - threshold: 0.95
      action: "read_only_mode"
    - threshold: 1.00
      action: "block_all_non_essential"
```

### 11.4.2 Throttling Behavior

| Budget Level | System Behavior |
|-------------|-----------------|
| **< 80%** | Normal operation — all tools available |
| **80-90%** | Notification sent to admin, reduce concurrent executions to 50% |
| **90-95%** | Read-only mode — only diagnostic tools, no remediation |
| **95-100%** | Critical alerts, only basic tools allowed |
| **> 100%** | All non-essential tools blocked, emergency admin override required |

### 11.4.3 Rate Limiting Configuration

```yaml
rate_limiting:
  enabled: true
  global:
    requests_per_minute: 60
    requests_per_hour: 1000
  per_user:
    requests_per_minute: 20
    requests_per_hour: 200
  per_tool:
    remediate_unhealthy_pod:
      requests_per_hour: 50      # Stricter limit for destructive actions
    diagnose_transaction_latency:
      requests_per_hour: 200
```

## 11.5 Result Caching

Frequent read-only queries are cached to **reduce backing service load**:

| Cache Rule | TTL | Example Query |
|------------|-----|---------------|
| Cluster health | 30 seconds | `GET /health` |
| Compliance drift results | 5 minutes | `verify_compliance_drift` with same standard |
| Cost anomalies | 15 minutes | `analyze_cloud_spend_anomaly` with same provider |
| Latency metrics | 1 minute | `diagnose_transaction_latency` with same service |

**Cache Hit Ratio Target:** > 40% of all read-only queries should be cache hits.

## 11.6 Efficiency Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tool execution success rate | > 99% | (successful executions / total executions) × 100 |
| Average execution time | < 2 seconds | Mean of p50, p95, p99 latencies |
| Cache hit ratio | > 40% | (cache hits / total read queries) × 100 |
| Approval turnaround time | < 5 minutes | Mean time from approval request to resolution |
| Retry rate | < 5% | (retried executions / total executions) × 100 |
| Wasted execution rate | < 2% | (failed + redundant / total executions) × 100 |

*Resource governance demonstrates operational discipline and financial responsibility. All tools in this project are self-contained Python modules with zero external API costs.*