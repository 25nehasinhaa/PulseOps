"""Postmortem generation endpoint."""

from __future__ import annotations

import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.models.schemas import PostmortemRequest
from backend.services.local_sre_service import stream_postmortem

router = APIRouter()


@router.post("")
async def generate_postmortem(request: PostmortemRequest) -> StreamingResponse:
    """Generate a Markdown incident postmortem."""

    async def generate():
        async for chunk in stream_postmortem(request.coral_data, request.incident_id):
            yield f"data: {json.dumps({'type': 'text', 'chunk': chunk})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
