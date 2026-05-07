# 02 - MCP Server Prompts

**Document:** finops-sre-sentinel Prompts  
**Section:** MCP Server Prompts  
**Target Audience:** Code Generation AI  
**Approx Tokens:** ~2,000

## 2.1 MCP Server Core

Generate code for the MCP server core, including:

1. **Tool execution**: Execute tools using the tool registry.
2. **Security measures**: Implement authentication, authorization, and PII redaction.

### 2.1.1 Prompt

```python
# Generate MCP server core code
# Use FastAPI and Python 3.11+
# Include tool execution and security measures

from fastapi import FastAPI
from fastmcp import MCPServer

app = FastAPI()
mcp_server = MCPServer(app)

# Define tool registry and tool execution logic
```

## 2.2 Tool Registry

Generate code for the tool registry, including:

1. **Tool definitions**: Define tools and their schemas.
2. **Tool execution logic**: Implement tool execution logic.

### 2.2.1 Prompt

```python
# Generate tool registry code
# Define tools and their schemas
# Implement tool execution logic

from tool_registry import ToolRegistry

tool_registry = ToolRegistry()

# Define tools and their schemas
```

*This section defines the prompts for generating MCP server code. For UI component prompts, proceed to Section 03.*
