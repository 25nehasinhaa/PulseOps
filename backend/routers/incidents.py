"""Incident listing endpoint."""

from __future__ import annotations

from fastapi import APIRouter

from backend.services.coral_service import get_service_status_sql, run_coral_query
from backend.services.demo_service import get_demo_incidents

router = APIRouter()


@router.get("")
async def get_incidents() -> dict[str, object]:
    """Fetch current incidents and source metrics."""
    sql = get_service_status_sql()
    coral_data = run_coral_query(sql)
    return {
        "incidents": get_demo_incidents(),
        "coral_sql": sql,
        "coral_metrics": coral_data,
        "sources_connected": ["github", "sentry", "slack"],
    }
