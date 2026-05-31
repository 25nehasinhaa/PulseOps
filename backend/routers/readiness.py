"""Submission and runtime readiness endpoint."""

from __future__ import annotations

import os

from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_readiness() -> dict[str, object]:
    """Return runtime and hackathon submission readiness signals."""
    demo_mode = os.getenv("DEMO_MODE", "true").lower() == "true"
    coral_available = os.getenv("CORAL_AVAILABLE", "false").lower() == "true"

    checks = [
        {
            "id": "frontend",
            "label": "Next.js frontend",
            "status": "ready",
            "detail": "Landing page and dashboard are implemented.",
        },
        {
            "id": "backend",
            "label": "FastAPI backend",
            "status": "ready",
            "detail": "Health, incidents, diagnosis, query, postmortem, and readiness APIs are available.",
        },
        {
            "id": "coral",
            "label": "Coral CLI",
            "status": "ready" if coral_available else "demo",
            "detail": "Live Coral mode is enabled." if coral_available else "Demo mode uses realistic Coral-shaped fallback data.",
        },
        {
            "id": "local_sre",
            "label": "Free local SRE analysis",
            "status": "ready",
            "detail": "No paid AI key is required; deterministic streaming analysis is active.",
        },
        {
            "id": "deployment",
            "label": "Deployment config",
            "status": "ready",
            "detail": "Railway, Vercel, and environment examples are included.",
        },
        {
            "id": "submission",
            "label": "Submission assets",
            "status": "manual",
            "detail": "GitHub repo, deployed links, YouTube demo, Discord join, and Coral star are manual steps.",
        },
    ]

    return {
        "project": "CoralOps",
        "demo_mode": demo_mode,
        "coral_available": coral_available,
        "free_submission_mode": True,
        "checks": checks,
    }
