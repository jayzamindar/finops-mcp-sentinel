// ============================================================
// FinOps-SRE Sentinel — Real-Time Insights (SSE Stream)
// ============================================================

import React, { useState, useEffect, useRef } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

const SEVERITY_STYLES = {
  critical: { bg: "#fef2f2", border: "#ef4444", badge: "#dc2626", icon: "🔴" },
  high: { bg: "#fff7ed", border: "#f97316", badge: "#ea580c", icon: "🟠" },
  warning: { bg: "#fffbeb", border: "#f59e0b", badge: "#d97706", icon: "🟡" },
  medium: { bg: "#fffbeb", border: "#f59e0b", badge: "#d97706", icon: "🟡" },
  info: { bg: "#eff6ff", border: "#3b82f6", badge: "#2563eb", icon: "🔵" },
};

const TYPE_ICONS = {
  alert: "⚠️",
  cost: "💰",
  compliance: "📋",
  event: "📡",
};

const RealTimeInsights = () => {
  const [insights, setInsights] = useState([]);
  const [connected, setConnected] = useState(false);
  const eventSourceRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      const eventSource = new EventSource(`${API_URL}/api/v1/stream`);
      eventSourceRef.current = eventSource;

      eventSource.onopen = () => setConnected(true);

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setInsights((prev) => [data, ...prev].slice(0, 100));
        } catch {
          console.warn("Failed to parse SSE event:", event.data);
        }
      };

      eventSource.onerror = () => {
        setConnected(false);
        eventSource.close();
        // Auto-reconnect after 5s
        setTimeout(connect, 5000);
      };
    };

    connect();
    return () => {
      if (eventSourceRef.current) eventSourceRef.current.close();
    };
  }, []);

  const getSeverityStyle = (severity) =>
    SEVERITY_STYLES[severity] || SEVERITY_STYLES.info;

  return (
    <div className="real-time-insights">
      <div className="insights-header">
        <div className="connection-status">
          <span className={`status-dot ${connected ? "connected" : "disconnected"}`} />
          <span className="status-text">
            {connected ? "Live — Connected" : "Reconnecting..."}
          </span>
        </div>
        <span className="event-count">{insights.length} events</span>
      </div>

      {insights.length === 0 ? (
        <div className="empty-state">
          <span className="empty-icon">📡</span>
          <p>Waiting for infrastructure events...</p>
        </div>
      ) : (
        <div className="insights-stream">
          {insights.map((event, idx) => {
            const style = getSeverityStyle(event.severity);
            return (
              <div
                key={event.id || idx}
                className="insight-card"
                style={{
                  backgroundColor: style.bg,
                  borderLeft: `4px solid ${style.border}`,
                }}
              >
                <div className="insight-card-header">
                  <span className="insight-icon">
                    {TYPE_ICONS[event.type] || "📡"}
                  </span>
                  <span
                    className="severity-badge"
                    style={{ backgroundColor: style.badge }}
                  >
                    {event.severity?.toUpperCase()}
                  </span>
                  <span className="insight-type-tag">{event.type}</span>
                  <span className="insight-service">{event.service}</span>
                  <span className="insight-time">
                    {event.timestamp
                      ? new Date(event.timestamp).toLocaleTimeString()
                      : ""}
                  </span>
                </div>
                <p className="insight-message">{event.message}</p>
                {event.source && (
                  <span className="insight-source">via {event.source}</span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default RealTimeInsights;