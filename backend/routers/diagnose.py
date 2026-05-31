"""Incident diagnosis endpoint."""

from __future__ import annotations

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.models.schemas import DiagnoseRequest
from backend.services.coral_service import get_incident_diagnosis_sql, run_coral_query
from backend.services.local_sre_service import stream_diagnosis

router = APIRouter()


@router.post("")
async def diagnose_incident(request: DiagnoseRequest) -> StreamingResponse:
    """Run a Coral JOIN query, then stream an SRE diagnosis."""
    sql = get_incident_diagnosis_sql(request.time_window_hours)
    coral_result = run_coral_query(sql, demo_mode=request.demo_mode)

    async def generate():
        yield f"data: {json.dumps({'type': 'sql', 'sql': sql})}\n\n"
        yield f"data: {json.dumps({'type': 'coral_result', 'data': coral_result})}\n\n"
        async for chunk in stream_diagnosis(coral_result, request.question):
            yield f"data: {json.dumps({'type': 'diagnosis', 'text': chunk})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
