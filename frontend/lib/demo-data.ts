import type { Incident } from "./types";

export const fallbackIncidents: Incident[] = [
  {
    id: "INC-001",
    title: "Fatal: OperationalError - too many DB connections",
    severity: "fatal",
    source: "sentry",
    timestamp: "2026-05-20T14:47:00Z",
    related_pr: "feat: optimize database connection pooling",
    related_slack: "INCIDENT: API response times spiking 400%",
    status: "investigating",
    error_count: 847,
    time_to_incident_minutes: 15
  },
  {
    id: "INC-002",
    title: "Error: Unhandled TypeError in payment service",
    severity: "error",
    source: "sentry",
    timestamp: "2026-05-20T11:22:00Z",
    related_pr: "refactor: payment service middleware",
    related_slack: "Payment service throwing 500s",
    status: "resolved",
    error_count: 124,
    time_to_incident_minutes: 8
  }
];
