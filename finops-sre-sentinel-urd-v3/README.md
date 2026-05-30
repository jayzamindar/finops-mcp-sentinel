# FinOps SRE Sentinel - User Requirements Document (URD)

**Version:** 3.0  
**Status:** ✅ Implemented — all 4 MCP tools, dashboard UI, test suite (36/36), Docker orchestration  
**Target Infrastructure:** Local Docker Desktop (mock mode) → AWS (production path)  
**Tech Stack:** Python (FastAPI) + React (JavaScript)  
**Repository:** [github.com/jayzamindar/finops-mcp-sentinel](https://github.com/jayzamindar/finops-mcp-sentinel)  

## Document Structure

This URD uses a **modular structure**. Each file is self-contained for easy AI ingestion.

```
finops-sre-sentinel/
├── README.md                                 ← You are here
├── 01_Executive_Summary.md                   ← Project overview, problem, value prop
├── 02_End_Users_and_Stakeholders.md          ← Personas, roles, pain points
├── 03_Functional_Requirements.md             ← 4 core MCP tools + data flows
├── 04_Non_Functional_Requirements.md        ← Performance, availability, scalability
├── 05_Security_and_Compliance.md             ← RBAC, PII redaction, audit trails
├── 06_Data_Models.md                         ← Core entities: ToolExecution, ApprovalRequest, AuditEvent, Incident
├── 07_API_Contracts.md                       ← MCP endpoints, SSE streaming, error codes
├── 08_Deployment_Architecture.md            ← Docker, K8s, Hybrid mock/real
├── 09_Testing_Scenarios.md                   ← Automated + Manual tests with Pass/Fail
├── 10_Success_Metrics.md                     ← KPIs, baselines, targets
├── 11_Token_Governance_and_Cost.md           ← Token tracking, wasted token analysis, real-world cost
├── 12_Anti_Hallucination_Framework.md        ← Strict no-hallucination rules
├── 13_UI_Architecture.md                     ← FastAPI + React SPA
├── 14_Local_Environment_Setup.md             ← PowerShell setup + uninstall
├── 15_Connection_Documentation.md            ← MCP client connection guide
├── 16_MCP_Blueprint_Reference.md             ← Reusable template for future MCP projects
├── 17_Appendix.md                            ← Glossary, references, assumptions
```

### Quick Navigation

| Section | Content | Best For |
|---------|---------|----------|
| `01` | Executive Summary | CTOs, Executives |
| `02` | End Users & Stakeholders | Product Owners |
| `03` | Functional Requirements | Developers |
| `04` | Non-Functional Requirements | Architects |
| `05` | Security & Compliance | Compliance Officers |
| `06` | Data Models | Backend Developers |
| `07` | API Contracts | Integration Engineers |
| `08` | Deployment Architecture | DevOps |
| `09` | Testing Scenarios | QA Engineers |
| `10` | Success Metrics | Stakeholders |
| `11` | Token Governance & Cost | FinOps Team |
| `12` | Anti-Hallucination Framework | AI Safety Team |
| `13` | UI Architecture | Frontend Developers |
| `14` | Local Environment Setup | New Contributors |
| `15` | Connection Documentation | End Users |
| `16` | MCP Blueprint Reference | Future Projects |
| `17` | Appendix | Reference |


---

## How to Use This Document Later
When creating the Architecture Document, reference sections:
- `01_Executive_Summary.md`
- `08_Deployment_Architecture.md`
- `05_Security_and_Compliance.md`
- `13_UI_Architecture.md`

When generating code prompts, reference sections:
- `03_Functional_Requirements.md`
- `06_Data_Models.md`
- `07_API_Contracts.md`

### To Generate Architecture Document
Feed the AI these sections in order:
1. `01_Executive_Summary.md` (context)
2. `08_Deployment_Architecture.md` (infrastructure)
3. `05_Security_and_Compliance.md` (guardrails)
4. `13_UI_Architecture.md` (frontend)

### To Generate Code Prompts
Feed the AI these sections per component:
- **MCP Server Core**: `03` + `06` + `07`
- **Security Layer**: `05` + `12`
- **UI Dashboard**: `13`
- **Testing Suite**: `09`

### AI Context Limit Safety
Each section is **under 3,000 tokens**. You can feed any section to any model (including NVIDIA free models) without hitting context limits.

---

*This document is the single source of truth for the finops-sre-sentinel project. All technical decisions must trace back to requirements defined herein.*