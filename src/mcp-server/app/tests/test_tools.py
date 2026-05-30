# ============================================================
# FinOps-SRE Sentinel — Tool Unit Tests
# ============================================================
# Tests each MCP tool module directly, validating output
# structure and deterministic behavior.
# ============================================================

import pytest
from app.tools import (
    analyze_cloud_spend_anomaly,
    diagnose_transaction_latency,
    remediate_unhealthy_pod,
    verify_compliance_drift,
)


class TestAnalyzeCloudSpendAnomaly:
    """Tests for the cloud spend anomaly detection tool."""

    @pytest.mark.asyncio
    async def test_returns_required_fields(self):
        result = await analyze_cloud_spend_anomaly.execute({
            "namespace": "production",
            "cost_threshold_percent": 20,
            "include_forecasts": True,
        })
        assert "baseline_monthly_cost_usd" in result
        assert "current_monthly_cost_usd" in result
        assert "anomaly_detected" in result
        assert "anomaly_percent" in result
        assert "top_charges" in result
        assert "recommendations" in result
        assert isinstance(result["top_charges"], list)
        assert isinstance(result["recommendations"], list)

    @pytest.mark.asyncio
    async def test_deterministic_output(self):
        """Same inputs produce identical results across runs (excluding timestamp)."""
        args = {"namespace": "production", "cost_threshold_percent": 20, "include_forecasts": True}
        r1 = await analyze_cloud_spend_anomaly.execute(args)
        r2 = await analyze_cloud_spend_anomaly.execute(args)
        # Exclude timestamp fields from comparison
        r1.pop("analyzed_at", None)
        r2.pop("analyzed_at", None)
        assert r1 == r2

    @pytest.mark.asyncio
    async def test_forecasts_included(self):
        result = await analyze_cloud_spend_anomaly.execute({"include_forecasts": True})
        assert "forecast_month_end_usd" in result
        assert "forecast_confidence" in result

    @pytest.mark.asyncio
    async def test_forecasts_excluded(self):
        result = await analyze_cloud_spend_anomaly.execute({"include_forecasts": False})
        assert "forecast_month_end_usd" not in result

    @pytest.mark.asyncio
    async def test_top_charges_sorted_by_delta(self):
        result = await analyze_cloud_spend_anomaly.execute({})
        charges = result["top_charges"]
        for i in range(len(charges) - 1):
            assert abs(charges[i]["delta_usd"]) >= abs(charges[i + 1]["delta_usd"])


class TestDiagnoseTransactionLatency:
    """Tests for the transaction latency diagnosis tool."""

    @pytest.mark.asyncio
    async def test_returns_required_fields(self):
        result = await diagnose_transaction_latency.execute({
            "service_name": "payment-gateway",
            "threshold_ms": 500,
        })
        assert "service_analyzed" in result
        assert "latency_p50_ms" in result
        assert "latency_p95_ms" in result
        assert "latency_p99_ms" in result
        assert "slow_traces_detail" in result
        assert "root_cause_breakdown" in result
        assert isinstance(result["slow_traces_detail"], list)
        assert isinstance(result["root_cause_breakdown"], list)

    @pytest.mark.asyncio
    async def test_deterministic_output(self):
        """Same inputs produce identical results across runs (excluding timestamps)."""
        args = {"service_name": "payment-gateway", "threshold_ms": 500}
        r1 = await diagnose_transaction_latency.execute(args)
        r2 = await diagnose_transaction_latency.execute(args)
        r1.pop("analyzed_at", None)
        r2.pop("analyzed_at", None)
        # Strip per-trace timestamps (based on datetime.now())
        for trace_list in (r1.get("slow_traces_detail", []), r2.get("slow_traces_detail", [])):
            for t in trace_list:
                t.pop("timestamp", None)
        assert r1 == r2

    @pytest.mark.asyncio
    async def test_percentile_ordering(self):
        result = await diagnose_transaction_latency.execute({"service_name": "payment-gateway"})
        assert result["latency_p50_ms"] <= result["latency_p95_ms"] <= result["latency_p99_ms"]


class TestRemediateUnhealthyPod:
    """Tests for the pod remediation tool."""

    @pytest.mark.asyncio
    async def test_returns_required_fields(self):
        result = await remediate_unhealthy_pod.execute({
            "auto_approve": False,
        })
        assert "pods" in result
        assert "pending_approval" in result
        assert "total_unhealthy_pods" in result
        assert "actions_taken" in result
        assert isinstance(result["pods"], list)
        assert isinstance(result["actions_taken"], list)

    @pytest.mark.asyncio
    async def test_high_risk_needs_approval(self):
        result = await remediate_unhealthy_pod.execute({"auto_approve": False})
        # When auto_approve=False, all pods require approval
        for pod in result["pods"]:
            assert "proposed_action" in pod
            assert "risk_score" in pod
            assert pod["requires_approval"] is True

    @pytest.mark.asyncio
    async def test_deterministic_output(self):
        """Same inputs produce identical results across runs (excluding timestamp)."""
        args = {"auto_approve": False}
        r1 = await remediate_unhealthy_pod.execute(args)
        r2 = await remediate_unhealthy_pod.execute(args)
        r1.pop("analyzed_at", None)
        r2.pop("analyzed_at", None)
        # Also strip detected_at from individual pods
        for p in r1.get("pods", []):
            p.pop("detected_at", None)
        for p in r2.get("pods", []):
            p.pop("detected_at", None)
        assert r1 == r2


class TestVerifyComplianceDrift:
    """Tests for the compliance drift verification tool."""

    @pytest.mark.asyncio
    async def test_returns_required_fields(self):
        result = await verify_compliance_drift.execute({})
        assert "frameworks" in result
        assert "findings" in result
        assert "top_risks" in result
        assert "overall_compliance_score" in result
        assert isinstance(result["frameworks"], dict)
        assert isinstance(result["findings"], list)
        assert isinstance(result["top_risks"], list)

    @pytest.mark.asyncio
    async def test_specific_frameworks(self):
        result = await verify_compliance_drift.execute({
            "frameworks": ["PCI-DSS", "SOC2"],
        })
        fw_names = list(result["frameworks"].keys())
        assert "PCI-DSS" in fw_names
        assert "SOC 2" in fw_names

    @pytest.mark.asyncio
    async def test_deterministic_output(self):
        """Same inputs produce identical results across runs (excluding timestamp)."""
        r1 = await verify_compliance_drift.execute({})
        r2 = await verify_compliance_drift.execute({})
        r1.pop("analyzed_at", None)
        r2.pop("analyzed_at", None)
        assert r1 == r2