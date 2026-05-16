"""Schema validation for normalized operational events."""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = {"event_id", "source", "timestamp", "event_type", "affected_service"}


def validate_event(event: dict[str, Any]) -> bool:
    """Return True when an event contains all required fields with truthy values."""
    return all(event.get(field) for field in REQUIRED_FIELDS)


def validate_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Attach validation results while preserving the event payload."""
    validated: list[dict[str, Any]] = []
    for event in events:
        enriched = dict(event)
        enriched["is_valid"] = validate_event(enriched)
        validated.append(enriched)
    return validated
