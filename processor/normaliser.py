"""Normalize source-specific telemetry into the PulseOps canonical schema."""

from __future__ import annotations

from typing import Any


def _service_name(raw: str | None) -> str:
    value = (raw or "unknown").replace("_", "-").strip().lower()
    if value.endswith(" service") or value.endswith("-service") or value.endswith("-api"):
        return value
    return f"{value}-service"


def normalize_event(event: dict[str, Any]) -> dict[str, Any]:
    """Convert one source-specific event into a single operational event schema."""
    source = str(event.get("source", "")).lower()
    raw_service = event.get("affected_service")
    if source == "github":
        raw_service = event.get("repo", raw_service)
    elif source in {"pagerduty", "sentry", "service_alert"}:
        raw_service = event.get("service", raw_service)

    return {
        "event_id": event.get("event_id"),
        "source": source,
        "timestamp": event.get("timestamp"),
        "event_type": event.get("event_type"),
        "affected_service": _service_name(str(raw_service) if raw_service else None),
        "status": event.get("status", "UNKNOWN"),
        "severity": event.get("severity", "LOW"),
        "description": event.get("description", ""),
        "actor": event.get("actor", source),
        "metadata": {
            key: value
            for key, value in event.items()
            if key
            not in {
                "event_id",
                "source",
                "timestamp",
                "event_type",
                "affected_service",
                "status",
                "severity",
                "description",
                "actor",
            }
        },
    }


def normalize_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Normalize a batch of operational events."""
    return [normalize_event(event) for event in events]
