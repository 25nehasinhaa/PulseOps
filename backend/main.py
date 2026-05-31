"""FastAPI entrypoint for the CoralOps backend."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import diagnose, incidents, postmortem, query, readiness

load_dotenv()

app = FastAPI(
    title="CoralOps API",
    description="AI-powered SRE agent backed by Coral SQL and PulseOps demo telemetry.",
    version="0.1.0",
)

frontend_origins = {
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://frontend-gold-gamma-85.vercel.app",
}

extra_frontend_origin = os.getenv("FRONTEND_ORIGIN")
if extra_frontend_origin:
    frontend_origins.add(extra_frontend_origin.rstrip("/"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=sorted(frontend_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnose.router, prefix="/diagnose", tags=["diagnose"])
app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
app.include_router(postmortem.router, prefix="/postmortem", tags=["postmortem"])
app.include_router(readiness.router, prefix="/readiness", tags=["readiness"])


@app.get("/health")
async def health() -> dict[str, str | bool]:
    """Return service health and current integration mode."""
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
    coral_available = os.getenv("CORAL_AVAILABLE", "false").lower() == "true"
    return {
        "status": "ok",
        "demo_mode": demo_mode,
        "coral_available": coral_available,
    }
