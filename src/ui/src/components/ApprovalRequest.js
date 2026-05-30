// ============================================================
// FinOps-SRE Sentinel — Approval Queue Component
// ============================================================

import React, { useState, useEffect } from "react";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8080";

const RISK_COLORS = {
  low: "#22c55e",
  medium: "#f59e0b",
  high: "#ef4444",
  critical: "#dc2626",
};

const ApprovalRequest = () => {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState(null);

  useEffect(() => {
    fetchPendingApprovals();
    const interval = setInterval(fetchPendingApprovals, 15000);
    return () => clearInterval(interval);
  }, []);

  const fetchPendingApprovals = async () => {
    try {
      const res = await fetch(`${API_URL}/api/v1/approvals/pending`);
      if (res.ok) {
        const data = await res.json();
        setRequests(data.approvals || []);
      }
    } catch (err) {
      console.error("Failed to fetch approvals:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleApproval = async (requestId, action) => {
    setProcessingId(requestId);
    try {
      const res = await fetch(`${API_URL}/api/v1/approvals/${requestId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action, user: "demo-operator" }),
      });
      if (res.ok) {
        setRequests((prev) => prev.filter((r) => r.id !== requestId));
      }
    } catch (err) {
      console.error("Failed to submit approval:", err);
    } finally {
      setProcessingId(null);
    }
  };

  if (loading) return <div className="loading">Loading approvals...</div>;

  if (requests.length === 0)
    return (
      <div className="empty-state">
        <span className="empty-icon">✅</span>
        <p>No pending approvals — all clear</p>
      </div>
    );

  return (
    <div className="approval-requests">
      <div className="approval-count">
        {requests.length} pending request{requests.length !== 1 ? "s" : ""}
      </div>
      {requests.map((req) => {
        const riskColor = RISK_COLORS[req.risk_label] || "#6b7280";
        const isProcessing = processingId === req.id;
        return (
          <div key={req.id} className="approval-card">
            <div className="approval-header">
              <div className="approval-title-row">
                <span className="tool-name">{req.tool}</span>
                <span className="approval-action-tag">{req.action}</span>
              </div>
              <span
                className="risk-badge"
                style={{ backgroundColor: riskColor }}
              >
                Risk: {req.risk_score}/100 ({req.risk_label})
              </span>
            </div>

            <div className="approval-body">
              <p className="approval-target">
                <strong>Target:</strong> {req.target}
              </p>
              <p className="approval-reason">{req.reason}</p>
              {req.proposed_command && (
                <pre className="approval-command">
                  <code>$ {req.proposed_command}</code>
                </pre>
              )}
            </div>

            <div className="approval-footer">
              <span className="approval-requested-by">
                Requested by {req.requested_by} · {req.requested_at}
              </span>
              <div className="approval-actions">
                <button
                  className="btn-approve"
                  onClick={() => handleApproval(req.id, "approve")}
                  disabled={isProcessing}
                >
                  {isProcessing ? "Processing..." : "✓ Approve"}
                </button>
                <button
                  className="btn-reject"
                  onClick={() => handleApproval(req.id, "reject")}
                  disabled={isProcessing}
                >
                  ✗ Reject
                </button>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ApprovalRequest;