export type Severity = "fatal" | "error" | "warning" | "info";
export type IncidentStatus = "open" | "investigating" | "resolved";
export type Source = "sentry" | "github" | "slack" | "pagerduty";
export type StreamEventType = "sql" | "coral_result" | "diagnosis" | "status" | "done" | "text";

export interface Incident {
  id: string;
  title: string;
  severity: Severity;
  source: Source;
  timestamp: string;
  related_pr?: string | null;
  related_slack?: string | null;
  status: IncidentStatus;
  error_count?: number;
  time_to_incident_minutes?: number | null;
}

export interface CoralResult {
  incident_diagnosis?: IncidentDiagnosis[];
  [key: string]: unknown;
}

export interface IncidentDiagnosis {
  pr_title: string;
  pr_merged_at: string;
  pr_author: string;
  sentry_error: string;
  sentry_first_seen: string;
  sentry_count: number;
  slack_message: string;
  slack_channel: string;
  time_to_incident_minutes: number;
}

export interface IncidentsResponse {
  incidents: Incident[];
  coral_sql: string;
  coral_metrics: CoralResult;
  sources_connected: Source[];
}

export type ReadinessStatus = "ready" | "demo" | "manual";

export interface ReadinessCheck {
  id: string;
  label: string;
  status: ReadinessStatus;
  detail: string;
}

export interface ReadinessResponse {
  project: string;
  demo_mode: boolean;
  coral_available: boolean;
  free_submission_mode: boolean;
  checks: ReadinessCheck[];
}

export interface StreamEvent {
  type: StreamEventType;
  sql?: string;
  data?: CoralResult;
  text?: string;
  chunk?: string;
}
