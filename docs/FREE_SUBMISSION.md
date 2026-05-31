# Free Submission Mode

CoralOps is configured to run for submission without paid services.

## Free Stack

- Frontend: Next.js on Vercel free tier.
- Backend: FastAPI on Railway free/trial tier or local tunnel for demo.
- Data layer: Coral CLI with free/local source setup.
- Demo fallback: realistic Coral-shaped incident evidence.
- Analysis: deterministic local SRE engine, no paid LLM API.
- Incident tools: GitHub, Sentry free tier, Slack free workspace.
- Video: YouTube free upload.

## Default Environment

```text
DEMO_MODE=true
CORAL_AVAILABLE=false
FREE_SUBMISSION_MODE=true
SLACK_CHANNEL=#incidents
```

## Why This Is Acceptable

The core hackathon idea is Coral-powered retrieval and cross-source incident context. The local SRE engine makes the demo stable and free while still showing the product workflow: Coral SQL, joined evidence, streamed diagnosis, timeline, postmortem, and export.

## Upgrade Path After Submission

If credits are available later, a hosted LLM can replace the local SRE engine. That is optional and not required for the free submission.
