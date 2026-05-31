# CoralOps Demo Script

Target length: 2 minutes 30 seconds.

## 0:00 - Hook

"Last Tuesday, our API went down. Engineers had to jump between GitHub, Sentry, Slack, and incident tooling just to understand what happened. CoralOps turns that into one joined operational timeline."

## 0:20 - Show Product

"This is CoralOps, an AI SRE workspace for enterprise incident response. The interface is intentionally quiet: the important thing is the signal."

## 0:35 - Select Incident

"I select this active incident. We already know the symptom, but we do not yet know the root cause."

## 0:45 - Diagnose

"Now CoralOps runs a Coral SQL query joining GitHub pull requests, Sentry errors, and Slack incident messages. No ETL. No warehouse. One query."

## 1:05 - Explain Diagnosis

"The local SRE engine identifies the likely root cause, establishes a timeline, estimates blast radius, and gives immediate and preventative actions. This keeps the whole submission free to run."

## 1:25 - Evidence Timeline

"The evidence timeline is the important part. CoralOps is not guessing from one source. It ties the PR merge, the first Sentry error, Slack incident context, and the time delta into one story."

## 1:45 - Postmortem

"One more click generates a structured incident postmortem. This usually takes an engineer another hour after the incident. Here it is drafted from the same joined evidence."

## 2:10 - Coral Angle

"PulseOps was my first mock dashboard. CoralOps is the real direction: replace mocked operational correlation with Coral's local SQL layer across production tools."

## 2:30 - Close

"CoralOps: one operational question, one Coral query, one SRE-ready answer."
