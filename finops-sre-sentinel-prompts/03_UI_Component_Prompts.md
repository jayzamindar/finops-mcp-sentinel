# 03 - UI Component Prompts

**Document:** finops-sre-sentinel Prompts  
**Section:** UI Component Prompts  
**Target Audience:** Code Generation AI  
**Approx Tokens:** ~2,500

## 3.1 UI Component

Generate code for the UI component, including:

1. **Real-time insights**: Display real-time data using SSE.
2. **Approval management**: Manage approvals with risk assessment.

### 3.1.1 Prompt

```javascript
// Generate UI component code
// Use React and TypeScript
// Include real-time insights and approval management

import React from 'react';
import { render } from 'react-dom';

const App = () => {
  // Render UI components
};

render(<App />, document.getElementById('root'));
```

## 3.2 Real-time Insights

Generate code for displaying real-time insights using SSE.

### 3.2.1 Prompt

```javascript
// Generate SSE code for real-time updates
// Use EventSource API

const eventSource = new EventSource('/api/v1/stream');
eventSource.onmessage = (event) => {
  console.log('Received event:', event.data);
};
```

## 3.3 Approval Management

Generate code for managing approvals with risk assessment.

### 3.3.1 Prompt

```javascript
// Generate approval management code
// Include risk assessment and approval logic

const ApprovalRequest = () => {
  // Render approval request component
};

const ApprovalResponse = () => {
  // Render approval response component
};
```

*This section defines the prompts for generating UI component code. For security layer prompts, proceed to Section 04.*