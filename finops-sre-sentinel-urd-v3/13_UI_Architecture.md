# 13 - UI Architecture

**Document:** finops-sre-sentinel URD v3.0  
**Section:** UI Architecture  
**Target Audience:** Frontend Developers, UX Designers  
**Approx Tokens:** ~3,000

---

## 13.1 UI Requirements

The UI serves as the primary interface for users to interact with the MCP server. It must provide:

1. **Real-time insights** into system health and tool execution results
2. **Human-in-the-loop (HITL) approvals** for critical actions (e.g., pod restarts)
3. **Resource usage tracking** for operational governance
4. **Compliance monitoring** with drill-down capabilities

## 13.2 Technical Architecture

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

### 13.2.1 Component Tree

```
FinOps SRE Sentinel UI
├── Navigation Sidebar
│   ├── Dashboard (Overview)
│   ├── Incidents (Active/Past)
│   ├── Approvals (Pending Queue)
│   ├── Resource Usage (Execution Dashboard)
│   └── Compliance (Drift Reports)
│
├── Main Content Area
│   ├── Live Reasoning Feed (SSE Stream)
│   │   ├── Tool Execution Progress
│   │   ├── Tool Execution Results
│   │   └── Confidence Scores
│   │
│   ├── Approval Request Window
│   │   ├── Action Details
│   │   ├── Risk Assessment
│   │   ├── Approve/Reject Buttons
│   │   └── Comment Box
│   │
│   └── Dashboard Panels
│       ├── MTTR Trend Chart
│       ├── Tool Execution Rate
│       ├── Active Incidents
│       └── Compliance Score
│
└── Footer
    ├── Audit Log Export
    └── Session Info
```

### 13.2.2 Key Components

| Component | File | Description |
|-----------|------|-------------|
| **DashboardMetrics** | `components/DashboardMetrics.js` | Displays system health metrics, execution counts, and status overview |
| **ToolRunner** | `components/ToolRunner.js` | Interface for selecting and executing MCP tools with input forms |
| **RealTimeInsights** | `components/RealTimeInsights.js` | SSE-powered live feed of tool execution results and system events |
| **ApprovalRequest** | `components/ApprovalRequest.js` | HITL approval interface for high-risk actions with approve/reject workflow |

### 13.2.3 Key Features

1. **Live Reasoning Feed**: Displays tool execution progress via SSE at `/api/v1/stream/insights`
2. **Approval Dashboard**: Manages pending approvals with risk assessment
3. **Resource Usage Dashboard**: Tracks tool execution counts and performance metrics
4. **Compliance Monitoring**: Shows compliance status with drill-down
5. **Incident Timeline**: Visualizes incident response timeline

## 13.3 Technical Implementation

### Frontend Framework
- **React 18** (JavaScript, NOT TypeScript) with `createRoot` API for concurrent rendering
- **Custom CSS** for styling (project-specific design system)
- **SSE (EventSource)** for real-time server-sent events from `/api/v1/stream/insights`
- **fetch API** for REST calls to MCP server endpoints

### State Management
- **React Hooks** (`useState`, `useEffect`) for local component state
- **Context API** for shared state across components (auth, tool registry)

### API Integration
- REST API calls to MCP server at `http://localhost:8000` for data
- SSE (Server-Sent Events) at `/api/v1/stream/insights` for real-time updates
- MCP JSON-RPC 2.0 at `/mcp` for MCP protocol communication

### 13.3.1 Entry Point

```javascript
// src/ui/src/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### 13.3.2 API Communication Pattern

```javascript
// REST call with API Key authentication
const response = await fetch('http://localhost:8000/api/v1/tools', {
  headers: { 'X-API-Key': apiKey }
});
const tools = await response.json();

// SSE connection for real-time insights
const eventSource = new EventSource('/api/v1/stream/insights');
eventSource.addEventListener('tool:execution', (event) => {
  const data = JSON.parse(event.data);
  // Update UI with real-time tool execution progress
});
```

## 13.4 Security Considerations

1. **Authentication**: API Key stored in client state, sent via `X-API-Key` header
2. **Authorization**: Tool access controlled by server-side RBAC based on API key role
3. **Data Protection**: Sensitive data masked/redacted server-side before reaching UI
4. **Audit Logging**: All user interactions logged via MCP server audit trail

## 13.5 Performance Optimization

1. **Code splitting**: Load components on demand via React.lazy()
2. **SSE over polling**: Real-time updates via server-sent events instead of client polling
3. **Lazy loading**: Load heavy components lazily
4. **Memoization**: React.memo() for expensive component renders

*The UI architecture must be responsive, secure, and provide real-time insights. For local environment setup, proceed to Section 14.*