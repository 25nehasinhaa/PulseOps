# CoralOps Submission Copy

## Project Name

CoralOps - AI SRE powered by Coral

## Track

Enterprise Agent

## Short Description

CoralOps is an AI-style SRE workspace that uses Coral SQL to join GitHub pull requests, Sentry errors, and Slack incident context into one operational evidence timeline. It streams a free local SRE diagnosis, generates a markdown postmortem, and lets teams move from incident signal to response narrative in one workflow.

## Long Description

CoralOps turns fragmented incident investigation into a single joined evidence trail. Instead of manually checking GitHub for recent deployments, Sentry for production errors, and Slack for incident context, CoralOps uses Coral-style SQL to correlate those sources and show the root-cause timeline directly in the dashboard.

The product includes incident selection, Coral SQL visualization, streamed local SRE diagnosis, deployment-to-incident timeline, postmortem generation, markdown download, and a readiness panel for the hackathon submission. The entire submission can run on free tools: Next.js, FastAPI, Coral/local demo mode, free-tier operational sources, and deterministic local SRE analysis.

## What Makes It Coral-Centric

- Coral SQL is the core retrieval abstraction.
- The main query joins GitHub pull requests, Sentry issues, and Slack messages.
- The diagnosis and postmortem are grounded in the joined Coral-shaped result.
- A PagerDuty Coral source draft is included for the custom source path.

## URLs To Fill In

- GitHub: `TODO`
- Live app: `TODO`
- Backend API: `TODO`
- YouTube demo: `TODO`

## Demo Steps

1. Open the dashboard.
2. Select `INC-001`.
3. Click `Diagnose`.
4. Show the Coral SQL and evidence timeline.
5. Click `Postmortem`.
6. Download the markdown report.
7. Show the readiness panel.

## Tech Stack

- Next.js
- TypeScript
- FastAPI
- Coral SQL / Coral-shaped local demo mode
- Server-sent events
- Free local SRE analysis engine
- Vercel / Railway deployment config
