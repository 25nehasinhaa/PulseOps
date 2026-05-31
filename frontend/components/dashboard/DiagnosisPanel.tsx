"use client";

import { BrainCircuit, Download, FileText, Play } from "lucide-react";
import type { CoralResult, Incident } from "@/lib/types";

export function DiagnosisPanel({
  incident,
  diagnosis,
  postmortem,
  loading,
  onDiagnose,
  onPostmortem
}: {
  incident?: Incident;
  diagnosis: string;
  postmortem: string;
  loading: boolean;
  onDiagnose: () => void;
  onPostmortem: () => void;
  coralResult?: CoralResult;
}) {
  function downloadPostmortem() {
    if (!postmortem || !incident) return;
    const blob = new Blob([postmortem], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${incident.id.toLowerCase()}-postmortem.md`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="panel diagnosis-panel">
      <div className="panel-head">
        <div>
          <span className="panel-kicker">AI SRE layer</span>
          <h2>{incident ? incident.id : "Select an incident"}</h2>
        </div>
        <div className="button-row">
          <button className="icon-button" onClick={onDiagnose} disabled={!incident || loading} title="Diagnose with Coral">
            <Play size={16} />
            Diagnose
          </button>
          <button className="icon-button ghost" onClick={onPostmortem} disabled={!incident || loading} title="Generate postmortem">
            <FileText size={16} />
            Postmortem
          </button>
          <button className="icon-button ghost" onClick={downloadPostmortem} disabled={!postmortem} title="Download postmortem markdown">
            <Download size={16} />
            Download
          </button>
        </div>
      </div>
      <div className="stream-box">
        <div className="stream-title"><BrainCircuit size={16} /> Streaming diagnosis</div>
        <article>{diagnosis || "Run diagnosis to stream root cause, timeline, blast radius, immediate fix, prevention, and confidence."}</article>
      </div>
      {postmortem ? (
        <div className="postmortem-report">
          <div className="postmortem-report-head">
            <div>
              <span className="panel-kicker">Generated report</span>
              <h3>{incident?.id || "Incident"} Postmortem</h3>
            </div>
            <button className="icon-button ghost" onClick={downloadPostmortem} title="Download postmortem markdown">
              <Download size={16} />
              Download .md
            </button>
          </div>
          <article>{postmortem}</article>
        </div>
      ) : null}
    </section>
  );
}
