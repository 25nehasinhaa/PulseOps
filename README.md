# PulseOps

PulseOps is an AI-powered operational intelligence dashboard that simulates how engineering teams monitor production systems, detect incidents, correlate telemetry, and generate operational recommendations.

## Architecture

The project is split into ingestion, processing, analytics, and dashboard layers:

- `ingestion/mock_events.py` generates mock GitHub, PagerDuty, Sentry, and service alert telemetry.
- `processor/normaliser.py` converts source-specific payloads into a canonical event schema.
- `processor/validate_event.py` validates required fields.
- `analytics/correlation_engine.py` detects deployment-to-incident relationships and generates AI-style recommendations.
- `analytics/quality_checks.py` reports validation and duplicate metrics.
- `dashboard/app.py` runs the Streamlit dashboard and persists JSON outputs.

## Folder Structure

```text
PulseOps/
├── ingestion/
│   └── mock_events.py
├── processor/
│   ├── validate_event.py
│   └── normaliser.py
├── analytics/
│   ├── correlation_engine.py
│   └── quality_checks.py
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   └── processed/
├── requirements.txt
├── README.md
└── .gitignore
```

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run dashboard/app.py
```

The app writes the generated datasets to:

- `data/processed/processed_events.json`
- `data/processed/correlation_insights.json`

## GitHub

```bash
git init
git add .
git commit -m "Initial PulseOps implementation"
git push
```
