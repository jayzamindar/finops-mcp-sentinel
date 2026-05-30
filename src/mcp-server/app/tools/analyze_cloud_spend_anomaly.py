# ============================================================
# FinOps-SRE Sentinel — Tool: Analyze Cloud Spend Anomaly
# ============================================================
# Generated based: [Arch_Section_03], [URD_Section_03.1.2]
# Target Path: src/mcp-server/app/tools/analyze_cloud_spend_anomaly.py
# ============================================================

from __future__ import annotations

import hashlib
import random
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

DESCRIPTION = "Detect and analyze unexpected cloud cost spikes with forecasting."

# ---------------------------------------------------------------------------
# Mock data seed — deterministic for demo reproducibility
# ---------------------------------------------------------------------------
_SEED = int(hashlib.sha256(b"finops-cost-anomaly").hexdigest()[:8], 16)

# Realistic AWS-style service cost breakdown
_SERVICES = [
    {"service": "Amazon EC2", "baseline_usd": 18_200, "category": "Compute"},
    {"service": "Amazon RDS", "baseline_usd": 8_400, "category": "Database"},
    {"service": "Amazon S3", "baseline_usd": 3_100, "category": "Storage"},
    {"service": "Amazon CloudFront", "baseline_usd": 2_800, "category": "CDN"},
    {"service": "Amazon EKS", "baseline_usd": 5_600, "category": "Kubernetes"},
    {"service": "Amazon ElastiCache", "baseline_usd": 2_200, "category": "Cache"},
    {"service": "AWS Lambda", "baseline_usd": 1_900, "category": "Serverless"},
    {"service": "Amazon CloudWatch", "baseline_usd": 900, "category": "Monitoring"},
    {"service": "AWS NAT Gateway", "baseline_usd": 1_400, "category": "Networking"},
    {"service": "Amazon SQS/SNS", "baseline_usd": 500, "category": "Messaging"},
]


async def execute(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Analyze cloud spend anomalies.

    Input Schema (URD Section 3.1.2):
        time_range: {start: ISO8601, end: ISO8601}
        namespace: str
        cost_threshold_percent: int
        include_forecasts: bool
    """
    logger.info("analyze_cloud_spend_anomaly_called", input=input_data)

    rng = random.Random(_SEED)
    namespace = input_data.get("namespace", "production")
    threshold = input_data.get("cost_threshold_percent", 20)
    include_forecasts = input_data.get("include_forecasts", True)

    # Simulate a 50.7% cost spike driven by EC2 + RDS scaling events
    anomaly_multiplier = 1.507
    top_charges = []
    total_baseline = 0
    total_current = 0

    for svc in _SERVICES:
        base = svc["baseline_usd"]
        # EC2 and RDS are the anomaly sources
        if svc["service"] in ("Amazon EC2", "Amazon RDS"):
            current = int(base * anomaly_multiplier * (1 + rng.uniform(-0.03, 0.03)))
        else:
            current = int(base * (1 + rng.uniform(-0.05, 0.08)))
        delta = current - base
        pct = round((delta / base) * 100, 1)
        total_baseline += base
        total_current += current
        top_charges.append({
            "service": svc["service"],
            "category": svc["category"],
            "baseline_usd": base,
            "current_usd": current,
            "delta_usd": delta,
            "change_percent": pct,
        })

    top_charges.sort(key=lambda c: abs(c["delta_usd"]), reverse=True)
    anomaly_pct = round(((total_current - total_baseline) / total_baseline) * 100, 1)

    result: dict[str, Any] = {
        "baseline_monthly_cost_usd": total_baseline,
        "current_monthly_cost_usd": total_current,
        "anomaly_detected": anomaly_pct >= threshold,
        "anomaly_percent": anomaly_pct,
        "top_charges": top_charges[:5],
        "recommendations": [
            "Right-size EC2 instances — 12 x m5.2xlarge running at <30% CPU utilization detected in us-east-1",
            "Enable RDS auto-scaling with scheduled scaling for peak hours (08:00-20:00 EST)",
            "Migrate infrequently accessed S3 objects to Glacier — estimated savings: $840/month",
            "Review NAT Gateway data transfer — 2.1TB cross-AZ traffic can be reduced with VPC endpoints",
            "Consider Reserved Instances for steady-state EC2/RDS workloads — 40% savings over 1-year term",
        ],
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "namespace": namespace,
    }

    if include_forecasts:
        forecast_usd = int(total_current * (1 + rng.uniform(0.02, 0.08)))
        result["forecast_month_end_usd"] = forecast_usd
        result["forecast_confidence"] = "medium"
        result["forecast_note"] = "Based on 10-day trailing average with seasonal adjustment"

    return result