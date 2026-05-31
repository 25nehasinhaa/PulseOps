import type { Source } from "@/lib/types";

const labels: Record<Source, string> = {
  sentry: "Sentry",
  github: "GitHub",
  slack: "Slack",
  pagerduty: "PagerDuty"
};

export function SourceBadge({ source }: { source: Source }) {
  return <span className={`source-badge ${source}`}>{labels[source]}</span>;
}
