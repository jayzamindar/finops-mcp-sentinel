# 04 - Security Layer Prompts

**Document:** finops-sre-sentinel Prompts  
**Section:** Security Layer Prompts  
**Target Audience:** Code Generation AI  
**Approx Tokens:** ~2,000

## 4.1 Security Layer

Generate code for the security layer, including:

1. **Authentication**: Implement JWT token authentication.
2. **Authorization**: Implement role-based access control (RBAC).
3. **PII Redaction**: Implement PII redaction for sensitive data.

### 4.1.1 Prompt

```python
# Generate security layer code
# Use JWT tokens for authentication
# Implement RBAC for authorization
# Include PII redaction for sensitive data

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str):
    # Authenticate user using credentials
    pass

def redact_pii(input_text: str) -> str:
    # Redact sensitive data (e.g., PAN, SSN, email)
    pass
```

## 4.2 Authentication

Generate code for JWT token authentication.

### 4.2.1 Prompt

```python
# Generate JWT token authentication code
# Use PyJWT library

import jwt

def generate_jwt_token(user: dict) -> str:
    # Generate JWT token for user
    pass

def verify_jwt_token(token: str) -> dict:
    # Verify JWT token
    pass
```

## 4.3 Authorization

Generate code for role-based access control (RBAC).

### 4.3.1 Prompt

```python
# Generate RBAC code
# Define roles and permissions

class Role(str, Enum):
    ADMIN = "admin"
    SRE = "sre"
    VIEWER = "viewer"

def authorize_user(user: dict, action: str) -> bool:
    # Authorize user using RBAC
    pass
```

*This section defines the prompts for generating security layer code. You now have a complete set of prompts for code generation.*