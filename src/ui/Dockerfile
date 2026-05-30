# ============================================================
# FinOps-SRE Sentinel — UI Dockerfile (Multi-Stage)
# ============================================================

# --- Stage 1: Build ---
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

# --- Stage 2: Serve ---
FROM nginx:1.25-alpine
# Custom nginx config for SPA routing + API proxy
COPY <<'EOF' /etc/nginx/conf.d/default.conf
server {
    listen 3001;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Proxy API requests to MCP server
    location /api/ {
        proxy_pass http://mcp-server:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }

    # Health check
    location /health {
        access_log off;
        return 200 '{"status":"ok"}';
        add_header Content-Type application/json;
    }
}
EOF

COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 3001
CMD ["nginx", "-g", "daemon off;"]