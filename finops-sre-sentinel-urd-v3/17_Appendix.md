# 17 - Appendix

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Appendix  
**Target Audience:** All Stakeholders  
**Approx Tokens:** ~2,000

---

## 17.1 Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - Standard for AI integration with infrastructure |
| **SRE** | Site Reliability Engineering - Approach to IT operations focusing on reliability |
| **FinOps** | Financial Operations - Practices for cloud cost management and optimization |
| **HITL** | Human-in-the-Loop - Human oversight and approval for critical tool actions |
| **PII** | Personally Identifiable Information - Data that can identify individuals |
| **SSE** | Server-Sent Events - Protocol for real-time updates from server to client |
| **RBAC** | Role-Based Access Control - Fine-grained permissions based on user roles |
| **JSON-RPC** | JSON Remote Procedure Call - Lightweight RPC protocol used by MCP |
| **FastAPI** | Modern Python web framework used for the MCP server |
| **ToolRegistry** | Dynamic tool discovery and registration system in the MCP server |

## 17.2 Reference Documents

| Document | Location |
|----------|----------|
| MCP Server Implementation | `src/mcp-server/app/main.py` |
| Tool Registry | `src/mcp-server/app/tool_registry.py` |
| Tool Implementations | `src/mcp-server/app/tools/` |
| Security Module | `src/mcp-server/app/security/__init__.py` |
| React UI Source | `src/ui/src/` |
| Docker Configuration | `docker-compose.yml` |
| Testing Instructions | `TestingInstructions.md` |

## 17.3 Assumptions & Constraints

**Assumptions:**
1. Target environment is local Docker Desktop + Kubernetes
2. All 4 tools are algorithmic (z-score, percentile calculations, compliance rules) — no external LLM API calls required
3. Communication via REST + SSE + MCP JSON-RPC 2.0
4. Local hardware: Docker-capable machine with 8GB+ RAM

**Constraints:**
1. All tools are deterministic algorithms — zero external API cost
2. All data processing supports local deployment
3. No proprietary dependencies for core functionality

## 17.4 Future Work

| Area | Description | Priority |
|------|-------------|----------|
| **Multi-Cloud Support** | Extend to AWS/Azure in addition to local K8s | High |
| **Enhanced Visualization** | Improve dashboard with more real-time metrics | Medium |
| **Additional Tools** | Develop more MCP tools for common SRE tasks | Medium |
| **WebSocket Support** | Add bidirectional streaming alongside SSE | Low |

*This appendix provides supplementary information and references. It concludes the finops-sre-sentinel URD v3.0.*