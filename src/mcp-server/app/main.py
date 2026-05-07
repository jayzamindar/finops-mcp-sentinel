# src/mcp-server/app/main.py
from fastapi import FastAPI, Depends
from fastmcp import MCPServer
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
mcp_server = MCPServer(app)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define tool registry and tool execution logic
tool_registry = ToolRegistry()

@app.post("/api/v1/tools/{tool_name}/execute")
async def execute_tool(tool_name: str, input_data: dict, token: str = Depends(oauth2_scheme)):
    tool = tool_registry.get_tool(tool_name)
    if tool:
        return await tool.execute(input_data)
    else:
        return {"error": "Tool not found"}