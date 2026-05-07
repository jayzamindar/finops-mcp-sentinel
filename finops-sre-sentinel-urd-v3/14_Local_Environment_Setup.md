# 14 - Local Environment Setup

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Local Environment Setup  
**Target Audience:** Developers, New Contributors  
**Approx Tokens:** ~4,000

---

## 14.1 Prerequisites

Before setting up the project locally, ensure you have the following installed:

1. **Docker Desktop**: For containerization and local Kubernetes
2. **Python 3.11+**: For the MCP server
3. **Node.js 18+**: For the React UI
4. **uv**: Python package manager
5. **VS Code**: Recommended IDE with Continue.dev plugin
6. **Ollama**: For local AI model inference

## 14.2 One-Click Setup Script

The project includes a **one-click setup PowerShell script** (`setup.ps1`) that:

1. Checks for prerequisites
2. Installs missing dependencies
3. Configures environment variables
4. Starts the Docker containers

### 14.2.1 Script Logic

```powershell
# setup.ps1
Write-Host "Checking prerequisites..."
if (!(docker --version)) {
    Write-Host "Installing Docker Desktop..."
    # Install Docker Desktop
}

if (!(python --version -eq "Python 3.11")) {
    Write-Host "Installing Python 3.11..."
    # Install Python 3.11
}

# Continue with uv installation, Docker compose up, etc.
```

## 14.3 Manual Setup Steps (if needed)

If the one-click script fails or you prefer manual setup:

1. **Install Docker Desktop** and enable Kubernetes
2. **Install Python 3.11+** and `uv`
3. **Run `uv sync`** to install Python dependencies
4. **Configure `.env`** file with NVIDIA API key
5. **Start Docker containers** using `docker-compose up`

## 14.4 Verifying the Setup

After setup, verify:

1. MCP server is running on `http://localhost:8000`
2. React UI is accessible at `http://localhost:3000`
3. Prometheus and Grafana are running
4. Ollama is configured correctly

## 14.5 Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Docker container fails to start | Check logs, ensure prerequisites installed |
| MCP server not responding | Verify `.env` configuration, check server logs |
| UI not loading | Check browser console for errors, ensure Node.js/npm installed |

*This section guides new contributors through setting up the project locally. For connection documentation, proceed to Section 15.*