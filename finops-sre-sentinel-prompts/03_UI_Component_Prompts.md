# 03 - UI Component Prompts

**Document:** finops-sre-sentinel Prompts
**Section:** UI Component Prompts
**Target Audience:** Code Generation AI (or human developers)

## 3.1 UI Overview

The UI is built with **React 18 in JavaScript** (NOT TypeScript). It uses functional components with hooks, `createRoot` API, and communicates with the MCP server via REST (`/api/v1/tools`) and SSE (`/api/v1/stream/insights`).

### Key Corrections from Previous Version
- ❌ Was: React + TypeScript with `render()` from `react-dom`
- ✅ Now: React 18 JavaScript with `createRoot()` from `react-dom/client`
- ❌ Was: SSE at `/api/v1/stream`
- ✅ Now: SSE at `/api/v1/stream/insights`
- ❌ Was: Separate `ApprovalRequest` and `ApprovalResponse` components
- ✅ Now: Single `ApprovalRequest` component with approve/deny callbacks

## 3.2 Entry Point (index.js)

### 3.2.1 Prompt

```javascript
// Generate React 18 entry point
// Key patterns:
//   - Use createRoot from 'react-dom/client' (NOT render from 'react-dom')
//   - Import App from './components/App' (the main app is in components/)
//   - StrictMode wrapper

import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './components/App';

const root = createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## 3.3 Main App Component (App.js)

The main App component manages state for tools list, active tab, and SSE insights.

### 3.3.1 Prompt

```javascript
// Generate main App component
// Key patterns:
//   - useState for tools, activeTab, insights
//   - useEffect to fetch tools from /api/v1/tools on mount
//   - Renders tabs: Dashboard, Run Tool, Real-Time Insights, Approvals
//   - DashboardMetrics shows tool count + latest insight
//   - ToolRunner lets user select and invoke tools
//   - RealTimeInsights shows SSE stream data

import React, { useState, useEffect } from 'react';
import DashboardMetrics from './DashboardMetrics';
import ToolRunner from './ToolRunner';
import RealTimeInsights from './RealTimeInsights';
import ApprovalRequest from './ApprovalRequest';
```

## 3.4 DashboardMetrics Component

Displays summary statistics: total tools, latest insight, system status.

### 3.4.1 Prompt

```javascript
// Generate DashboardMetrics component
// Key patterns:
//   - Receives tools (array) and insights (array) as props
//   - Shows tool count, latest insight text, timestamp
//   - Card-based layout

const DashboardMetrics = ({ tools, insights }) => {
  const latestInsight = insights.length > 0 ? insights[insights.length - 1] : null;
  // Render metric cards
};
```

## 3.5 ToolRunner Component

Allows users to select a tool, fill in parameters, and invoke it with an API key.

### 3.5.1 Prompt

```javascript
// Generate ToolRunner component
// Key patterns:
//   - Receives tools (array) as prop
//   - useState for selectedTool, parameters (JSON string), apiKey, result
//   - POST to /api/v1/tools/{name}/invoke with X-API-Key header
//   - Displays result content array as formatted text
//   - Loading and error states

const ToolRunner = ({ tools }) => {
  const [selectedTool, setSelectedTool] = useState('');
  const [parameters, setParameters] = useState('{}');
  const [apiKey, setApiKey] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
};
```

## 3.6 RealTimeInsights Component

Displays SSE stream events from `/api/v1/stream/insights`.

### 3.6.1 Prompt

```javascript
// Generate RealTimeInsights component
// Key patterns:
//   - useEffect creates EventSource to /api/v1/stream/insights
//   - Appends incoming events to insights array state
//   - Auto-scrolls to latest event
//   - Shows event type, data, and timestamp
//   - Cleanup: close EventSource on unmount

import React, { useState, useEffect, useRef } from 'react';

const RealTimeInsights = ({ insights, setInsights }) => {
  // Uses EventSource API for SSE
  // Endpoint: /api/v1/stream/insights
};
```

## 3.7 ApprovalRequest Component

Displays pending approval requests with approve/deny actions.

### 3.7.1 Prompt

```javascript
// Generate ApprovalRequest component
// Key patterns:
//   - Receives approval requests as prop
//   - Shows risk level (LOW/MEDIUM/HIGH/CRITICAL) with color coding
//   - Approve/Deny buttons trigger callbacks
//   - Shows confidence score and rationale

const ApprovalRequest = ({ requests, onApprove, onDeny }) => {
  // Render approval cards with risk badges
};
```

*For security layer prompts, proceed to Section 04.*