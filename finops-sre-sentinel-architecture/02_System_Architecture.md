# 02 - System Architecture

**Document:** finops-sre-sentinel Architecture Document  
**Section:** System Architecture  
**Target Audience:** Technical Stakeholders, Developers  
**Approx Tokens:** ~2,500

## 2.1 High-Level Architecture

The MCP SRE Sentinel system is designed as a modular, scalable architecture to support the complex needs of fintech organizations.

### 2.1.1 Component Interactions

The system consists of several key components that interact with each other to provide a comprehensive SRE solution.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MCP SRE SENTINEL                            │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   MCP      │  │   Security   │  │   UI Layer   │  │   Tools    │  │
│  │  Server    │  │   Layer      │  │              │  │            │  │
│  └─────┬──────┘  └─────┬────────┘  └──────┬───────┘  └─────┬──────┘  │
│        │               │                  │               │         │
│        │               │                  │               │         │
│        ▼               ▼                  ▼               ▼         │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  NVIDIA    │  │  Ollama     │  │  React UI    │  │  Tool      │  │
│  │  NIM API   │  │  Local Models│  │              │  │  Registry  │  │
│  └────────────┘  └────────────┘  └──────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1.2 Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **MCP Server** | Handles MCP protocol requests, executes tools |
| **Security Layer** | Provides authentication, authorization, PII redaction |
| **UI Layer** | Presents real-time insights, manages approvals |
| **Tools** | Performs specific SRE tasks (e.g., diagnose, analyze, remediate) |

## 2.2 Technical Implementation

The system is built using a combination of technologies to ensure scalability, security, and performance.

### 2.2.1 Backend Technology Stack

- **Python 3.11+**: For the MCP server and tool execution
- **FastAPI**: For building the REST API
- **uv**: For package management

### 2.2.2 Frontend Technology Stack

- **React**: For building the UI components
- **TypeScript**: For type safety and maintainability
- **Material-UI**: For consistent design

## 2.3 Data Flow

The system processes data from various sources, including logs, metrics, and cloud cost data.

### 2.3.1 Data Sources

| Data Source | Description |
|-------------|-------------|
| **Logs** | Collected from various services and applications |
| **Metrics** | Collected from Prometheus and other monitoring tools |
| **Cloud Cost Data** | Collected from cloud providers (e.g., AWS, Azure) |

### 2.3.2 Data Processing

The system processes data using various tools and techniques, including:
- **Log analysis**: Using ELK Stack or similar tools
- **Metric analysis**: Using Prometheus and other monitoring tools
- **Cloud cost analysis**: Using cloud provider APIs and FinOps tools

*This section defines the high-level architecture of the system. For component design details, proceed to Section 03.*
