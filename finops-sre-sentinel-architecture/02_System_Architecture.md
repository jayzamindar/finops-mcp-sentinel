# 02 - System Architecture

**Document:** finops-sre-sentinel Architecture Document  
**Section:** System Architecture  
**Target Audience:** Technical Stakeholders, Developers  
**Approx Tokens:** ~2,500

## 2.1 High-Level Architecture

The MCP SRE Sentinel system is designed as a modular, scalable architecture to support the complex needs of fintech organizations.

### 2.1.1 Component Interactions

The system consists of several key components that interact with each other to provide a comprehensive SRE solution.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MCP SRE SENTINEL                            │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   MCP      │  │   Security   │  │   UI Layer   │  │   Tools    │  │
│  │  Server    │  │   Layer      │  │              │  │            │  │
│  └─────┬──────┘  └─────┬────────┘  └──────┬───────┘  └─────┬──────┘  │
│        │               │                  │               │         │
│        ▼               ▼                  ▼               ▼         │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  FastAPI   │  │  API Key   │  │  React 18    │  │  Tool      │  │
│  │  + uvicorn │  │  + SHA-256 │  │  JavaScript  │  │  Registry  │  │
│  └────────────┘  └────────────┘  └──────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1.2 Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **MCP Server** | Handles MCP JSON-RPC 2.0 requests, REST API, SSE streaming |
| **Security Layer** | API Key authentication (SHA-256), RBAC, PII redaction |
| **UI Layer** | React 18 dashboard with real-time insights, tool runner, approvals |
| **Tools** | 4 algorithmic tools: anomaly detection, latency diagnosis, pod remediation, compliance audit |

## 2.2 Technical Implementation

The system is built using a combination of technologies to ensure scalability, security, and performance.

### 2.2.1 Backend Technology Stack

- **Python 3.11+**: For the MCP server and tool execution
- **FastAPI + uvicorn**: For building the REST API and SSE streaming endpoints
- **uv**: For package management
- **ToolRegistry**: Dynamic tool discovery via `tool_registry.py`

### 2.2.2 Frontend Technology Stack

- **React 18 (JavaScript)**: For building the UI components (NOT TypeScript)
- **createRoot API**: Modern React 18 rendering
- **Material-UI**: For consistent design
- **Fetch API**: For REST calls and SSE connections

## 2.3 Data Flow

The system processes data from various sources, including logs, metrics, and cloud cost data.

### 2.3.1 Data Sources

| Data Source | Description |
|-------------|-------------|
| **Metrics** | Collected from Prometheus (latency, pod health, resource usage) |
| **Cloud Cost Data** | Collected from cloud provider APIs (spend, billing) |
| **Compliance Data** | Collected from cloud provider compliance APIs |

### 2.3.2 Data Processing

The system processes data using algorithmic tools:
- **Spend anomaly detection**: Z-score statistical analysis on daily cost data
- **Latency diagnosis**: P50/P90/P95/P99 percentile classification
- **Pod remediation**: Health status checks with safe restart and rollback
- **Compliance auditing**: Rule-based checks against compliance frameworks

*This section defines the high-level architecture of the system. For component design details, proceed to Section 03.*