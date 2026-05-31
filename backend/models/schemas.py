"""API schemas for CoralOps."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class DiagnoseRequest(BaseModel):
    question: str = Field(..., min_length=3)
    time_window_hours: int = Field(default=24, ge=1, le=168)
    demo_mode: bool = False


class QueryRequest(BaseModel):
    natural_language: str = Field(..., min_length=3)
    demo_mode: bool = False


class PostmortemRequest(BaseModel):
    incident_id: str = Field(..., min_length=3)
    coral_data: dict[str, Any]
    demo_mode: bool = False


class Incident(BaseModel):
    id: str
    title: str
    severity: Literal["fatal", "error", "warning", "info"]
    source: Literal["sentry", "github", "slack", "pagerduty"]
    timestamp: str
    related_pr: str | None = None
    related_slack: str | None = None
    status: Literal["open", "investigating", "resolved"]
    error_count: int = 0
    time_to_incident_minutes: int | None = None


class DiagnoseResponse(BaseModel):
    coral_sql: str
    coral_result: dict[str, Any]
    diagnosis: str
    confidence: float
