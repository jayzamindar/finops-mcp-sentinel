// ============================================================
// FinOps-SRE Sentinel — Dashboard Metrics Component
// ============================================================

import React, { useState, useEffect } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

const MetricCard = ({ label, value, trend, unit, color }) => (
  <div className="metric-card" style={{ borderLeftColor: color }}>
    <div className="metric-label">{label}</div>
    <div className="metric-value">
      {typeof value === "number" ? value.toLocaleString() : value}
      {unit && <span className="metric-unit">{unit}</span>}
    </div>
    {trend !== undefined && (
      <div className={`metric-trend ${trend >= 0 ? "trend-up" : "trend-down"}`}>
        {trend >= 0 ? "▲" : "▼"} {Math.abs(trend)}%
      </div>
    )}
  </div>
);

const DashboardMetrics = () => {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await fetch(`${API_URL}/api/v1/dashboard/summary`);
        if (res.ok) setMetrics(await res.json());
      } catch (err) {
        console.error("Failed to fetch dashboard metrics:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className="metrics-loading">Loading metrics...</div>;
  if (!metrics) return <div className="metrics-error">Failed to load metrics</div>;

  return (
    <div className="dashboard-metrics">
      <div className="metrics-grid">
        <MetricCard
          label="Uptime"
          value={metrics.uptime_percent}
          unit="%"
          color="#22c55e"
        />
        <MetricCard
          label="Monthly Cost"
          value={`$${metrics.monthly_cost_usd?.toLocaleString()}`}
          trend={metrics.cost_trend_percent}
          color="#3b82f6"
        />
        <MetricCard
          label="Active Incidents"
          value={metrics.active_incidents}
          color="#ef4444"
        />
        <MetricCard
          label="Resolved Today"
          value={metrics.resolved_today}
          color="#22c55e"
        />
        <MetricCard
          label="Compliance Score"
          value={metrics.compliance_score}
          unit="%"
          color={metrics.compliance_score >= 80 ? "#22c55e" : "#f59e0b"}
        />
        <MetricCard
          label="Pending Approvals"
          value={metrics.pending_approvals}
          color={metrics.pending_approvals > 0 ? "#f59e0b" : "#22c55e"}
        />
        <MetricCard
          label="Pods Healthy"
          value={`${metrics.pods_healthy}/${metrics.pods_healthy + metrics.pods_unhealthy}`}
          color={metrics.pods_unhealthy > 0 ? "#f59e0b" : "#22c55e"}
        />
        <MetricCard
          label="Cluster CPU"
          value={metrics.cluster_cpu_percent}
          unit="%"
          color={metrics.cluster_cpu_percent > 80 ? "#ef4444" : "#3b82f6"}
        />
      </div>
    </div>
  );
};

export default DashboardMetrics;