"""Incident correlation and AI insight generation for PulseOps."""

from __future__ import annotations

from datetime import datetime
from typing import Any


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _severity_rank(severity: str) -> int:
    return {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}.get(severity.upper(), 1)


def correlate_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Detect deployment impact chains across normalized operational events."""
    valid_events = [event for event in events if event.get("is_valid", True)]
    deployments = [event for event in valid_events if event["event_type"] == "deployment"]
    correlations: list[dict[str, Any]] = []

    for deployment in deployments:
        service = deployment["affected_service"]
        deployed_at = _parse_timestamp(deployment["timestamp"])
        related = []
        for event in valid_events:
            if event["event_id"] == deployment["event_id"]:
                continue
            if event["affected_service"] != service:
                continue
            delta_minutes = (_parse_timestamp(event["timestamp"]) - deployed_at).total_seconds() / 60
            if 0 <= delta_minutes <= 45 and event["status"] in {"WARNING", "CRITICAL", "OPEN"}:
                related.append(event)

        if related:
            highest = max(related, key=lambda item: _severity_rank(str(item.get("severity", "LOW"))))
            severity = "CRITICAL" if highest["status"] == "CRITICAL" else str(highest.get("severity", "HIGH")).upper()
            confidence = min(94, 58 + (len(related) * 18))
            correlations.append(
                {
                    "correlation_id": f"CORR-{deployment['event_id'].split('-')[-1]}",
                    "deployment_event": deployment["event_id"],
                    "affected_service": service,
                    "incident_type": "deployment impact",
                    "severity": severity if severity != "LOW" else "HIGH",
                    "confidence": confidence,
                    "related_event_ids": [event["event_id"] for event in related],
                    "summary": (
                        f"{deployment['event_id']} preceded {len(related)} instability signal"
                        f"{'s' if len(related) != 1 else ''} for {service}."
                    ),
                }
            )

    return correlations


def generate_ai_insights(correlations: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Generate deterministic AI-style operational recommendations."""
    insights: list[dict[str, str]] = []
    for correlation in correlations:
        severity = str(correlation["severity"]).upper()
        service = correlation["affected_service"]
        if severity in {"CRITICAL", "HIGH"}:
            insight = "Recent deployment activity may have contributed to instability."
            action = "Review deployment logs, validate rollback readiness, and monitor error rates for ten minutes."
        else:
            insight = "A weaker deployment-to-signal relationship was detected."
            action = "Keep the service on an elevated watch window and compare with baseline telemetry."
        insights.append(
            {
                "priority": "HIGH" if severity == "CRITICAL" else severity,
                "service": service,
                "insight": insight,
                "recommended_action": action,
                "correlation_id": correlation["correlation_id"],
            }
        )
    return insights
