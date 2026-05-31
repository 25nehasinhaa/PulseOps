import { GitPullRequest, MessageSquare, Siren, TimerReset } from "lucide-react";
import type { CoralResult } from "@/lib/types";

function formatTime(value?: string) {
  if (!value) return "pending";
  return value.replace("T", " ").replace("Z", " UTC");
}

export function EvidenceTimeline({ coralResult }: { coralResult: CoralResult }) {
  const row = coralResult.incident_diagnosis?.[0];
  const items = [
    {
      label: "GitHub PR merged",
      value: row?.pr_title || "Waiting for Coral result",
      meta: row ? `${formatTime(row.pr_merged_at)} by ${row.pr_author}` : "Run diagnosis to populate timeline",
      icon: GitPullRequest,
      tone: "green",
    },
    {
      label: "Sentry issue detected",
      value: row?.sentry_error || "No error evidence yet",
      meta: row ? `${formatTime(row.sentry_first_seen)} - ${row.sentry_count} events` : "Coral joins Sentry issues after deploys",
      icon: Siren,
      tone: "plum",
    },
    {
      label: "Slack incident context",
      value: row?.slack_message || "No Slack context yet",
      meta: row?.slack_channel || "Coral joins incident channel messages",
      icon: MessageSquare,
      tone: "sand",
    },
    {
      label: "Time to incident",
      value: row ? `${row.time_to_incident_minutes} minutes` : "Unknown",
      meta: "Computed from PR merge to first Sentry signal",
      icon: TimerReset,
      tone: "almond",
    },
  ];

  return (
    <section className="panel evidence-panel">
      <div className="panel-head">
        <div>
          <span className="panel-kicker">Coral evidence graph</span>
          <h2>Deployment to Incident Timeline</h2>
        </div>
        <span className="pill">Joined result</span>
      </div>
      <div className="timeline-list">
        {items.map((item) => {
          const Icon = item.icon;
          return (
            <div className={`timeline-item ${item.tone}`} key={item.label}>
              <div className="timeline-icon"><Icon size={17} /></div>
              <div>
                <span>{item.label}</span>
                <strong>{item.value}</strong>
                <p>{item.meta}</p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}
