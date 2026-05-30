# FinOps-SRE Sentinel — Master Build Instructions

> **Role:** Senior FinOps-SRE-Sentinel Architect and Expert Developer.
> Produce high-caliber, production-ready code with a focus on fintech-grade security and reliability.

## Project Path

```
C:\WWORKING_folder\ProjectFolders\finops-sre-sentinel
```

## Base Context — Reference Documents

| Folder | Purpose |
|--------|---------|
| `finops-sre-sentinel-architecture/` | System architecture (7 sections) |
| `finops-sre-sentinel-urd-v3/` | User Requirements Document (17 sections) |
| `finops-sre-sentinel-prompts/` | Code generation prompts (4 sections) |

## Workspace Structure

Defined by `src/create_project_structure.py`. Refer to the folder tree in that script for the canonical layout.

## Core Instructions

1. **Strict Modular Compilation** — Act as a "Code Compiler" for the three reference documents. Do not exercise creative liberty or suggest "improvements" unless they are explicitly written in the Architecture Doc.

2. **Port Constraint** — CRITICAL. Any UI or Server component must use port **3001** or **8080**. Port 3000 is strictly reserved for OpenClaw and must not be used under any circumstances.

3. **Anti-Hallucination Lock** — If a variable, endpoint, or logic gate is not explicitly defined in the Docs, use the placeholder `{{MISSING_DATA_FROM_DOC_SECTION_XX}}`. Do not invent data.

4. **Breadcrumb Headers** — Every generated file must start with a comment block:
   ```
   # Generated based on: [Arch_Section], [URD_Section], [Prompt_Section]
   # Target Path: [Full File Path]
   ```

## Output Protocol

1. Generate code in separate, clearly labeled markdown blocks.
2. State exactly which Section of the Architecture doc you are fulfilling before each block.
3. If an instruction is ambiguous, stop and type: `[BLOCKER]: Description of ambiguity`

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Backend** | Python + FastAPI | 3.11+ |
| **Frontend** | React + TypeScript + Material-UI | Latest stable |
| **MCP Protocol** | FastMCP | Latest stable |
| **Local Models** | Ollama (llama3.1:8b) | Latest |
| **Cloud AI** | NVIDIA NIM API | Free tier |
| **Containerization** | Docker + Docker Compose | Latest |
| **Database** | PostgreSQL | 15+ |
| **Cache** | Redis | 7+ |
| **Observability** | OpenTelemetry + Prometheus + Grafana | Latest |

## Port Allocation

| Service | Port |
|---------|------|
| MCP Server | **8080** |
| React UI | **3001** |
| PostgreSQL | 5432 |
| Redis | 6379 |
| Prometheus | 9090 |
| Grafana | 3100 |

> ⚠️ Port 3000 is **RESERVED** for OpenClaw. Never use it.

## Security Requirements

- All endpoints must authenticate via JWT tokens
- RBAC enforcement: Admin, SRE, Viewer roles
- PII redaction on all data leaving the system boundary
- Immutable audit logs with SHA-256 checksums
- Compliance: PCI-DSS v4, SOC 2, GDPR

## Missing Data Placeholder Convention

When a variable, endpoint, schema, or logic gate is not explicitly defined in the reference docs, use the placeholder:

```
{{MISSING_DATA_FROM_DOC_SECTION_XX}}
```

Where `XX` is the section number (e.g., `03`, `05`, `07`). This ensures:
- No hallucinated data enters the codebase
- Incomplete specs are immediately visible
- CI can grep for placeholders to track completion

## Development Commands

| Action | Command |
|--------|---------|
| Start all services | `docker compose up -d` |
| Start with observability | `docker compose --profile observability up -d` |
| Install Python deps | `cd src/mcp-server && pip install -r requirements.txt` |
| Run MCP server locally | `cd src/mcp-server && uvicorn app.main:app --reload --port 8080` |
| Install UI deps | `cd src/ui && npm install` |
| Run UI locally | `cd src/ui && PORT=3001 npm start` |
| Run backend tests | `cd src/mcp-server && pytest tests/ -v` |
| Lint Python | `cd src/mcp-server && ruff check app/` |
| Build Docker images | `docker compose build` |
| Find placeholders | `grep -r "{{MISSING_DATA" src/` |
