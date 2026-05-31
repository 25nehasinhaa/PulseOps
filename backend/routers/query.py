"""Natural-language query endpoint."""

from __future__ import annotations

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.models.schemas import QueryRequest
from backend.services.coral_service import run_coral_query
from backend.services.local_sre_service import natural_language_to_sql, stream_diagnosis

router = APIRouter()


@router.post("")
async def natural_language_query(request: QueryRequest) -> StreamingResponse:
    """Convert English to Coral SQL, execute it, and stream interpretation."""

    async def generate():
        yield f"data: {json.dumps({'type': 'status', 'text': 'Generating SQL query...'})}\n\n"
        sql = await natural_language_to_sql(request.natural_language)
        yield f"data: {json.dumps({'type': 'sql', 'sql': sql})}\n\n"
        yield f"data: {json.dumps({'type': 'status', 'text': 'Querying Coral sources...'})}\n\n"
        coral_result = run_coral_query(sql, demo_mode=request.demo_mode)
        yield f"data: {json.dumps({'type': 'coral_result', 'data': coral_result})}\n\n"
        async for chunk in stream_diagnosis(coral_result, request.natural_language):
            yield f"data: {json.dumps({'type': 'diagnosis', 'text': chunk})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
