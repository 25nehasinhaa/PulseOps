# CoralOps Submission Copy

## Project Name

CoralOps, AI SRE powered by Coral

## Track

Enterprise Agent

## Short Description

CoralOps is an SRE workspace that uses Coral SQL to join GitHub pull requests, Sentry errors, and Slack incident context into one operational evidence timeline. It streams a free local SRE diagnosis, generates a markdown postmortem, and lets teams move from incident signal to response narrative in one workflow.

## Long Description

CoralOps turns fragmented incident investigation into a single joined evidence trail. Instead of manually checking GitHub for recent deployments, Sentry for production errors, and Slack for incident context, CoralOps uses Coral SQL patterns to correlate those sources and show the root cause timeline directly in the dashboard.

The product includes incident selection, Coral SQL visualization, streamed local SRE diagnosis, deployment timeline, postmortem generation, markdown download, and a readiness panel for the hackathon submission. The entire submission can run on free tools: Next.js, FastAPI, Coral local demo mode, free operational sources, and deterministic local SRE analysis.

## What Makes It Coral Native

1. Coral SQL is the core retrieval abstraction.
2. The main query joins GitHub pull requests, Sentry issues, and Slack messages.
3. The diagnosis and postmortem are grounded in the joined Coral shaped result.
4. A PagerDuty Coral source draft is included for the custom source path.

## URLs

1. GitHub: https://github.com/25nehasinhaa/PulseOps
2. Live app: https://frontend-gold-gamma-85.vercel.app
3. Backend API: https://api-production-4e7b.up.railway.app
4. YouTube demo: add after recording

## Demo Steps

1. Open the dashboard.
2. Select `INC-001`.
3. Click `Diagnose`.
4. Show the Coral SQL and evidence timeline.
5. Click `Postmortem`.
6. Download the markdown report.
7. Show the readiness panel.

## Tech Stack

1. Next.js
2. TypeScript
3. FastAPI
4. Coral SQL and Coral shaped local demo mode
5. Server sent events
6. Free local SRE analysis engine
7. Vercel and Railway deployment config
