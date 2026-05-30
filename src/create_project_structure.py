import os

def create_project_structure():
    project_name = "finops-sre-sentinel"
    root_dir = os.getcwd()

    # Create project directory
    project_dir = os.path.join(root_dir, project_name)
    os.makedirs(project_dir, exist_ok=True)

    # Create subdirectories
    urd_dir = os.path.join(project_dir, "finops-sre-sentinel-urd-v3")
    architecture_dir = os.path.join(project_dir, "finops-sre-sentinel-architecture")
    prompts_dir = os.path.join(project_dir, "finops-sre-sentinel-prompts")
    src_dir = os.path.join(project_dir, "src")
    mcp_server_dir = os.path.join(src_dir, "mcp-server")
    app_dir = os.path.join(mcp_server_dir, "app")
    tools_dir = os.path.join(app_dir, "tools")
    security_dir = os.path.join(app_dir, "security")
    ui_dir = os.path.join(src_dir, "ui")
    public_dir = os.path.join(ui_dir, "public")
    ui_src_dir = os.path.join(ui_dir, "src")
    components_dir = os.path.join(ui_src_dir, "components")

    os.makedirs(urd_dir, exist_ok=True)
    os.makedirs(architecture_dir, exist_ok=True)
    os.makedirs(prompts_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(mcp_server_dir, exist_ok=True)
    os.makedirs(app_dir, exist_ok=True)
    os.makedirs(tools_dir, exist_ok=True)
    os.makedirs(security_dir, exist_ok=True)
    os.makedirs(ui_dir, exist_ok=True)
    os.makedirs(public_dir, exist_ok=True)
    os.makedirs(ui_src_dir, exist_ok=True)
    os.makedirs(components_dir, exist_ok=True)

    # Create files
    with open(os.path.join(app_dir, "__init__.py"), "w") as f:
        pass
    with open(os.path.join(app_dir, "main.py"), "w") as f:
        pass
    with open(os.path.join(tools_dir, "__init__.py"), "w") as f:
        pass
    with open(os.path.join(tools_dir, "diagnose_transaction_latency.py"), "w") as f:
        pass
    with open(os.path.join(tools_dir, "analyze_cloud_spend_anomaly.py"), "w") as f:
        pass
    with open(os.path.join(tools_dir, "remediate_unhealthy_pod.py"), "w") as f:
        pass
    with open(os.path.join(security_dir, "__init__.py"), "w") as f:
        pass
    with open(os.path.join(security_dir, "authentication.py"), "w") as f:
        pass
    with open(os.path.join(security_dir, "authorization.py"), "w") as f:
        pass
    with open(os.path.join(mcp_server_dir, "requirements.txt"), "w") as f:
        pass
    with open(os.path.join(mcp_server_dir, "Dockerfile"), "w") as f:
        pass
    with open(os.path.join(public_dir, "index.html"), "w") as f:
        pass
    with open(os.path.join(components_dir, "App.js"), "w") as f:
        pass
    with open(os.path.join(components_dir, "ApprovalRequest.js"), "w") as f:
        pass
    with open(os.path.join(components_dir, "RealTimeInsights.js"), "w") as f:
        pass
    with open(os.path.join(ui_src_dir, "index.js"), "w") as f:
        pass
    with open(os.path.join(ui_src_dir, "App.css"), "w") as f:
        pass
    with open(os.path.join(ui_dir, "package.json"), "w") as f:
        pass
    with open(os.path.join(ui_dir, "Dockerfile"), "w") as f:
        pass
    with open(os.path.join(project_dir, "docker-compose.yml"), "w") as f:
        pass

if __name__ == "__main__":
    create_project_structure()