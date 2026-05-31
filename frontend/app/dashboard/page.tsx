"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { Activity, ArrowLeft, DatabaseZap, ShieldCheck } from "lucide-react";
import { DiagnosisPanel } from "@/components/dashboard/DiagnosisPanel";
import { EvidenceTimeline } from "@/components/dashboard/EvidenceTimeline";
import { IncidentFeed } from "@/components/dashboard/IncidentFeed";
import { QueryBar } from "@/components/dashboard/QueryBar";
import { ReadinessPanel } from "@/components/dashboard/ReadinessPanel";
import { SqlVisualizer } from "@/components/dashboard/SqlVisualizer";
import { fetchIncidents, fetchReadiness, streamEndpoint } from "@/lib/api";
import { fallbackIncidents } from "@/lib/demo-data";
import type { CoralResult, Incident, ReadinessCheck } from "@/lib/types";

export default function DashboardPage() {
  const [incidents, setIncidents] = useState<Incident[]>(fallbackIncidents);
  const [selected, setSelected] = useState<Incident | undefined>(fallbackIncidents[0]);
  const [sql, setSql] = useState("");
  const [diagnosis, setDiagnosis] = useState("");
  const [postmortem, setPostmortem] = useState("");
  const [coralResult, setCoralResult] = useState<CoralResult>({});
  const [readinessChecks, setReadinessChecks] = useState<ReadinessCheck[]>([]);
  const [query, setQuery] = useState("Why did our API go down last Tuesday?");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchIncidents()
      .then((data) => {
        setIncidents(data.incidents);
        setSelected(data.incidents[0]);
        setSql(data.coral_sql);
        setCoralResult(data.coral_metrics);
      })
      .catch(() => {
        setIncidents(fallbackIncidents);
        setSelected(fallbackIncidents[0]);
      });

    fetchReadiness()
      .then((data) => setReadinessChecks(data.checks))
      .catch(() => {
        setReadinessChecks([
          {
            id: "offline",
            label: "Readiness API",
            status: "demo",
            detail: "Backend readiness could not be reached, but local demo fallback is available.",
          },
        ]);
      });
  }, []);

  const stats = useMemo(() => {
    const open = incidents.filter((item) => item.status !== "resolved").length;
    const events = incidents.reduce((total, item) => total + (item.error_count || 0), 0);
    return { open, events, sources: 3 };
  }, [incidents]);

  async function runDiagnose() {
    if (!selected) return;
    setLoading(true);
    setDiagnosis("");
    setPostmortem("");
    try {
      await streamEndpoint(
        "/diagnose",
        { question: `Diagnose ${selected.id}: ${selected.title}`, time_window_hours: 24, demo_mode: true },
        (event) => {
          if (event.type === "sql" && event.sql) setSql(event.sql);
          if (event.type === "coral_result" && event.data) setCoralResult(event.data);
          if (event.type === "diagnosis" && event.text) setDiagnosis((current) => current + event.text);
        }
      );
    } finally {
      setLoading(false);
    }
  }

  async function runQuery() {
    setLoading(true);
    setDiagnosis("");
    setPostmortem("");
    try {
      await streamEndpoint("/query", { natural_language: query, demo_mode: true }, (event) => {
        if (event.type === "sql" && event.sql) setSql(event.sql);
        if (event.type === "coral_result" && event.data) setCoralResult(event.data);
        if (event.type === "diagnosis" && event.text) setDiagnosis((current) => current + event.text);
        if (event.type === "status" && event.text) setDiagnosis((current) => `${current}${event.text}\n`);
      });
    } finally {
      setLoading(false);
    }
  }

  async function runPostmortem() {
    if (!selected) return;
    setLoading(true);
    setPostmortem("");
    try {
      await streamEndpoint(
        "/postmortem",
        { incident_id: selected.id, coral_data: coralResult, demo_mode: true },
        (event) => {
          if (event.type === "text" && event.chunk) setPostmortem((current) => current + event.chunk);
        }
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="dashboard-shell">
      <nav className="topbar">
        <Link href="/" className="back-link"><ArrowLeft size={16} /> CoralOps</Link>
        <div className="topbar-status"><span /> Demo mode connected to FastAPI</div>
      </nav>

      <header className="dashboard-header">
        <div>
          <p className="eyebrow"><DatabaseZap size={16} /> Coral-powered operational intelligence</p>
          <h1>AI SRE Control Room</h1>
          <p>Join production signals, diagnose incidents, and generate postmortems from a single workflow.</p>
        </div>
        <div className="metric-row">
          <div className="metric"><Activity size={18} /><strong>{stats.open}</strong><span>open incidents</span></div>
          <div className="metric"><ShieldCheck size={18} /><strong>{stats.events}</strong><span>Sentry events</span></div>
          <div className="metric"><DatabaseZap size={18} /><strong>{stats.sources}</strong><span>joined sources</span></div>
        </div>
      </header>

      <QueryBar value={query} loading={loading} onChange={setQuery} onSubmit={runQuery} />

      <div className="dashboard-grid">
        <IncidentFeed incidents={incidents} selectedId={selected?.id} onSelect={setSelected} />
        <DiagnosisPanel
          incident={selected}
          diagnosis={diagnosis}
          postmortem={postmortem}
          loading={loading}
          onDiagnose={runDiagnose}
          onPostmortem={runPostmortem}
          coralResult={coralResult}
        />
      </div>

      <EvidenceTimeline coralResult={coralResult} />
      <SqlVisualizer sql={sql} />
      <ReadinessPanel checks={readinessChecks} />
    </main>
  );
}
