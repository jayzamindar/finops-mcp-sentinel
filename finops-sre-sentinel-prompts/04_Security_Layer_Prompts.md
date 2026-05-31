# 04 - Security Layer Prompts

**Document:** finops-sre-sentinel Prompts
**Section:** Security Layer Prompts
**Target Audience:** Code Generation AI (or human developers)

## 4.1 Security Architecture Overview

The security layer is implemented in `src/mcp-server/app/security/__init__.py`. It uses **API Key authentication** (not JWT), **role-based access control**, and **PII redaction**.

### Key Corrections from Previous Version
- ❌ Was: JWT token authentication with `OAuth2PasswordBearer` and PyJWT
- ✅ Now: API Key authentication with SHA-256 hash verification
- ❌ Was: Separate authentication and authorization functions
- ✅ Now: `verify_api_key()` FastAPI dependency that returns the key for downstream RBAC checks
- ❌ Was: Placeholder `redact_pii()` function
- ✅ Now: Full `Redactor` class with PAN, SSN, email, IP, and phone regex patterns

## 4.2 API Key Authentication

### 4.2.1 Prompt

```python
# Generate API key authentication code
# Key patterns:
#   - API keys stored as SHA-256 hashes (never plaintext)
#   - verify_api_key() is a FastAPI Depends() that extracts X-API-Key header
#   - Returns the raw key on success, raises 401 on failure
#   - DEFAULT_API_KEY_SHA256 env var provides the expected hash

import hashlib
import os
from fastapi import Header, HTTPException

DEFAULT_API_KEY_SHA256 = os.getenv("DEFAULT_API_KEY_SHA256", "")

async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """FastAPI dependency: validates X-API-Key header against SHA-256 hash."""
    if not DEFAULT_API_KEY_SHA256:
        raise HTTPException(status_code=500, detail="Server misconfiguration")
    hashed = hashlib.sha256(x_api_key.encode()).hexdigest()
    if hashed != DEFAULT_API_KEY_SHA256:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
```

## 4.3 RBAC (Role-Based Access Control)

### 4.3.1 Prompt

```python
# Generate RBAC code
# Key patterns:
#   - Role enum: ADMIN, SRE, VIEWER
#   - Permission enum: VIEW_METRICS, RUN_TOOLS, MANAGE_APPROVALS, MANAGE_SYSTEM
#   - ROLE_PERMISSIONS dict maps roles to sets of permissions
#   - Tools can check permissions before executing

from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    SRE = "sre"
    VIEWER = "viewer"

class Permission(str, Enum):
    VIEW_METRICS = "view_metrics"
    RUN_TOOLS = "run_tools"
    MANAGE_APPROVALS = "manage_approvals"
    MANAGE_SYSTEM = "manage_system"

ROLE_PERMISSIONS = {
    Role.ADMIN: {Permission.VIEW_METRICS, Permission.RUN_TOOLS,
                 Permission.MANAGE_APPROVALS, Permission.MANAGE_SYSTEM},
    Role.SRE: {Permission.VIEW_METRICS, Permission.RUN_TOOLS,
               Permission.MANAGE_APPROVALS},
    Role.VIEWER: {Permission.VIEW_METRICS},
}
```

## 4.4 PII Redaction (Redactor Class)

### 4.4.1 Prompt

```python
# Generate PII redaction code
# Key patterns:
#   - Redactor class with compiled regex patterns for: PAN, SSN, email, IP, phone
#   - redact(text) method applies all patterns and returns sanitized text
#   - redact_text() is a module-level convenience function that creates a Redactor instance
#   - Used in tool output processing to prevent PII leakage

import re

class Redactor:
    """Redacts PII from text using compiled regex patterns."""

    PAN_PATTERN = re.compile(r'\b(?:\d[ -]*?){13,19}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    IP_PATTERN = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')
    PHONE_PATTERN = re.compile(r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')

    def redact(self, text: str) -> str:
        text = self.PAN_PATTERN.sub('[REDACTED_PAN]', text)
        text = self.SSN_PATTERN.sub('[REDACTED_SSN]', text)
        text = self.EMAIL_PATTERN.sub('[REDACTED_EMAIL]', text)
        text = self.IP_PATTERN.sub('[REDACTED_IP]', text)
        text = self.PHONE_PATTERN.sub('[REDACTED_PHONE]', text)
        return text

_redactor = Redactor()

def redact_text(text: str) -> str:
    """Module-level convenience function for PII redaction."""
    return _redactor.redact(text)
```

*This completes the prompt engineering documentation for finops-sre-sentinel. All 4 prompt files now match the actual codebase implementation.*