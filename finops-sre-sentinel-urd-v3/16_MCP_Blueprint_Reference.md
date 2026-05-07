# 16 - MCP Blueprint Reference

**Document:** finops-sre-sentinel URD v3.0  
**Section:** MCP Blueprint Reference  
**Target Audience:** Future MCP Project Developers  
**Approx Tokens:** ~3,000

---

## 16.1 Purpose of MCP Blueprint

The MCP blueprint serves as a **reusable template** for future MCP projects. It provides a structured framework for defining:

1. **MCP Architecture**: Core components and their interactions
2. **Tool Definitions**: Standardized tool schemas and execution logic
3. **Security Guardrails**: Role-based access control and data protection
4. **Token Governance**: Cost tracking and optimization strategies

## 16.2 Using the MCP Blueprint

To use this blueprint for a new MCP project:

1. **Review the template**: Understand the core components and their interactions
2. **Customize the tool definitions**: Define new tools or modify existing ones based on project requirements
3. **Configure security guardrails**: Set up role-based access control and data protection
4. **Implement token governance**: Track and optimize token usage

### Unified SOC Operations Wireframe

1. **Global Health Dashboard**
	* MTTR Trend Chart
	* Alert Volume Gauge
	* Compliance Scorecard
2. **Active Incidents Grid**
	* Incident Severity Filter (High/Medium/Low)
	* Incident Timeline View
	* Quick Actions (e.g., approve/reject remediation)
3. **Drill-Down Views**
	* Entity Timelines (User, Host, IP)
	* Cross-resource queries (e.g., KQL)

### Fill-in-the-Gaps Template

```markdown
# MCP Project Template

## Project Overview
- **Project Name**: [Insert project name]
- **Project Purpose**: [Insert project purpose]

## MCP Architecture
- **Transport Layer**: [STDIO/SSE/REST]
- **Tool Registry**: [List tools and their purposes]
- **Security Layer**: [Describe security measures]

## Tool Definitions
- **Tool 1**: [Describe tool 1 and its schema]
- **Tool 2**: [Describe tool 2 and its schema]

## Security Guardrails
- **RBAC**: [Describe role-based access control]
- **Data Protection**: [Describe data protection measures]

## Token Governance
- **Cost Tracking**: [Describe cost tracking strategy]

### 16.2.1 Fill-in-the-Gaps Template

The blueprint includes a fill-in-the-gaps template for defining new MCP projects.

```markdown
# MCP Project Template

## Project Overview
- **Project Name**: [Insert project name]
- **Project Purpose**: [Insert project purpose]

## MCP Architecture
- **Transport Layer**: [STDIO/SSE/REST]
- **Tool Registry**: [List tools and their purposes]
- **Security Layer**: [Describe security measures]

## Tool Definitions
- **Tool 1**: [Describe tool 1 and its schema]
- **Tool 2**: [Describe tool 2 and its schema]

## Security Guardrails
- **RBAC**: [Describe role-based access control]
- **Data Protection**: [Describe data protection measures]

## Token Governance
- **Cost Tracking**: [Describe cost tracking strategy and audit log verification
- **PII Redaction Engine**: Regex-based masking of PAN, SSN, email, phone
- **Data Encryption**: Environment variables and secrets stored securely

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
| **GDPR** | Data privacy, Right to explanation | PII redaction + XAI | Continuous |

*This section provides a reusable MCP blueprint. For the appendix, proceed to Section 17.*