"use client";

import type { Incident } from "@/lib/types";
import { SourceBadge } from "@/components/ui/SourceBadge";
import { StatusDot } from "@/components/ui/StatusDot";

export function IncidentFeed({
  incidents,
  selectedId,
  onSelect
}: {
  incidents: Incident[];
  selectedId?: string;
  onSelect: (incident: Incident) => void;
}) {
  return (
    <section className="panel incident-feed">
      <div className="panel-head">
        <div>
          <span className="panel-kicker">Live incidents</span>
          <h2>Correlated Signals</h2>
        </div>
        <span className="pill">{incidents.length} active</span>
      </div>
      <div className="incident-list">
        {incidents.map((incident) => (
          <button
            className={`incident-card ${incident.severity} ${selectedId === incident.id ? "selected" : ""}`}
            key={incident.id}
            onClick={() => onSelect(incident)}
          >
            <div className="incident-card-top">
              <SourceBadge source={incident.source} />
              <span className="incident-id">{incident.id}</span>
            </div>
            <strong>{incident.title}</strong>
            <span className="incident-meta">
              <StatusDot tone={incident.status === "resolved" ? "ok" : incident.severity === "fatal" ? "bad" : "warn"} />
              {incident.status} - {incident.error_count || 0} events - {incident.time_to_incident_minutes ?? "?"} min after deploy
            </span>
            <span className="incident-pr">{incident.related_pr || "No linked PR yet"}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
