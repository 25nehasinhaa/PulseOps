import { CheckCircle2, CircleDashed, ExternalLink, RadioTower } from "lucide-react";
import type { ReadinessCheck } from "@/lib/types";

function statusLabel(status: ReadinessCheck["status"]) {
  if (status === "ready") return "Ready";
  if (status === "demo") return "Demo";
  return "Manual";
}

export function ReadinessPanel({ checks }: { checks: ReadinessCheck[] }) {
  return (
    <section className="panel readiness-panel">
      <div className="panel-head">
        <div>
          <span className="panel-kicker">Submission command center</span>
          <h2>Hackathon Readiness</h2>
        </div>
        <a className="pill link-pill" href="https://www.wemakedevs.org/hackathons/coral" target="_blank">
          Official page <ExternalLink size={13} />
        </a>
      </div>
      <div className="readiness-grid">
        {checks.map((check) => {
          const Icon = check.status === "ready" ? CheckCircle2 : check.status === "demo" ? RadioTower : CircleDashed;
          return (
            <div className={`readiness-item ${check.status}`} key={check.id}>
              <div className="readiness-top">
                <Icon size={17} />
                <span>{statusLabel(check.status)}</span>
              </div>
              <strong>{check.label}</strong>
              <p>{check.detail}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
