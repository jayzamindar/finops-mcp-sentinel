# 16 - MCP Blueprint Reference

**Document:** finops-sre-sentinel URD v3.0  
**Section:** MCP Blueprint Reference  
**Target Audience:** Future MCP Project Developers  
**Approx Tokens:** ~3,000

---

## 16.1 Purpose of MCP Blueprint

The MCP blueprint serves as a **reusable template** for future MCP projects. It provides a structured framework for defining:

1. **MCP Architecture**: Core components and their interactions (FastAPI + JSON-RPC 2.0)
2. **Tool Definitions**: Standardized tool schemas and execution logic (plain Python modules with auto-discovery)
3. **Security Guardrails**: Role-based access control and data protection (API Key + SHA-256)
4. **Resource Governance**: Execution budgets and operational efficiency tracking

## 16.2 Using the MCP Blueprint

To use this blueprint for a new MCP project:

1. **Review the template**: Understand the core components and their interactions
2. **Customize the tool definitions**: Define new tools or modify existing ones based on project requirements
3. **Configure security guardrails**: Set up role-based access control and data protection
4. **Implement resource governance**: Track execution budgets and rate limits

## 16.3 Fill-in-the-Gaps Template

```markdown
# MCP Project Template

## Project Overview
- **Project Name**: [Insert project name]
- **Project Purpose**: [Insert project purpose]

## MCP Architecture
- **Transport Layer**: FastAPI (REST + SSE + MCP JSON-RPC 2.0)
- **Tool Registry**: ToolRegistry with auto-discovery from tools/ directory
- **Security Layer**: API Key auth (X-API-Key header), RBAC, PII Redaction

## Tool Definitions
- **Tool 1**: [module_name] - [description], input schema: {...}, output schema: {...}
- **Tool 2**: [module_name] - [description], input schema: {...}, output schema: {...}

## Security Guardrails
- **Authentication**: API Key with SHA-256 hashing
- **RBAC**: Role enums (admin, sre, viewer) with permission matrix
- **Data Protection**: PII Redactor class for sensitive data masking

## Resource Governance
- **Execution Budgets**: Per-tool hourly/daily limits
- **Rate Limiting**: Per-user and per-tool request throttling
- **Cost Tracking**: Zero external API cost (all algorithmic tools)
```

## 16.4 Architecture Patterns

### 16.4.1 Tool Registration Pattern

```python
# Each tool is a plain Python module in app/tools/
# ToolRegistry auto-discovers and registers them
class ToolRegistry:
    def register(self, tool_name: str, tool_module):
        """Register a tool by name and module reference."""
        self._tools[tool_name] = {
            "name": tool_name,
            "description": tool_module.description,
            "input_schema": tool_module.input_schema,
            "execute": tool_module.execute
        }
```

### 16.4.2 Security Pattern

```python
# API Key authentication with SHA-256 hashing
def verify_api_key(api_key: str) -> Optional[dict]:
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    return VALID_KEYS.get(key_hash)

# RBAC permission check
def check_permission(role: str, tool_name: str) -> bool:
    return PERMISSION_MATRIX.get(role, {}).get(tool_name, False)
```

### 16.4.3 SSE Streaming Pattern

```python
# Server-Sent Events for real-time insights
@app.get("/api/v1/stream/insights")
async def stream_insights(request: Request):
    async def event_generator():
        while True:
            data = await get_next_event()
            yield f"data: {json.dumps(data)}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```

## 16.5 PII Redaction Engine

Regex-based masking of PAN, SSN, email, phone using the `Redactor` class from `app/security/__init__.py`.

### 16.5.1 Redaction Rules

| Data Type | Pattern | Replacement | Example |
|-----------|---------|-------------|---------|
| Credit Card Number | `\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b` | `$1-XXXX-XXXX-$4` | `4111-XXXX-XXXX-1111` |
| Bank Account Number | `ACCT-\d{6,12}` | `ACCT-XXXXXXXX` | `ACCT-XXXXXXXX` |
| SSN | `\b\d{3}-\d{2}-\d{4}\b` | `XXX-XX-XXXX` | `XXX-XX-XXXX` |
| Email Address | `\b[\w\.-]+@[\w\.-]+\.\w+\b` | `u***@d***.com` | `u***@e***.com` |
| Phone Number | `\b\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b` | `+X-XXX-XXX-XXXX` | `+1-555-XXX-4567` |
| IP Address (Internal) | `\b(10\.\|172\.(1[6-9]\|2\d\|3[01])\|192\.168\.)\d{1,3}\.\d{1,3}\b` | `REDACTED_IP` | `REDACTED_IP` |

### 16.5.2 Redaction Flow

```
Input Text (may contain PII)
    │
    ▼
1. Scan text for PII patterns
2. Replace matches with masked values
3. Log redaction event (no PII stored)
4. Return sanitized text
    │
    ▼
Sanitized Output (no PII)
```

### 16.5.3 Redaction Testing

| Test ID | Input | Expected Output |
|---------|-------|-----------------|
| PII_001 | `Card: 4111-1111-1111-1111` | `Card: 4111-XXXX-XXXX-1111` |
| PII_002 | `Email: john.doe@company.com` | `Email: j***@c***.com` |
| PII_003 | `SSN: 123-45-6789` | `SSN: XXX-XX-6789` |
| PII_004 | `No sensitive data` | `No sensitive data` (unchanged) |

## 16.6 Audit Trail Requirements

### 16.6.1 What Gets Logged

| Event | Fields Logged | Immutable? |
|-------|---------------|------------|
| Tool Execution | tool_name, input, output (sanitized), user, role, timestamp | ✅ Yes |
| Approval | approval_id, decision, responder, timestamp | ✅ Yes |
| Authentication | user, role, ip, user_agent, timestamp | ✅ Yes |
| Configuration | changed_by, old_value, new_value | ✅ Yes |
| Errors | error_type, message, stack_trace (sanitized) | ✅ Yes |

### 16.6.2 Audit Log Integrity

- SHA-256 checksum chain across entries
- Verification tool provided

## 16.7 Compliance Matrix

| Standard | Requirements | Verification | Frequency |
|----------|--------------|--------------|-----------|
| **PCI-DSS** | Encryption, Access Control, Audit Trails | Automated tool + manual | Quarterly |
| **SOC 2** | Security, Availability, Confidentiality | Audit log export + review | Annual |
| **GDPR** | Data privacy, Right to explanation | PII redaction + audit trail | Continuous |

*This section provides a reusable MCP blueprint. For the appendix, proceed to Section 17.*