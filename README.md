# 🛡️ FinOps-SRE Sentinel

**AI-powered SRE command center for fintech infrastructure — built on the Model Context Protocol (MCP), with production-grade architecture scaled down for a personal lab environment.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18-61dafb.svg)
![Docker](https://img.shields.io/badge/docker-ready-2496ed.svg)
![MCP](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)
![Tests](https://img.shields.io/badge/tests-36%2F36%20passing-brightgreen.svg)

---

## 📌 What This Project Demonstrates

> **Built in 3 weeks as a solo project** — designed with production-grade architecture principles, then deliberately scoped down to run entirely on a personal laptop with zero cloud credentials required.

This project showcases **full-stack SRE platform engineering** using the cutting-edge **Model Context Protocol (MCP)** — the standard that connects AI assistants like Claude, Cursor, and custom agents to real infrastructure tooling. It solves a critical gap: **how do you give AI assistants safe, auditable access to production infrastructure operations?**

### Skills Demonstrated for Senior SRE / Platform Engineer Roles

| Skill Area | What It Shows |
|------------|---------------|
| **MCP Protocol Implementation** | JSON-RPC 2.0 server, tool registration, schema validation — working with Anthropic's latest AI infrastructure protocol |
| **API Design** | RESTful endpoints + MCP JSON-RPC + SSE streaming — three protocol patterns in one server |
| **Production Safety** | Human-in-the-loop approval flow with risk scoring for destructive operations |
| **Test Engineering** | 36 automated tests (22 API + 14 unit), deterministic mock data with seeded RNG |
| **Infrastructure as Code** | Docker Compose with health checks, multi-stage builds, observability |
| **Security Architecture** | Compliance frameworks (PCI-DSS, SOC2, GDPR), audit trails, CORS, rate limiting |
| **Frontend Engineering** | React dashboard with real-time SSE, dark theme, responsive layout |
| **System Design** | Clean layer separation (gateway → tool engine → backing services), extensible tool registry |
| **AI Reliability** | Anti-hallucination framework with `{{MISSING_DATA}}` sentinel patterns |

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      AI Client Layer                             │
│  ┌────────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ Claude Desktop  │  │  Cursor IDE  │  │  Dashboard UI     │   │
│  └───────┬────────┘  └──────┬───────┘  └─────────┬─────────┘   │
│          │                  │                     │              │
│          │   MCP Protocol   │          REST/SSE   │              │
│          ▼                  ▼                     ▼              │
├─────────────────────────────────────────────────────────────────┤
│                   MCP Server (FastAPI)                           │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │               FastAPI Application                         │  │
│  │  ┌─────────────┐ ┌────────────┐ ┌─────────────────────┐  │  │
│  │  │ MCP JSON-RPC │ │ REST APIs  │ │    SSE Stream       │  │  │
│  │  │   /mcp       │ │ /api/v1/*  │ │ /api/v1/stream      │  │  │
│  │  └──────┬──────┘ └──────┬─────┘ └──────────┬──────────┘  │  │
│  │         │               │                   │              │  │
│  │         ▼               ▼                   ▼              │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │            Tool Auto-Discovery Registry               │ │  │
│  │  │  (pkgutil scan → register → expose via MCP + REST)    │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │  ┌──────────────────────────────────────────────────────┐ │  │
│  │  │            Mock Data Engine (seed=42)                 │ │  │
│  │  │  ┌───────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │ │  │
│  │  │  │Cloud Spend│ │ Latency  │ │   Pod    │ │Compli- │ │ │  │
│  │  │  │  Anomaly  │ │Diagnosis │ │Remediate │ │ance    │ │ │  │
│  │  │  └───────────┘ └──────────┘ └──────────┘ └────────┘ │ │  │
│  │  └──────────────────────────────────────────────────────┘ │  │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐ │  │
│  │  │ Risk Scoring   │  │Approval Queue │  │  Audit Trail  │ │  │
│  │  └───────────────┘  └───────────────┘  └───────────────┘ │  │
│  └───────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│              Backing Services (Docker Compose)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   PostgreSQL  │  │    Redis     │  │   Observability      │  │
│  │  (audit DB)   │  │  (cache/RT)  │  │  (metrics/traces)    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/jayzamindar/finops-mcp-sentinel.git
cd finops-mcp-sentinel
docker compose up --build
```

Two containers start:

| Service | URL | Description |
|---------|-----|-------------|
| **MCP Server** | `http://localhost:8080` | FastAPI backend with mock data engine |
| **Dashboard UI** | `http://localhost:3001` | React dashboard (proxies API via nginx) |

### Option 2: Local Development

**Backend (MCP Server):**
```bash
cd src/mcp-server
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

**Frontend (Dashboard UI):**
```bash
cd src/ui
npm install
REACT_APP_API_URL=http://localhost:8080 npm start
```

### Option 3: Connect from Claude Desktop

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "finops-sre-sentinel": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

---

## 🛠️ MCP Tools

The server exposes **4 production SRE tools** via the MCP protocol. Each tool is self-contained with its own schema, validation, mock data, and audit logging.

### 1. `analyze_cloud_spend_anomaly` — Cloud Cost Intelligence

Detects cost anomalies across cloud services with YTD analysis and forecasts.

**Input Schema:**
```json
{
  "namespace": "production",
  "cost_threshold_percent": 20,
  "include_forecasts": true
}
```

**Output:**
- Baseline vs. current monthly cost (USD)
- Per-service cost breakdown with delta percentages
- Anomaly detection with severity classification
- Month-end forecasts with confidence intervals
- Actionable cost optimization recommendations

**Real-world use case:** A FinOps engineer asks Claude — *"Why did our AWS bill spike 40% this month?"* — and gets a detailed breakdown identifying that EC2 costs increased due to untagged staging instances.

---

### 2. `diagnose_transaction_latency` — Transaction Performance Root Cause Analysis

Identifies root causes of transaction latency spikes in financial services.

**Input Schema:**
```json
{
  "service_name": "payment-gateway",
  "threshold_ms": 500,
  "limit": 50
}
```

**Output:**
- P50/P95/P99 latency percentile metrics
- Slow trace details with trace IDs, timestamps, and root causes
- Root cause breakdown (DB connection pool exhaustion, external API timeouts, etc.)
- Per-cause remediation recommendations

**Real-world use case:** An SRE asks Claude — *"Why are payment transactions slow this morning?"* — and gets trace-level analysis showing DB connection pool exhaustion as the root cause with a recommendation to increase pool size.

---

### 3. `remediate_unhealthy_pod` — Kubernetes Pod Health Management

Identifies unhealthy Kubernetes pods and proposes remediation actions with risk-based approval flow.

**Input Schema:**
```json
{
  "namespace": "production",
  "auto_approve": false,
  "max_risk_score": 50
}
```

**Output:**
- Inventory of unhealthy pods with restart counts and status durations
- Proposed remediation actions (restart, scale, rollback, drain)
- Risk scores for each action (1-100 scale)
- Pending approval requests for high-risk operations

**Real-world use case:** An SRE asks Claude — *"Which pods are unhealthy in production?"* — and gets a prioritized list with risk-scored remediation actions. High-risk actions (like rolling back a deployment) are queued for human approval.

---

### 4. `verify_compliance_drift` — Compliance & Security Posture

Checks infrastructure compliance against PCI-DSS, SOC2, and GDPR frameworks.

**Input Schema:**
```json
{
  "frameworks": ["PCI-DSS", "SOC2", "GDPR"],
  "include_passing": true
}
```

**Output:**
- Framework-by-framework compliance scores (0-100)
- Individual control pass/fail status with evidence
- Top compliance risks prioritized by severity
- Remediation guidance for each failed control

**Real-world use case:** A compliance engineer asks Claude — *"What's our PCI-DSS compliance status?"* — and gets a detailed report showing 94% compliance with specific failures in encryption-at-rest configuration.

---

## 🖥️ Dashboard UI

The React dashboard provides four operational views:

<!-- Screenshot placeholders — add images to docs/screenshots/ -->
| Tab | Description | Screenshot |
|-----|-------------|------------|
| **Overview** | KPI metrics, recent events, pending approvals at a glance | `![Overview](docs/screenshots/overview.png)` |
| **Live Stream** | Real-time SSE event feed with severity filtering | `![Live Stream](docs/screenshots/live-stream.png)` |
| **Approvals** | Human-in-the-loop approval queue with approve/reject actions | `![Approvals](docs/screenshots/approvals.png)` |
| **Tool Runner** | Execute MCP tools manually with custom JSON parameters | `![Tool Runner](docs/screenshots/tool-runner.png)` |

---

## 📡 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root welcome message |
| `/health` | GET | Health check with system status |
| `/ready` | GET | Readiness probe (dependency checks) |
| `/mcp` | POST | MCP JSON-RPC 2.0 endpoint (initialize, tools/list, tools/call) |
| `/api/v1/tools` | GET | List available MCP tools with schemas |
| `/api/v1/tools/{name}/execute` | POST | Execute a specific tool with parameters |
| `/api/v1/approvals/pending` | GET | List pending approval requests |
| `/api/v1/approvals/{id}` | POST | Approve or reject a request |
| `/api/v1/dashboard/summary` | GET | Dashboard metrics summary |
| `/api/v1/audit/trail` | GET | Audit trail of all actions |
| `/api/v1/stream` | GET | SSE real-time event stream |

---

## 🧪 Testing

**36 automated tests** covering API endpoints, MCP protocol, tool execution, and deterministic behavior.

```bash
cd src/mcp-server
python -m pytest app/tests/ -v
```

**Expected output:**
```
36 passed, 1 warning in 0.25s
```

For detailed testing instructions, troubleshooting, and manual test procedures, see **[TestingInstructions.md](TestingInstructions.md)**.

---

## 📁 Project Structure

```
finops-sre-sentinel/
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── CLAUDE.md                       # AI assistant context file
├── docker-compose.yml              # One-command full stack startup
├── pyproject.toml                  # Python project config (pytest, tools)
├── README.md                       # This file
├── TestingInstructions.md          # Detailed testing guide
│
├── .github/
│   └── workflows/                  # CI/CD pipeline (lint, test, build)
│
├── src/
│   ├── mcp-server/                 # Backend — FastAPI + MCP Protocol
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── app/
│   │       ├── main.py             # FastAPI app + all routes + MCP handler
│   │       ├── tool_registry.py    # Auto-discovery tool registry (pkgutil)
│   │       ├── security/           # Rate limiting, CORS, auth middleware
│   │       ├── tools/              # MCP tool implementations
│   │       │   ├── analyze_cloud_spend_anomaly.py
│   │       │   ├── diagnose_transaction_latency.py
│   │       │   ├── remediate_unhealthy_pod.py
│   │       │   └── verify_compliance_drift.py
│   │       └── tests/              # Test suite (36 tests)
│   │           ├── conftest.py
│   │           ├── test_api_endpoints.py
│   │           └── test_tools.py
│   │
│   └── ui/                         # Frontend — React Dashboard
│       ├── Dockerfile
│       ├── package.json
│       └── src/
│           ├── App.js              # Main layout with tab navigation
│           ├── App.css             # Production dark-theme styles
│           └── components/
│               ├── DashboardMetrics.js  # KPI cards grid
│               ├── RealTimeInsights.js  # SSE event stream viewer
│               ├── ApprovalRequest.js   # Approval queue with actions
│               └── ToolRunner.js        # Manual tool execution UI
│
└── docs/                           # Architecture & design documentation
    ├── finops-sre-sentinel-architecture/   # 7 architecture documents
    ├── finops-sre-sentinel-prompts/        # 4 prompt engineering guides
    └── finops-sre-sentinel-urd-v3/         # 17-section requirements document
```

---

## 🔧 Tech Stack & Design Decisions

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | Python 3.11+ / FastAPI | Async-native, Pydantic validation, OpenAPI auto-docs |
| **MCP Protocol** | JSON-RPC 2.0 | Anthropic's standard for AI-to-tool communication |
| **Frontend** | React 18 | Component-based UI, strong ecosystem |
| **Styling** | CSS (dark theme) | No build dependencies, fast iteration |
| **Containerization** | Docker / Docker Compose | Consistent dev/prod parity |
| **Testing** | pytest + httpx | Async test support, FastAPI integration |
| **Logging** | structlog | Structured JSON logging for production observability |
| **CI/CD** | GitHub Actions | Lint → type-check → test → build pipeline |

---

## 🏭 Production Deployment Path

This project is **designed for production architecture but scoped for personal lab use**. Here's the path from mock to real:

### Current State (Mock Mode)
- Seed-based deterministic data (seed=42) — identical results every run
- No external dependencies — works offline, no cloud credentials needed
- Full API surface — every endpoint, every schema, every response format

### Production Migration

```python
# Each tool in app/tools/ has a clear swap point:
# 
# Mock:   result = generate_mock_spend_data(namespace, threshold)
# Real:   result = await aws_cost_explorer.get_cost_anomaly_detection(
#             Filter={"Dimensions": {"Key": "SERVICE", "Values": ["Amazon EC2"]}},
#             DateInterval={"StartDate": start, "EndDate": end}
#         )
```

**Target cloud: AWS** (primary), with cloud-agnostic tool interfaces that can be adapted to GCP or Azure.

### Production Infrastructure Additions
- Replace mock data with AWS SDK calls (Cost Explorer, X-Ray, EKS, Config)
- Add PostgreSQL for persistent audit trail
- Add Redis for real-time event streaming and caching
- Add Prometheus + Grafana for observability
- Add mTLS for service-to-service authentication
- Add Kubernetes deployment manifests

---

## 📊 Project Scorecard

Engineering quality self-assessment:

| Area | Score | Detail |
|------|-------|--------|
| **Documentation** | 9/10 | 7 architecture sections, 17 URD sections, 4 prompt sections — exceptional planning depth |
| **Architecture Design** | 8/10 | Clean separation of concerns, proper layering (gateway → tool engine → backing services) |
| **Port Discipline** | 10/10 | Port 3001/8080 enforced everywhere, OpenClaw reservation respected |
| **Anti-Hallucination Framework** | 9/10 | `{{MISSING_DATA_FROM_DOC_SECTION_XX}}` convention is a best-practice for AI-generated code |
| **Docker Orchestration** | 8/10 | docker-compose.yml with health checks, dependency ordering, observability profile |
| **CI/CD Pipeline** | 7/10 | GitHub Actions with lint, type-check, test, and Docker build stages |
| **Tool Auto-Discovery** | 8/10 | ToolRegistry with pkgutil auto-discovery is elegant and extensible |

---

## 🔐 Security Architecture

- **Human-in-the-Loop Approval:** Operations with risk score ≥ 50 require explicit human approval before execution
- **Audit Trail:** Every tool execution and approval decision logged with timestamps, user attribution, and full request/response payloads
- **CORS:** Configurable allowed origins (locked to UI origin in production)
- **Rate Limiting:** 60 requests/minute per IP (configurable)
- **Compliance Frameworks:** Built-in checks against PCI-DSS, SOC2, and GDPR
- **No Secrets in Code:** All credentials via environment variables

---

## 👤 About

**Built by [Jay Zamin](https://www.linkedin.com/in/jayzamindar/)** — Senior SRE / Platform Engineer with AI infrastructure expertise.

- **GitHub:** [github.com/jayzamindar](https://github.com/jayzamindar/)
- **LinkedIn:** [linkedin.com/in/jayzamindar](https://www.linkedin.com/in/jayzamindar/)
- **Development Timeline:** 3 weeks (solo project)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Built on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) specification by Anthropic. Designed for integration with Claude Desktop, Cursor, and the broader MCP ecosystem.