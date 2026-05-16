"""Data quality checks for the PulseOps telemetry pipeline."""

from __future__ import annotations

from typing import Any


def run_quality_checks(events: list[dict[str, Any]]) -> dict[str, int | float]:
    """Return compact quality metrics for dashboard and logs."""
    total = len(events)
    valid = sum(1 for event in events if event.get("is_valid"))
    event_ids = [event.get("event_id") for event in events]
    duplicates = total - len(set(event_ids))
    return {
        "total_events": total,
        "valid_events": valid,
        "invalid_events": total - valid,
        "duplicate_events": duplicates,
        "validation_pass_rate": round((valid / total) * 100, 2) if total else 0.0,
    }
