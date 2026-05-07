# 04 - Non-Functional Requirements

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Non-Functional Requirements  
**Target Audience:** Architects, DevOps Engineers, QA  
**Approx Tokens:** ~2,500

## 4.1 Performance Requirements

| Metric | Target | Measurement Method | Priority |
|--------|--------|-------------------|----------|
| Tool Execution Latency (p95) | < 2 seconds | OpenTelemetry spans across tool execution | High |
| Tool Execution Latency (p99) | < 5 seconds | OpenTelemetry spans | Medium |
| SSE Connection Setup | < 500ms | Client-side timing from connect to first event | High |
| Concurrent Tool Executions | 50+ parallel | Load test with simulated agents | Medium |
| Log Streaming Latency | < 100ms | End-to-end timestamp diff from source to client | High |
| UI Page Load Time | < 2 seconds | Browser DevTools network tab | Medium |
| API Response Time (p95) | < 500ms | FastAPI middleware timing | High |
| Token Usage Calculation | < 50ms | Inline calculation before/after each tool call | Medium |

### 4.1.1 Performance Testing Requirements

- All performance tests must use **mock data** to ensure consistency
- Tests must be run on the target hardware (16GB RAM, AMD Ryzen AI 7, Docker Desktop)
- Results must be documented in `test_results/` directory
- Any degradation >20% from baseline must be flagged as a failure

## 4.2 Availability & Reliability Requirements

| Metric | Target | Notes |
|--------|--------|-------|
| System Uptime | 99.95% | Excluding planned maintenance (local environment) |
| Tool Success Rate | > 99.9% | Excluding user-aborted executions |
| MTTR (System Self-Recovery) | < 30 minutes | For critical failures of the MCP server itself |
| Data Durability | 99.999999999% | Audit logs - immutable and checksum-verified |
| Graceful Degradation | Required | If AI model unreachable, revert to cached/mock responses |
| Kill Switch Response Time | < 5 seconds | From activation to all connections terminated |

## 4.3 Scalability Requirements

| Requirement | Target | Notes |
|-------------|--------|-------|
| Concurrent AI Agent Connections | 100+ | Via SSE channels |
| Tool Executions Per Hour | 10,000+ | For production scenario |
| Log Ingestion Rate | 1M+ lines/second | When connected to real log sources |
| Concurrent Approval Requests | 50+ pending | In the HITL queue |

## 4.4 Security Requirements

| Requirement | Implementation | Verification Method |
|-------------|---------------|-------------------|
| Authentication | JWT tokens with RS256 signing | Unit tests for token validation |
| Authorization | RBAC with role-based permission checks | Integration tests for all roles |
| PII Redaction | Regex-based masking of PAN, SSN, email, phone | Unit tests with known patterns |
| Audit Trail | Immutable log with SHA-256 checksums | Verification tests for tamper detection |
| Secrets Management | Environment variables via .env file | Manual review of .env.example |
| Transport Security | TLS 1.3 for any non-local connections | N/A for local-only deployment |
| Input Validation | JSON Schema validation on all tool inputs | Schema validation tests |
| Rate Limiting | Per-user, per-tool rate limits | Load tests |

## 4.5 Maintainability Requirements

| Requirement | Standard | Notes |
|-------------|----------|-------|
| Code Documentation | Docstrings for all functions | Google-style Python docstrings |
| API Documentation | Auto-generated OpenAPI/Swagger | FastAPI built-in |
| Logging | Structured JSON logging | Using Python logging module |
| Configuration | YAML files with .env overrides | config.yaml.example provided |
| Testing | pytest with minimum 80% coverage | Measured via coverage.py |
| Containerization | Dockerfile with multi-stage builds | Distroless for production |

## 4.6 Compatibility Requirements

| Component | Required Version | Notes |
|-----------|-----------------|-------|
| Python | 3.11+ | 3.11.0 minimum |
| Node.js | 18+ | For React UI build |
| Docker | 24+ | Docker Desktop on Windows |
| Ollama | Latest stable | For local model inference |
| VS Code | Latest | With Continue.dev plugin |
| Browser | Chrome 100+, Firefox 100+, Edge 100+ | For React UI |

## 4.7 Local Environment Constraints

| Constraint | Value | Impact |
|-----------|-------|--------|
| RAM | 16 GB | Limits local model size to 7B-13B parameters |
| CPU | AMD Ryzen AI 7 | Adequate for CPU inference of small models |
| GPU | AMD Radeon (Integrated) | Not suitable for large model inference |
| Storage | Assumed > 50GB free | For Docker images, models, and project files |
| Network | Internet required | For NVIDIA NIM API calls |

## 4.8 Observability Requirements

| Component | Tool | Purpose |
|-----------|------|---------|
| Application Metrics | Prometheus (via FastAPI instrumentation) | Tool latency, success rates, token usage |
| Logging | Structured JSON to stdout + file | Debugging, audit trails |
| Distributed Tracing | OpenTelemetry SDK | End-to-end tool execution tracking |
| AI Model Observability | Custom middleware logging | Token counts, response times, hallucination checks |
| UI Performance | Browser DevTools / Lighthouse | Load times, bundle size |
| Token Tracking | Custom dashboard (UI) | Real-time burn rate, wasted token analysis |

*This section defines the non-negotiable quality attributes of the system. All development decisions must respect these constraints.*