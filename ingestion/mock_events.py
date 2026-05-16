"""Mock operational telemetry generation for PulseOps."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any


def _iso(minutes_ago: int) -> str:
    return (datetime.now(timezone.utc) - timedelta(minutes=minutes_ago)).isoformat(timespec="seconds")


def generate_mock_events() -> list[dict[str, Any]]:
    """Generate representative operational events from several production sources."""
    return [
        {
            "event_id": "EVT-001",
            "source": "github",
            "timestamp": _iso(22),
            "event_type": "deployment",
            "status": "SUCCESS",
            "repo": "checkout",
            "environment": "production",
            "description": "Deployment pushed to production",
            "actor": "release-bot",
        },
        {
            "event_id": "EVT-002",
            "source": "sentry",
            "timestamp": _iso(14),
            "event_type": "application_error",
            "status": "CRITICAL",
            "service": "checkout",
            "error_count": 47,
            "description": "Error rate spike detected",
            "actor": "sentry-monitor",
        },
        {
            "event_id": "EVT-003",
            "source": "pagerduty",
            "timestamp": _iso(13),
            "event_type": "incident",
            "status": "OPEN",
            "service": "checkout",
            "severity": "CRITICAL",
            "description": "Critical incident triggered",
            "actor": "pagerduty",
        },
        {
            "event_id": "EVT-004",
            "source": "github",
            "timestamp": _iso(39),
            "event_type": "deployment",
            "status": "SUCCESS",
            "repo": "user-auth",
            "environment": "production",
            "description": "Auth service deployment completed",
            "actor": "release-bot",
        },
        {
            "event_id": "EVT-005",
            "source": "pagerduty",
            "timestamp": _iso(31),
            "event_type": "service_alert",
            "status": "WARNING",
            "service": "user-auth",
            "severity": "HIGH",
            "description": "Application errors detected post-deploy",
            "actor": "pagerduty",
        },
        {
            "event_id": "EVT-006",
            "source": "sentry",
            "timestamp": _iso(27),
            "event_type": "application_error",
            "status": "WARNING",
            "service": "user-auth",
            "error_count": 18,
            "description": "Authentication timeout spike",
            "actor": "sentry-monitor",
        },
        {
            "event_id": "EVT-007",
            "source": "github",
            "timestamp": _iso(63),
            "event_type": "deployment",
            "status": "SUCCESS",
            "repo": "payment-api",
            "environment": "production",
            "description": "Payment API rollout completed",
            "actor": "release-bot",
        },
        {
            "event_id": "EVT-008",
            "source": "service_alert",
            "timestamp": _iso(51),
            "event_type": "latency",
            "status": "RESOLVED",
            "service": "payment-api",
            "severity": "MEDIUM",
            "description": "P95 latency returned to baseline",
            "actor": "cloudwatch",
        },
        {
            "event_id": "EVT-009",
            "source": "service_alert",
            "timestamp": _iso(8),
            "event_type": "heartbeat",
            "status": "SUCCESS",
            "service": "data-pipeline",
            "severity": "LOW",
            "description": "SQS to Lambda to S3 pipeline healthy",
            "actor": "pipeline-health",
        },
    ]
