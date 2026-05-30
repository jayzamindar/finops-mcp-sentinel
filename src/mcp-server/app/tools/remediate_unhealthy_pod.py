# ============================================================
# FinOps-SRE Sentinel — Tool: Remediate Unhealthy Pod
# ============================================================
# Generated based: [Arch_Section_03], [URD_Section_03.1.3]
# Target Path: src/mcp-server/app/tools/remediate_unhealthy_pod.py
# ============================================================

from __future__ import annotations

import hashlib
import random
from datetime import datetime, timezone
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

DESCRIPTION = "Detect and remediate unhealthy Kubernetes pods with risk-scored actions."

# ---------------------------------------------------------------------------
# Mock data seed — deterministic for demo reproducibility
# ---------------------------------------------------------------------------
_SEED = int(hashlib.sha256(b"finops-pod-remediate").hexdigest()[:8], 16)

# Realistic fintech service deployments on EKS
_SERVICES = [
    {"namespace": "payments", "deployment": "payment-gateway", "replicas": 6},
    {"namespace": "payments", "deployment": "transaction-processor", "replicas": 4},
    {"namespace": "fraud", "deployment": "fraud-detection-engine", "replicas": 3},
    {"namespace": "kyc", "deployment": "kyc-verification", "replicas": 3},
    {"namespace": "core", "deployment": "api-gateway", "replicas": 4},
    {"namespace": "core", "deployment": "auth-service", "replicas": 3},
    {"namespace": "data", "deployment": "event-processor", "replicas": 5},
    {"namespace": "data", "deployment": "analytics-pipeline", "replicas": 2},
]

_POD_FAILURE_REASONS = [
    {"reason": "CrashLoopBackOff", "exit_code": 137, "cause": "OOMKilled — container exceeded 2Gi memory limit",
     "action": "restart", "kubectl": "kubectl rollout restart deployment/{deployment} -n {namespace}"},
    {"reason": "CrashLoopBackOff", "exit_code": 1, "cause": "Application error — unhandled NullPointerException in payment validator",
     "action": "rollback", "kubectl": "kubectl rollout undo deployment/{deployment} -n {namespace}"},
    {"reason": "ImagePullBackOff", "exit_code": 0, "cause": "ECR token expired — image pull failing for 12 minutes",
     "action": "restart", "kubectl": "kubectl delete pod {pod_name} -n {namespace} --grace-period=0"},
    {"reason": "Pending", "exit_code": 0, "cause": "Insufficient CPU — cluster autoscaler at capacity (max 50 nodes reached)",
     "action": "scale", "kubectl": "kubectl scale deployment/{deployment} -n {namespace} --replicas={new_replicas}"},
    {"reason": "Evicted", "exit_code": 0, "cause": "Disk pressure on node ip-10-0-42-17 — ephemeral storage exhausted",
     "action": "restart", "kubectl": "kubectl delete pod {pod_name} -n {namespace}"},
    {"reason": "OOMKilled", "exit_code": 137, "cause": "Memory spike during fraud model inference — exceeded 4Gi limit",
     "action": "scale", "kubectl": "kubectl set resources deployment/{deployment} -n {namespace} --limits=memory=8Gi"},
]

_RISK_LEVELS = {
    "restart": {"score": 25, "label": "low", "description": "Pod restart — no data loss, brief interruption"},
    "scale": {"score": 55, "label": "medium", "description": "Horizontal scaling — safe but increases cost"},
    "rollback": {"score": 75, "label": "high", "description": "Deployment rollback — reverts to previous version"},
}


def _generate_pod_name(rng: random.Random, deployment: str) -> str:
    suffix = hashlib.md5(rng.randbytes(4)).hexdigest()[:8]
    return f"{deployment}-{suffix}"


async def execute(input_data: dict[str, Any]) -> dict[str, Any]:
    """
    Remediate unhealthy Kubernetes pods.

    Input Schema (URD Section 3.1.3):
        namespace: str (optional, defaults to all)
        auto_approve: bool (defaults to false — human-in-the-loop)
        max_risk_score: int (1-100, default 50)
    """
    logger.info("remediate_unhealthy_pod_called", input=input_data)

    rng = random.Random(_SEED)
    target_namespace = input_data.get("namespace")
    auto_approve = input_data.get("auto_approve", False)
    max_risk = input_data.get("max_risk_score", 50)

    # Generate 4-7 unhealthy pods across services
    num_issues = rng.randint(4, 7)
    unhealthy_pods = []
    now = datetime.now(timezone.utc)

    for i in range(num_issues):
        svc = rng.choice(_SERVICES)
        if target_namespace and svc["namespace"] != target_namespace:
            continue

        failure = rng.choice(_POD_FAILURE_REASONS)
        pod_name = _generate_pod_name(rng, svc["deployment"])
        action = failure["action"]
        risk = _RISK_LEVELS[action]
        new_replicas = svc["replicas"] + (1 if action == "scale" else 0)

        kubectl_cmd = failure["kubectl"].format(
            deployment=svc["deployment"],
            namespace=svc["namespace"],
            pod_name=pod_name,
            new_replicas=new_replicas,
        )

        unhealthy_pods.append({
            "pod_name": pod_name,
            "namespace": svc["namespace"],
            "deployment": svc["deployment"],
            "status": failure["reason"],
            "exit_code": failure["exit_code"],
            "cause": failure["cause"],
            "proposed_action": action,
            "risk_score": risk["score"],
            "risk_label": risk["label"],
            "risk_description": risk["description"],
            "kubectl_command": kubectl_cmd,
            "auto_executed": auto_approve and risk["score"] <= max_risk,
            "requires_approval": risk["score"] > max_risk or not auto_approve,
            "detected_at": now.isoformat(),
        })

    # Separate by approval status
    auto_executed = [p for p in unhealthy_pods if p["auto_executed"]]
    pending_approval = [p for p in unhealthy_pods if p["requires_approval"]]

    return {
        "total_unhealthy_pods": len(unhealthy_pods),
        "auto_executed": len(auto_executed),
        "pending_approval": len(pending_approval),
        "pods": unhealthy_pods,
        "actions_taken": [
            {
                "pod": p["pod_name"],
                "action": p["proposed_action"],
                "command": p["kubectl_command"],
                "status": "executed" if p["auto_executed"] else "awaiting_approval",
            }
            for p in unhealthy_pods
        ],
        "summary": (
            f"Found {len(unhealthy_pods)} unhealthy pods. "
            f"{len(auto_executed)} auto-remediated (risk ≤ {max_risk}). "
            f"{len(pending_approval)} require human approval."
        ),
        "analyzed_at": now.isoformat(),
    }