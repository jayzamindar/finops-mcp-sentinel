# 03 - Component Design

**Document:** finops-sre-sentinel Architecture Document  
**Section:** Component Design  
**Target Audience:** Developers, Technical Stakeholders  
**Approx Tokens:** ~3,000

## 3.1 MCP Server Component

The MCP server is the core component of the system, responsible for handling MCP protocol requests and executing tools.

### 3.1.1 MCP Server Architecture

The MCP server is built using **FastAPI** and **Python 3.11+**.

```python
from fastapi import FastAPI
from fastmcp import MCPServer

app = FastAPI()
mcp_server = MCPServer(app)
```

### 3.1.2 Tool Execution

The MCP server executes tools using a **tool registry**.

```python
from tool_registry import ToolRegistry

tool_registry = ToolRegistry()

@app.post("/api/v1/tools/{tool_name}/execute")
async def execute_tool(tool_name: str, input_data: dict):
    tool = tool_registry.get_tool(tool_name)
    if tool:
        return await tool.execute(input_data)
    else:
        return {"error": "Tool not found"}
```

## 3.2 Security Layer Component

The security layer provides authentication, authorization, and PII redaction.

### 3.2.1 Authentication

The system uses **JWT tokens** for authentication.

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str):
    # Authenticate user using credentials
    pass
```

### 3.2.2 Authorization

The system uses **role-based access control (RBAC)** for authorization.

```python
from rbac import RoleBasedAccessControl

rbac = RoleBasedAccessControl()

async def authorize_user(user: dict, action: str):
    # Authorize user using RBAC
    pass
```

## 3.3 UI Layer Component

The UI layer presents real-time insights and manages approvals.

### 3.3.1 UI Technology Stack

The UI is built using **React** and **TypeScript**.

```javascript
import React from 'react';
import { render } from 'react-dom';

const App = () => {
  // Render UI components
};

render(<App />, document.getElementById('root'));
```

### 3.3.2 Real-time Insights

The UI uses **SSE (Server-Sent Events)** for real-time updates.

```javascript
const eventSource = new EventSource('/api/v1/stream');
eventSource.onmessage = (event) => {
  console.log('Received event:', event.data);
};
```

*This section defines the detailed design of individual components. For data flow details, proceed to Section 04.*