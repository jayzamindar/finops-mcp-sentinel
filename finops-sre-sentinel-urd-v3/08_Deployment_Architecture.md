# 08 - Deployment Architecture

**Document:** finops-sre-sentinel URD v3.0  
**Section:** Deployment Architecture  
**Target Audience:** DevOps Engineers, System Administrators  
**Approx Tokens:** ~3,000

---

## 8.1 Local Development Environment

| Layer | Technology | Alternative Considered | Reasoning |
|-------|-----------|---------------------|-----------|
| **Backend Server** | FastAPI | Flask, Django | FastAPI chosen for async capabilities and OpenAPI support |
| **Frontend UI** | React | Angular, Vue.js | React chosen for component-based architecture and ecosystem |
| **AI Model** | NVIDIA NIM API | Other cloud AI providers (e.g., AWS SageMaker) | NVIDIA NIM chosen for free tier and performance |


The project uses **Docker Compose** for local development. This setup includes:

- MCP Server (FastAPI)
- Prometheus (Metrics)
- Grafana (Dashboards)
- Mock Backing Services (Prometheus, Elasticsearch, Kubernetes)

### 8.1.1 Docker Compose Stack

```yaml
version: '3.8'
services:
  mcp-server:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - prometheus
      - grafana
    environment:
      - NVIDIA_API_KEY=${NVIDIA_API_KEY}
      - OLLAMA_ENDPOINT=http://ollama:11434

  prometheus:
    image: prometheus/prometheus:v2.45.0
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:9.3.6
    ports:
      - "3000:3000"
    volumes:
      - ./grafana-dashboards:/var/lib/grafana/dashboards

  # Mock services for development
  mock-prometheus:
    image: mock-prometheus:latest
    ports:
      - "9091:9090"

  mock-elasticsearch:
    image: mock-elasticsearch:latest
    ports:
      - "9201:9200"
```

### 8.1.2 Local Testing

- Use `docker-compose up` to start the stack
- Access MCP Server at `http://localhost:8000`
- Prometheus at `http://localhost:9090`
- Grafana at `http://localhost:3000`

## 8.2 Production Deployment

For production, the MCP server will be deployed using **Kubernetes**. The deployment includes:

- MCP Server Deployment
- Prometheus Operator for monitoring
- Grafana for visualization
- Kubernetes Service for exposing the MCP server

### 8.2.1 Kubernetes Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: finops-sre-sentinel/mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: NVIDIA_API_KEY
          valueFrom:
            secretKeyRef:
              name: nvidia-api-key
              key: api_key
```

## 8.3 Hybrid Deployment (Mock + Real)

The system supports a **hybrid deployment** where some services are mocked for development/testing, while others connect to real infrastructure for demos.

### 8.3.1 Configuration

The `config.yaml` file controls whether to use mock or real services.

```yaml
services:
  prometheus:
    type: "mock"  # or "real"
    endpoint: "http://mock-prometheus:9090"  # for mock
    # endpoint: "http://prometheus:9090"  # for real

  kubernetes:
    type: "mock"  # or "real"
    endpoint: "http://mock-kubernetes:8080"  # for mock
    # endpoint: "https://kubernetes.default.svc"  # for real
```

## 8.4 Deployment Checklist

Before deploying:

- [ ] Ensure NVIDIA API key is stored securely in `.env`
- [ ] Configure `config.yaml` for desired service types (mock/real)
- [ ] Verify Docker images are built and pushed to registry
- [ ] Kubernetes cluster is accessible and configured

*This section defines how the system will be deployed. For testing scenarios, proceed to Section 09.*