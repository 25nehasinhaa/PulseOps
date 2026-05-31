# Deployment Guide

## Backend: Railway

Root directory:

```text
/
```

Start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```text
DEMO_MODE=true
CORAL_AVAILABLE=false
SLACK_CHANNEL=#incidents
FREE_SUBMISSION_MODE=true
```

Use `DEMO_MODE=true` for a stable public demo. For local live Coral demos, run the backend locally with Coral configured and tunnel it with ngrok.

## Frontend: Vercel

Root directory:

```text
frontend
```

Environment variables:

```text
NEXT_PUBLIC_API_URL=https://your-railway-backend.example
NEXT_PUBLIC_DEMO_MODE=true
```

Build command:

```bash
npm run build
```

## Local Verification

Backend:

```bash
uvicorn backend.main:app --reload --port 8010
```

Verify:

```text
http://127.0.0.1:8010/health
http://127.0.0.1:8010/readiness
```

Frontend:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:3000/dashboard
```
