// ============================================================
// FinOps-SRE Sentinel — App Root (Full Dashboard)
// ============================================================

import React, { useState } from "react";
import DashboardMetrics from "./components/DashboardMetrics";
import RealTimeInsights from "./components/RealTimeInsights";
import ApprovalRequest from "./components/ApprovalRequest";
import ToolRunner from "./components/ToolRunner";
import "./App.css";

const TABS = [
  { key: "overview", label: "Overview", icon: "📊" },
  { key: "stream", label: "Live Stream", icon: "📡" },
  { key: "approvals", label: "Approvals", icon: "✅" },
  { key: "tools", label: "Tool Runner", icon: "🔧" },
];

const App = () => {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-brand">
          <span className="logo-icon">🛡️</span>
          <div>
            <h1>FinOps-SRE Sentinel</h1>
            <p className="header-subtitle">
              AI-powered SRE platform for fintech infrastructure
            </p>
          </div>
        </div>
        <div className="header-status">
          <span className="status-indicator online" />
          <span>System Online</span>
        </div>
      </header>

      <nav className="app-nav">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            className={`nav-tab ${activeTab === tab.key ? "active" : ""}`}
            onClick={() => setActiveTab(tab.key)}
          >
            <span className="nav-icon">{tab.icon}</span>
            <span className="nav-label">{tab.label}</span>
          </button>
        ))}
      </nav>

      <main className="app-main">
        {activeTab === "overview" && (
          <div className="tab-content">
            <DashboardMetrics />
            <div className="overview-grid">
              <section className="section-card">
                <h2 className="section-title">📡 Recent Events</h2>
                <RealTimeInsights />
              </section>
              <section className="section-card">
                <h2 className="section-title">✅ Pending Approvals</h2>
                <ApprovalRequest />
              </section>
            </div>
          </div>
        )}

        {activeTab === "stream" && (
          <div className="tab-content">
            <section className="section-card full-width">
              <h2 className="section-title">
                📡 Real-Time Infrastructure Event Stream
              </h2>
              <RealTimeInsights />
            </section>
          </div>
        )}

        {activeTab === "approvals" && (
          <div className="tab-content">
            <section className="section-card full-width">
              <h2 className="section-title">
                ✅ Approval Queue — Human-in-the-Loop
              </h2>
              <ApprovalRequest />
            </section>
          </div>
        )}

        {activeTab === "tools" && (
          <div className="tab-content">
            <section className="section-card full-width">
              <h2 className="section-title">
                🔧 MCP Tool Runner — Execute & Inspect
              </h2>
              <ToolRunner />
            </section>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <span>FinOps-SRE Sentinel v1.0.0</span>
        <span>·</span>
        <span>MCP Server: localhost:8080</span>
        <span>·</span>
        <span>UI: localhost:3001</span>
      </footer>
    </div>
  );
};

export default App;