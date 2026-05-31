"""Realistic fallback data for hackathon demos."""

from __future__ import annotations

from typing import Any


def get_demo_incidents() -> list[dict[str, Any]]:
    """Return stable incident data for the frontend and API demos."""
    return [
        {
            "id": "INC-001",
            "title": "Fatal: OperationalError - too many DB connections",
            "severity": "fatal",
            "source": "sentry",
            "timestamp": "2026-05-20T14:47:00Z",
            "related_pr": "feat: optimize database connection pooling",
            "related_slack": "INCIDENT: API response times spiking 400%",
            "status": "investigating",
            "error_count": 847,
            "time_to_incident_minutes": 15,
        },
        {
            "id": "INC-002",
            "title": "Error: Unhandled TypeError in payment service",
            "severity": "error",
            "source": "sentry",
            "timestamp": "2026-05-20T11:22:00Z",
            "related_pr": "refactor: payment service middleware",
            "related_slack": "Payment service throwing 500s",
            "status": "resolved",
            "error_count": 124,
            "time_to_incident_minutes": 8,
        },
        {
            "id": "INC-003",
            "title": "Warning: Memory usage above 85% on prod cluster",
            "severity": "warning",
            "source": "github",
            "timestamp": "2026-05-19T09:15:00Z",
            "related_pr": "feat: add image processing pipeline",
            "related_slack": None,
            "status": "resolved",
            "error_count": 0,
            "time_to_incident_minutes": 42,
        },
    ]
