"""Coral SQL execution with a reliable demo-mode fallback."""

from __future__ import annotations

import json
import os
import subprocess
from typing import Any


DEMO_RESULT: dict[str, Any] = {
    "incident_diagnosis": [
        {
            "pr_title": "feat: optimize database connection pooling",
            "pr_merged_at": "2026-05-20T14:32:00Z",
            "pr_author": "dev-team",
            "sentry_error": "OperationalError: too many connections",
            "sentry_first_seen": "2026-05-20T14:47:00Z",
            "sentry_count": 847,
            "slack_message": "INCIDENT: API response times spiking 400%",
            "slack_channel": "#incidents",
            "time_to_incident_minutes": 15,
        }
    ]
}


def should_use_demo(demo_mode: bool = False) -> bool:
    """Return whether API calls should use deterministic demo data."""
    env_demo = os.getenv("DEMO_MODE", "true").lower() == "true"
    env_coral = os.getenv("CORAL_AVAILABLE", "false").lower() == "true"
    return demo_mode or env_demo or not env_coral


def run_coral_query(sql: str, timeout: int = 30, demo_mode: bool = False) -> dict[str, Any]:
    """Execute a Coral SQL query and fall back to demo data when unavailable."""
    if should_use_demo(demo_mode):
        return DEMO_RESULT

    try:
        result = subprocess.run(
            ["coral", "sql", "--format", "json", sql],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return DEMO_RESULT

    if result.returncode != 0:
        return DEMO_RESULT

    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError:
        return DEMO_RESULT

    return parsed if isinstance(parsed, dict) else {"rows": parsed}


def get_incident_diagnosis_sql(time_window_hours: int = 24) -> str:
    channel = os.getenv("SLACK_CHANNEL", "#incidents")
    return f"""
SELECT
    g.title AS pr_title,
    g.merged_at AS pr_merged_at,
    g.user_login AS pr_author,
    s.message AS sentry_error,
    s.first_seen AS sentry_first_seen,
    s.times_seen AS sentry_count,
    sl.text AS slack_message,
    sl.channel AS slack_channel,
    ROUND((EXTRACT(EPOCH FROM (s.first_seen - g.merged_at)) / 60)::numeric, 1)
        AS time_to_incident_minutes
FROM github.pull_requests g
JOIN sentry.issues s
    ON s.first_seen >= g.merged_at
    AND s.first_seen <= g.merged_at + INTERVAL '{time_window_hours} hours'
JOIN slack.messages sl
    ON sl.timestamp >= g.merged_at
    AND sl.channel = '{channel}'
WHERE s.level IN ('fatal', 'error')
    AND g.merged_at >= NOW() - INTERVAL '{time_window_hours} hours'
ORDER BY s.first_seen DESC
LIMIT 20;
""".strip()


def get_sprint_health_sql() -> str:
    return """
SELECT
    g.title AS pr_title,
    g.state AS pr_state,
    g.user_login AS author,
    g.created_at,
    g.merged_at,
    COUNT(g.id) OVER() AS total_prs,
    SUM(CASE WHEN g.state = 'open' THEN 1 ELSE 0 END) OVER() AS open_prs
FROM github.pull_requests g
WHERE g.created_at >= NOW() - INTERVAL '7 days'
ORDER BY g.created_at DESC
LIMIT 50;
""".strip()


def get_service_status_sql() -> str:
    return """
SELECT
    'sentry' AS source,
    level AS severity,
    COUNT(*) AS error_count,
    MAX(last_seen) AS last_occurrence
FROM sentry.issues
WHERE last_seen >= NOW() - INTERVAL '1 hour'
GROUP BY level
ORDER BY error_count DESC;
""".strip()
