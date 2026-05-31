# CoralOps

CoralOps is an incident command room for teams that need answers before the trail goes cold.

It takes the messy part of outage response, where someone is jumping between GitHub, Sentry, Slack, and a half written incident doc, and turns it into one calm workflow. Pick an incident. Run the Coral SQL diagnosis. Watch the evidence line up. Generate the postmortem while the context is still fresh.

Built for the WeMakeDevs Coral Enterprise Agent Hackathon.

## Live Links

1. Live app: https://frontend-gold-gamma-85.vercel.app
2. Dashboard: https://frontend-gold-gamma-85.vercel.app/dashboard
3. Backend API: https://api-production-4e7b.up.railway.app
4. API health: https://api-production-4e7b.up.railway.app/health
5. GitHub repo: https://github.com/25nehasinhaa/PulseOps

## Why I Built It

Incident response is rarely blocked by a lack of data. It is blocked by scattered data.

The deploy is in GitHub. The error spike is in Sentry. The first human signal is in Slack. The report is in a blank document. CoralOps uses Coral shaped SQL to bring those signals into one investigation flow, then turns the joined evidence into a practical SRE diagnosis and a clean postmortem.

The goal is simple: less tab switching, fewer guesses, better incident memory.

## What Judges Should Try

1. Open the dashboard.
2. Select the active Sentry incident.
3. Click Diagnose.
4. Watch CoralOps stream the suspected root cause, blast radius, and fix path.
5. Review the Coral SQL and evidence timeline.
6. Click Postmortem.
7. Download the generated incident report.
8. Open the readiness panel to see the hackathon checks.

## What Makes It Coral Native

CoralOps treats Coral SQL as the investigation layer, not as a decorative add on.

The core query joins GitHub pull requests, Sentry issues, and Slack messages into one evidence set. The diagnosis, timeline, and postmortem all come from that joined result. A PagerDuty source draft is included to show how the project can move from demo data to a deeper Coral source path.

## Product Highlights

1. Incident queue with severity, event count, deployment context, and current status.
2. Streamed SRE diagnosis with root cause, impact, confidence, and next actions.
3. Coral SQL viewer so the evidence path is visible to judges.
4. Evidence timeline that connects deploys, error spikes, Slack context, and response status.
5. One click postmortem generation with download support.
6. Readiness panel mapped to the hackathon submission needs.
7. Free mode with no paid AI API requirement.

## Tech Stack

1. Next.js and TypeScript for the frontend.
2. FastAPI for the backend.
3. Server sent events for streamed diagnosis and report generation.
4. Coral SQL patterns for operational joins.
5. Local SRE engine for free and reliable judging demos.
6. Railway for the API deployment.
7. Vercel for the frontend deployment.

## Project Map

```text
analytics        Original PulseOps correlation logic
backend          FastAPI API for incidents, diagnosis, queries, reports, readiness
coral            Coral source draft and SQL direction
dashboard        Earlier Streamlit prototype
data             Demo operational events
docs             Demo script, submission copy, free mode notes, deployment guide
frontend         Next.js CoralOps experience
ingestion        Mock operational event generation
processor        Event normalisation and validation
```

## Run Locally

Backend:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8010
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Local URLs:

```text
http://127.0.0.1:8010/health
http://127.0.0.1:8010/docs
http://localhost:3000
http://localhost:3000/dashboard
```

## Environment

Backend:

```text
DEMO_MODE=true
CORAL_AVAILABLE=false
SLACK_CHANNEL=#incidents
FREE_SUBMISSION_MODE=true
FRONTEND_ORIGIN=https://frontend-gold-gamma-85.vercel.app
```

Frontend:

```text
NEXT_PUBLIC_API_URL=https://api-production-4e7b.up.railway.app
NEXT_PUBLIC_DEMO_MODE=true
```

## Demo Line

CoralOps is an AI SRE control room that uses Coral SQL patterns to join operational signals and turn an outage trail into a diagnosis, timeline, and postmortem in one workflow.

## Repository Description

CoralOps turns GitHub, Sentry, and Slack incident signals into a Coral SQL powered SRE diagnosis, evidence timeline, and postmortem workflow.
