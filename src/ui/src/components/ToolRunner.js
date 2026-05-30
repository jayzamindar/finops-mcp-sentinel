// ============================================================
// FinOps-SRE Sentinel — Tool Runner Component
// ============================================================
// Allows operators to manually trigger MCP tools from the UI
// ============================================================

import React, { useState, useEffect } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

const TOOL_INPUTS = {
  analyze_cloud_spend_anomaly: {
    label: "Cloud Spend Anomaly",
    icon: "💰",
    defaults: {
      namespace: "production",
      cost_threshold_percent: 20,
      include_forecasts: true,
    },
    fields: [
      { key: "namespace", label: "Namespace", type: "text" },
      { key: "cost_threshold_percent", label: "Threshold %", type: "number" },
      { key: "include_forecasts", label: "Include Forecasts", type: "checkbox" },
    ],
  },
  diagnose_transaction_latency: {
    label: "Transaction Latency",
    icon: "⏱️",
    defaults: {
      service_name: "payment-gateway",
      threshold_ms: 500,
      limit: 50,
    },
    fields: [
      { key: "service_name", label: "Service", type: "text" },
      { key: "threshold_ms", label: "Threshold (ms)", type: "number" },
      { key: "limit", label: "Max Results", type: "number" },
    ],
  },
  remediate_unhealthy_pod: {
    label: "Pod Remediation",
    icon: "🔧",
    defaults: {
      namespace: "",
      auto_approve: false,
      max_risk_score: 50,
    },
    fields: [
      { key: "namespace", label: "Namespace (blank=all)", type: "text" },
      { key: "auto_approve", label: "Auto-Approve", type: "checkbox" },
      { key: "max_risk_score", label: "Max Risk Score", type: "number" },
    ],
  },
  verify_compliance_drift: {
    label: "Compliance Drift",
    icon: "📋",
    defaults: {
      frameworks: ["PCI-DSS", "SOC2", "GDPR"],
      include_passing: true,
    },
    fields: [
      { key: "include_passing", label: "Include Passing", type: "checkbox" },
    ],
  },
};

const ToolRunner = () => {
  const [tools, setTools] = useState([]);
  const [selectedTool, setSelectedTool] = useState("");
  const [inputs, setInputs] = useState({});
  const [result, setResult] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/api/v1/tools`)
      .then((res) => res.json())
      .then((data) => setTools(data.tools || []))
      .catch(() => {});
  }, []);

  const handleToolSelect = (toolName) => {
    setSelectedTool(toolName);
    setResult(null);
    setError(null);
    const config = TOOL_INPUTS[toolName];
    setInputs(config ? { ...config.defaults } : {});
  };

  const handleInputChange = (key, value) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  const executeTool = async () => {
    setExecuting(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API_URL}/api/v1/tools/${selectedTool}/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(inputs),
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || "Execution failed");
      }
      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setExecuting(false);
    }
  };

  const config = TOOL_INPUTS[selectedTool];

  return (
    <div className="tool-runner">
      <div className="tool-selector">
        {Object.entries(TOOL_INPUTS).map(([key, cfg]) => (
          <button
            key={key}
            className={`tool-select-btn ${selectedTool === key ? "active" : ""}`}
            onClick={() => handleToolSelect(key)}
          >
            <span className="tool-icon">{cfg.icon}</span>
            <span className="tool-label">{cfg.label}</span>
          </button>
        ))}
      </div>

      {config && (
        <div className="tool-config">
          <h3>
            {config.icon} {config.label} — Configuration
          </h3>
          <div className="tool-fields">
            {config.fields.map((field) => (
              <div key={field.key} className="tool-field">
                <label htmlFor={`tool-${field.key}`}>{field.label}</label>
                {field.type === "checkbox" ? (
                  <input
                    id={`tool-${field.key}`}
                    type="checkbox"
                    checked={inputs[field.key] || false}
                    onChange={(e) => handleInputChange(field.key, e.target.checked)}
                  />
                ) : (
                  <input
                    id={`tool-${field.key}`}
                    type={field.type}
                    value={inputs[field.key] ?? ""}
                    onChange={(e) =>
                      handleInputChange(
                        field.key,
                        field.type === "number" ? Number(e.target.value) : e.target.value
                      )
                    }
                  />
                )}
              </div>
            ))}
          </div>
          <button
            className="btn-execute"
            onClick={executeTool}
            disabled={executing}
          >
            {executing ? "⏳ Executing..." : `▶ Execute ${config.label}`}
          </button>
        </div>
      )}

      {error && (
        <div className="tool-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="tool-result">
          <div className="result-header">
            <h3>Result — {result.tool}</h3>
            <span className="result-time">Executed at {result.executed_at}</span>
          </div>
          <pre className="result-json">
            {JSON.stringify(result.result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default ToolRunner;