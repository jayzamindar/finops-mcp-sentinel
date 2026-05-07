# 15 - Connection Documentation

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Connection Documentation  
**Target Audience:** Developers, Integration Engineers  
**Approx Tokens:** ~2,500

---

## 15.1 MCP Client Connection Guide

The MCP server supports multiple client connection methods:

1. **STDIO**: For local development and testing
2. **SSE (Server-Sent Events)**: For real-time updates in web UI
3. **REST APIs**: For tool execution and data retrieval

### 15.1.1 STDIO Connection

For local development:

1. Run `mcp dev server.py` to start the MCP server in dev mode
2. Use `stdio` protocol to communicate with the server

### 15.1.2 SSE Connection

For web UI:

1. Connect to `http://localhost:8000/api/v1/stream` using SSE
2. Specify `client_id` and `event_types` as query parameters

Example:
```javascript
const eventSource = new EventSource('http://localhost:8000/api/v1/stream?client_id=my_client&events=tool:execution,approval:request');
eventSource.onmessage = (event) => {
  console.log('Received event:', event.data);
};
```

### 15.1.3 REST API Connection

For tool execution and data retrieval:

1. Use `POST /api/v1/tools/{tool_name}/execute` to execute tools
2. Include `Authorization: Bearer {jwt_token}` header for authentication

Example:
```bash
curl -X POST \
  http://localhost:8000/api/v1/tools/diagnose_transaction_latency/execute \
  -H 'Authorization: Bearer your_jwt_token' \
  -H 'Content-Type: application/json' \
  -d '{"service_name": "payment-gateway"}'
```

## 15.2 Client Integration

To integrate with the MCP server:

1. **Claude Desktop/Cursor IDE**: Use `stdio` protocol for local development
2. **Web UI**: Use SSE for real-time updates
3. **Custom Applications**: Use REST APIs for tool execution and data retrieval

## 15.3 Security Considerations

1. **Authentication**: Use JWT tokens with role-based access control
2. **Authorization**: Fine-grained permissions based on user roles
3. **Data Protection**: Sensitive data masked/redacted in responses

*This section provides guidance on connecting to the MCP server. For the MCP blueprint reference, proceed to Section 16.*