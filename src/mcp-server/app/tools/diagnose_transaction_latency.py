# ============================================================
# FinOps-SRE Sentinel — Tool: Diagnose Transaction Latency
# ============================================================
# Generated based: [Arch_Section_03], [URD_Section_03.1.1]
# Target Path: src/mcp-server/app/tools/diagnose_transaction_latency.py
# ============================================================

from __future__ import annotations

import hashlib
import random
from datetime import datetime, timezone
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

DESCRIPTION = "Query payment/transaction logs to identify latency patterns and root causes."

# ---------------------------------------------------------------------------
# Mock data seed — deterministic for demo reproducibility
# ---------------------------------------------------------------------------
_SEED = int(hashlib.sha256(b"finops-txn-latency").hexdigest()[:8], 16)

_ROOT_CAUSES = [
    {
        "cause": "database_connection_pool_exhaustion",
        "description": "PostgreSQL connection pool saturated — 50/50 connections in use",
        "recommendation": "Increase max_connections from 50 to 100 or add PgBouncer connection pooler",
        "severity": "high",
        "service": "payment-gateway",
        "latency_range_ms": (1800, 3200),
    },
    {
        "cause": "redis_cache_miss_storm",
        "description": "Redis cache eviction causing thundering herd on downstream services",
        "recommendation": "Implement cache-aside pattern with jittered TTLs (300s ± 60s)",
        "severity": "medium",
        "service": "payment-gateway",
        "latency_range_ms": (900, 1600),
    },
    {
        "cause": "gc_pause_sustained",
        "description": "JVM garbage collection pause exceeding 2s in fraud-detection service",
        "recommendation": "Switch to ZGC or increase heap size from 4GB to 8GB",
        "severity": "medium",
        "service": "fraud-detection",
        "latency_range_ms": (2000, 4500),
    },
    {
        "cause": "external_api_timeout",
        "description": "KYC provider (Plaid) responding in 3-5s, exceeding 2s SLA",
        "recommendation": "Implement circuit breaker with 3s timeout and fallback to cached results",
        "severity": "high",
        "service": "kyc-verification",
        "latency_range_ms": (3000, 5000),
    },
    {
        "cause": "kafka_consumer_lag",
        "description": "Transaction event processing lagging by 12,000 messages",
        "recommendation": "Scale consumer group from 3 to 8 partitions and add 2 consumer instances",
        "severity": "critical",
        "service": "event-processor",
        "latency_range_ms": (5000, 12000),
    },
]


def _generate_trace_id(rng: random.Random) -> str:
    return f"txn_{hashlib.md5(rng.randbytes(8)).hexdigest()[:12]}"


async def execute(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Diagnose transaction latency.

    Input Schema (URD Section 3.1.1):
        time_range: {start: ISO8601, end: ISO8601}
        service_name: str
        threshold_ms: int
        limit: int
    """
    logger.info("diagnose_transaction_latency_called", input=input_data)

    rng = random.Random(_SEED)
    service = input_data.get("service_name", "payment-gateway")
    threshold_ms = input_data.get("threshold_ms", 500)
    limit = input_data.get("limit", 100)

    # Generate realistic latency distribution
    # Normal transactions: 45-250ms (95% of traffic)
    # Elevated: 250-500ms (4%)
    # Slow: >500ms (1%)
    total_traces = 1547
    normal_count = int(total_traces * 0.95)
    elevated_count = int(total_traces * 0.04)
    slow_count = total_traces - normal_count - elevated_count  # ~23

    # Generate slow trace details
    slow_traces = []
    now = datetime.now(timezone.utc)
    for i in range(min(slow_count, limit)):
        cause = rng.choice(_ROOT_CAUSES)
        latency = rng.randint(*cause["latency_range_ms"])
        timestamp = now.replace(
            hour=rng.randint(0, 23),
            minute=rng.randint(0, 59),
            second=rng.randint(0, 59),
        )
        slow_traces.append({
            "trace_id": _generate_trace_id(rng),
            "timestamp": timestamp.isoformat(),
            "latency_ms": latency,
            "service": cause["service"],
            "root_cause": cause["cause"],
            "root_cause_description": cause["description"],
            "recommendation": cause["recommendation"],
            "severity": cause["severity"],
        })

    slow_traces.sort(key=lambda t: t["latency_ms"], reverse=True)

    # Calculate percentiles from a simulated distribution
    p50 = rng.randint(62, 78)
    p95 = rng.randint(210, 260)
    p99 = rng.randint(850, 980)

    # Group by root cause for summary
    cause_summary: dict[str, int] = {}
    for trace in slow_traces:
        rc = trace["root_cause"]
        cause_summary[rc] = cause_summary.get(rc, 0) + 1

    root_cause_breakdown = [
        {"root_cause": cause, "count": count, "percent": round(count / len(slow_traces) * 100, 1)}
        for cause, count in sorted(cause_summary.items(), key=lambda x: x[1], reverse=True)
    ]

    return {
        "total_traces": total_traces,
        "slow_traces": len(slow_traces),
        "slow_traces_detail": slow_traces[:limit],
        "latency_p50_ms": p50,
        "latency_p95_ms": p95,
        "latency_p99_ms": p99,
        "threshold_ms": threshold_ms,
        "service_analyzed": service,
        "root_cause_breakdown": root_cause_breakdown,
        "summary": f"{len(slow_traces)} traces exceeded {threshold_ms}ms threshold across {len(cause_summary)} distinct root causes",
        "analyzed_at": now.isoformat(),
    }