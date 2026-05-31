# CoralOps Hackathon Checklist

This checklist is based on the official WeMakeDevs Pirates of the Coral-bean pages reviewed on May 24, 2026.

## Eligibility

- Star the Coral GitHub repository.
- Join the Coral Discord.
- Keep the crew size between 1 and 4 members.
- Treat Coral as the core data retrieval layer, not a minor add-on.
- Build the final submission during the hackathon period.

## Product Requirements

- Track: Enterprise Agent.
- Project: CoralOps, an AI SRE agent for incident diagnosis.
- Core Coral use: GitHub + Sentry + Slack cross-source SQL joins.
- Demo mode: reliable fallback data for judges and recording.
- Real mode: `CORAL_AVAILABLE=true` and Coral CLI configured locally.
- AI-style layer: free local deterministic SRE diagnosis and postmortem streaming.
- Evidence timeline: GitHub PR merge, Sentry first seen, Slack context, and time-to-incident are shown visually.
- Readiness panel: app exposes demo/live/manual submission status from `/readiness`.
- Postmortem export: generated markdown can be downloaded from the dashboard.
- Source spec bounty: PagerDuty connector draft in `coral/sources/pagerduty.yaml`.

## Submission Assets

- Public GitHub repository.
- Deployed frontend URL.
- Deployed backend URL or demo backend path.
- YouTube demo video, maximum 3 minutes.
- README with setup, architecture, Coral usage, and demo script.
- Screenshots for Discord/social showcase.

## Judging Alignment

- Potential Impact: reduces SRE incident investigation time.
- Creativity: turns operational context into one joined query and one guided workflow.
- Learning & Growth: documents migration from PulseOps mocks to Coral-powered data retrieval.
- Technical Implementation: FastAPI, Next.js, Coral SQL, SSE streaming, free local SRE analysis.
- Aesthetics & UX: polished dark editorial interface with a focused incident workflow.
- Best Use of Coral: highlights SQL interface, cross-source joins, local execution, and source spec expansion.

## Demo Flow

1. Open the dashboard.
2. Select `INC-001`.
3. Click `Diagnose`.
4. Show the Coral SQL query.
5. Show the evidence timeline built from the Coral result.
6. Show the streamed root cause, timeline, blast radius, fix, and prevention.
7. Click `Postmortem`.
8. Show the generated markdown incident report.
9. Download the markdown report.
10. Explain that PulseOps needed mock Python telemetry, while CoralOps uses one Coral SQL layer.
