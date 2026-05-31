# 01 - Prompt Guidelines

**Document:** finops-sre-sentinel Prompts
**Section:** Prompt Guidelines
**Target Audience:** Code Generation AI (or human developers)

## 1.1 Purpose

This document defines prompt engineering guidelines for generating or modifying code in the **FinOps SRE Sentinel** project. The prompts in sections 02–04 describe actual implemented patterns that any code generation must follow.

## 1.2 Core Guidelines

1. **Match the actual implementation**: All generated code must follow the patterns established in `src/mcp-server/app/` and `src/ui/src/`. Do not introduce frameworks or libraries not in the current dependency tree.
2. **Follow the Architecture Document**: Reference `finops-sre-sentinel-architecture/` for system-level design decisions.
3. **Use the URD for requirements**: Reference `finops-sre-sentinel-urd-v3/` for functional and non-functional requirements.
4. **Anti-hallucination rules**: Every tool, class, and function referenced must exist in the codebase. Verify imports against `requirements.txt` and `package.json` before generating code.

## 1.3 Technology Stack (Verified)

| Layer | Technology | Version |
|-------|-----------|---------|
| **MCP Server** | Python + FastAPI + uvicorn | 3.11+ |
| **UI** | React (JavaScript, not TypeScript) | 18.x |
| **Security** | API Key auth (SHA-256), PII Redactor | Custom |
| **Communication** | REST + SSE (`/api/v1/stream/insights`) | — |
| **Containerization** | Docker + Docker Compose | — |
| **MCP Protocol** | JSON-RPC 2.0 over Streamable HTTP | — |

## 1.4 File Structure Reference

```
src/mcp-server/app/
├── main.py              # FastAPI app, routes, lifespan
├── tool_registry.py     # ToolRegistry class
├── tools/               # Individual tool implementations
│   ├── analyze_cloud_spend_anomaly.py
│   ├── diagnose_transaction_latency.py
│   ├── remediate_unhealthy_pod.py
│   └── verify_compliance_drift.py
└── security/
    └── __init__.py      # RBAC roles, API key auth, Redactor class

src/ui/src/
├── App.js               # Main React app
├── index.js             # React 18 createRoot entry
└── components/
    ├── DashboardMetrics.js
    ├── ToolRunner.js
    ├── RealTimeInsights.js
    └── ApprovalRequest.js
```

*For MCP server code generation prompts, proceed to Section 02.*