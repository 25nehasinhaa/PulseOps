# PulseOps / CoralOps

PulseOps started as an AI-powered operational intelligence dashboard that simulates how engineering teams monitor production systems, detect incidents, correlate telemetry, and generate operational recommendations.

The hackathon direction is **CoralOps**: an AI SRE agent that uses Coral SQL to join GitHub pull requests, Sentry errors, and Slack incident messages, then streams an SRE-style diagnosis and generates incident postmortems.

Current MVP flow:

1. Select an incident.
2. Run a Coral SQL-backed diagnosis.
3. Stream the AI SRE analysis.
4. Inspect the deployment-to-incident evidence timeline.
5. Generate a markdown postmortem.
6. Download the postmortem file.

## Architecture

The project currently has two working surfaces:

- `ingestion/mock_events.py` generates mock GitHub, PagerDuty, Sentry, and service alert telemetry.
- `processor/normaliser.py` converts source-specific payloads into a canonical event schema.
- `processor/validate_event.py` validates required fields.
- `analytics/correlation_engine.py` detects deployment-to-incident relationships and generates AI-style recommendations.
- `analytics/quality_checks.py` reports validation and duplicate metrics.
- `dashboard/app.py` runs the Streamlit dashboard and persists JSON outputs.
- `backend/main.py` exposes the new FastAPI API for CoralOps.
- `backend/services/coral_service.py` runs Coral SQL when configured and falls back to realistic demo data.
- `backend/services/local_sre_service.py` streams free local diagnosis and postmortem text without paid AI APIs.
- `frontend/app/page.tsx` runs the Next.js CoralOps landing page.
- `frontend/app/dashboard/page.tsx` runs the interactive AI SRE dashboard against the FastAPI API.

## Folder Structure

```text
PulseOps/
|-- analytics/
|-- backend/
|   |-- main.py
|   |-- models/
|   |-- queries/
|   |-- routers/
|   `-- services/
|-- coral/
|   `-- sources/
|-- dashboard/
|-- data/
|-- frontend/
|   |-- app/
|   |-- components/
|   |-- hooks/
|   `-- lib/
|-- ingestion/
|-- processor/
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Install

```bash
pip install -r requirements.txt
```

## Run Streamlit Dashboard

```bash
streamlit run dashboard/app.py
```

The app writes the generated datasets to:

- `data/processed/processed_events.json`
- `data/processed/correlation_insights.json`

## Run CoralOps API

```bash
uvicorn backend.main:app --reload --port 8000
```

Useful endpoints:

- `GET /health`
- `GET /incidents`
- `POST /diagnose`
- `POST /query`
- `POST /postmortem`
- `GET /readiness`

Copy `backend/.env.example` to `backend/.env` when you are ready to use real credentials:

```text
DEMO_MODE=true
CORAL_AVAILABLE=false
SLACK_CHANNEL=#incidents
FREE_SUBMISSION_MODE=true
```

Keep `DEMO_MODE=true` for reliable hackathon demos before Coral sources are connected.

## Run CoralOps Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend defaults to `http://127.0.0.1:8010` for the API. To change it, create `frontend/.env.local`:

```text
NEXT_PUBLIC_API_URL=http://127.0.0.1:8010
NEXT_PUBLIC_DEMO_MODE=true
```

Open:

- `http://localhost:3000`
- `http://localhost:3000/dashboard`

## Visual Direction

The frontend uses the attached Green Velvet palette:

- Green Velvet: `#29281E`
- Golden Sandlewood: `#857861`
- Almond Light: `#E7D4BB`
- Plum Wine: `#48252F`
- Carbon Powder: `#101211`

The goal is a classy AI operations workspace inspired by a black editorial gallery layout: quiet surfaces, premium serif headings in upright type, subtle borders, and high-contrast operational content.

## Deployment Files

- `backend/Procfile` and `backend/railway.toml` are ready for Railway backend deployment.
- `frontend/vercel.json` is ready for Vercel frontend deployment.
- `coral/sources/pagerduty.yaml` is the first custom Coral source spec draft for the PagerDuty bounty path.

## Hackathon Package

- `docs/HACKATHON_CHECKLIST.md` maps the build to the official hackathon rules and judging criteria.
- `docs/DEMO_SCRIPT.md` provides a 2.5 minute demo script.
- `docs/DEPLOYMENT.md` provides Railway and Vercel deployment steps.
- `docs/FREE_SUBMISSION.md` explains how to submit using free tools only.
- `docs/SUBMISSION_COPY.md` contains paste-ready hackathon submission text.

## Hackathon Demo Hook

"I built PulseOps: a DevOps dashboard with Python-generated GitHub, PagerDuty, and Sentry data. Then I found Coral. CoralOps replaces the mocked correlation layer with Coral SQL joins across operational sources, then uses a free local SRE engine to diagnose root cause and generate a postmortem."
