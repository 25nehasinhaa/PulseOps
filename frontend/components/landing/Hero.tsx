import Link from "next/link";
import { ArrowRight, DatabaseZap } from "lucide-react";

export function Hero() {
  return (
    <main className="landing-shell">
      <nav className="landing-nav">
        <div className="brand-mark">CoralOps <span className="brand-line" /></div>
        <div className="landing-links">
          <Link href="/dashboard">Dashboard</Link>
          <a href="http://127.0.0.1:8010/docs">API</a>
          <a href="https://www.wemakedevs.org/hackathons/coral">Hackathon</a>
          <a href="https://withcoral.com">Coral</a>
        </div>
      </nav>
      <section className="hero-panel">
        <div className="hero-copy">
          <div className="eyebrow"><DatabaseZap size={16} /> Enterprise Agent Hackathon Build</div>
          <h1>Selected signals for incident response right now</h1>
          <p>
            A refined AI SRE workspace that joins GitHub, Sentry, and Slack with Coral SQL,
            then turns operational noise into diagnosis, timelines, and postmortems.
          </p>
          <div className="hero-actions">
            <Link className="primary-link" href="/dashboard">
              Open Dashboard <ArrowRight size={18} />
            </Link>
            <a className="secondary-link" href="http://127.0.0.1:8010/docs">
              API Docs
            </a>
          </div>
        </div>
        <div className="showcase-row" aria-label="CoralOps feature gallery">
          <div className="showcase-card carbon side-left">
            <span>Coral SQL</span>
            <strong>Cross-source joins without glue code</strong>
          </div>
          <div className="showcase-card plum">
            <span>Sentry</span>
            <strong>Fatal errors mapped to deployments</strong>
          </div>
          <div className="showcase-card almond">
            <span>Diagnosis</span>
            <strong>Root cause, blast radius, and fix path</strong>
          </div>
          <div className="showcase-card green">
            <span>Postmortem</span>
            <strong>Incident reports generated in one click</strong>
          </div>
          <div className="showcase-card sand side-right">
            <span>Slack</span>
            <strong>Team context joined into the timeline</strong>
          </div>
        </div>
      </section>
    </main>
  );
}
