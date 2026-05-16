"""PulseOps Streamlit dashboard."""

from __future__ import annotations

import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analytics.correlation_engine import correlate_events, generate_ai_insights
from analytics.quality_checks import run_quality_checks
from ingestion.mock_events import generate_mock_events
from processor.normaliser import normalize_events
from processor.validate_event import validate_events


PROCESSED_DIR = ROOT / "data" / "processed"
PROCESSED_EVENTS_PATH = PROCESSED_DIR / "processed_events.json"
CORRELATION_INSIGHTS_PATH = PROCESSED_DIR / "correlation_insights.json"


def persist_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


@st.cache_data(ttl=30)
def build_pipeline() -> dict[str, Any]:
    raw_events = generate_mock_events()
    normalized_events = normalize_events(raw_events)
    processed_events = validate_events(normalized_events)
    correlations = correlate_events(processed_events)
    insights = generate_ai_insights(correlations)
    quality = run_quality_checks(processed_events)

    persist_json(PROCESSED_EVENTS_PATH, processed_events)
    persist_json(CORRELATION_INSIGHTS_PATH, {"correlations": correlations, "ai_insights": insights})

    return {
        "events": processed_events,
        "correlations": correlations,
        "insights": insights,
        "quality": quality,
        "frame": pd.DataFrame(processed_events),
    }


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def status_class(status: str) -> str:
    status = status.upper()
    if status in {"SUCCESS", "RESOLVED", "FIXED"}:
        return "sv-success"
    if status in {"CRITICAL", "OPEN"}:
        return "sv-critical"
    return "sv-warning"


def source_class(source: str) -> str:
    if source in {"github", "sentry", "pagerduty"}:
        return source
    return "slack"


def source_icon(source: str) -> str:
    return {"github": "GH", "sentry": "SE", "pagerduty": "PD", "service_alert": "SA"}.get(source, "EV")


def event_rows(events: list[dict[str, Any]]) -> str:
    rows = []
    for event in events[:6]:
        source = source_class(str(event["source"]))
        status = str(event.get("status", "UNKNOWN")).upper()
        description = esc(event.get("description", event["event_type"]))
        rows.append(
            f"""
            <div class="event-row er-{source}" onclick="showToast('Event {esc(event["event_id"])} - {description}')">
              <div class="ev-id">{esc(event["event_id"])}</div>
              <div class="ev-source src-{source}">{source_icon(str(event["source"]))}</div>
              <div class="ev-desc">{description}<small>{esc(event["event_type"])} &middot; {esc(str(event["timestamp"])[11:19])} UTC</small></div>
              <div class="ev-service">{esc(event["affected_service"])}</div>
              <div class="ev-status {status_class(status)}"><div class="sv-dot"></div>{esc(status)}</div>
            </div>
            """
        )
    return "\n".join(rows)


def correlation_rows(correlations: list[dict[str, Any]]) -> str:
    rows = []
    for item in correlations:
        severity = str(item["severity"]).upper()
        color = "var(--red)" if severity == "CRITICAL" else "var(--amber)"
        background = "rgba(255,61,90,.15)" if severity == "CRITICAL" else "rgba(255,170,0,.15)"
        border = "rgba(255,61,90,.3)" if severity == "CRITICAL" else "rgba(255,170,0,.3)"
        rows.append(
            f"""
            <div class="corr-row" onclick="openModal('{esc(item["deployment_event"])}','Deploy to Incident Correlation','{esc(item["affected_service"])}','{severity}','{esc(item["summary"])}','{item["confidence"]}%')">
              <div class="cr-service">{esc(item["deployment_event"])} &middot; GitHub Deploy</div>
              <div class="cr-type">{esc(item["affected_service"])} &rarr; {len(item["related_event_ids"])} related signals</div>
              <div><span class="cr-sev" style="background:{background};color:{color};border:1px solid {border}">{severity}</span></div>
              <div class="bar-container"><div class="bar-fill" style="width:{item["confidence"]}%;background:{color};box-shadow:0 0 6px {color};"></div></div>
            </div>
            """
        )
    rows.append(
        """
        <div class="corr-row" style="opacity:.5;">
          <div class="cr-service" style="color:var(--text2)">No further correlations</div>
          <div class="cr-type">All other deployments clean</div>
          <div><span class="cr-sev" style="background:rgba(0,224,150,.1);color:var(--green);border:1px solid rgba(0,224,150,.2)">CLEAN</span></div>
          <div class="bar-container"><div class="bar-fill" style="width:0%;background:var(--green);"></div></div>
        </div>
        """
    )
    return "\n".join(rows)


def insight_markup(insights: list[dict[str, str]]) -> str:
    primary = insights[0] if insights else {
        "priority": "LOW",
        "service": "all services",
        "insight": "No correlated incident chains are active.",
        "recommended_action": "Continue monitoring the live event feed.",
    }
    return f"""
    <div class="ai-msg">
      <div class="ai-avatar av-ai">AI</div>
      <div class="ai-bubble ai">
        <strong>{esc(primary["priority"])} PRIORITY INCIDENT</strong><br>
        {esc(primary["insight"])}<br><br>
        <strong>Recommended Action:</strong><br>
        {esc(primary["recommended_action"])}
        <span class="ai-ts">Just now &middot; PulseOps AI &middot; RAG-grounded</span>
      </div>
    </div>
    <div class="ai-msg">
      <div class="ai-avatar av-sys">SYS</div>
      <div class="ai-bubble sys" style="font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text2)">
        Pipeline status: SQS &rarr; Lambda &rarr; S3 OK<br>
        DLQ depth: 0 &middot; Validation pass rate: 100%
        <span class="ai-ts">Live UTC</span>
      </div>
    </div>
    """


def render_dashboard(payload: dict[str, Any]) -> str:
    events = payload["events"]
    correlations = payload["correlations"]
    insights = payload["insights"]
    critical_count = sum(1 for event in events if str(event.get("status")).upper() in {"CRITICAL", "OPEN"})
    health = 90
    generated_at = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');
:root {{
  --black:#020408; --deep:#060d16; --navy:#0a1628; --card:#0d1f35; --edge:#122440; --rim:#1a3355;
  --cyan:#00e5ff; --cyan2:#00b8d9; --cyan-glow:rgba(0,229,255,.12); --cyan-dim:rgba(0,229,255,.06);
  --amber:#ffaa00; --amber-glow:rgba(255,170,0,.12); --red:#ff3d5a; --red-glow:rgba(255,61,90,.15);
  --green:#00e096; --green-glow:rgba(0,224,150,.12); --purple:#7c4dff; --text:#c8dff0; --text2:#5a7a99; --text3:#2a4060;
}}
*{{box-sizing:border-box;margin:0;padding:0}} html{{scroll-behavior:smooth}}
body{{background:var(--black);color:var(--text);font-family:'Syne',sans-serif;min-height:100vh;overflow-x:hidden}}
.bg-mesh,.scanlines,.grid-bg{{position:fixed;inset:0;z-index:0;pointer-events:none}}
.bg-mesh{{background:radial-gradient(ellipse 60% 40% at 15% 20%,rgba(0,100,200,.07) 0%,transparent 60%),radial-gradient(ellipse 40% 60% at 85% 80%,rgba(0,180,220,.05) 0%,transparent 60%),radial-gradient(ellipse 50% 30% at 50% 50%,rgba(124,77,255,.03) 0%,transparent 60%);animation:meshDrift 20s ease-in-out infinite alternate}}
@keyframes meshDrift{{0%{{filter:hue-rotate(0deg)}}100%{{filter:hue-rotate(20deg)}}}}
.scanlines{{background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,rgba(0,229,255,.008) 3px,rgba(0,229,255,.008) 4px)}}
.grid-bg{{background-image:linear-gradient(rgba(0,229,255,.025) 1px,transparent 1px),linear-gradient(90deg,rgba(0,229,255,.025) 1px,transparent 1px);background-size:60px 60px}}
.z1{{position:relative;z-index:1}}
nav{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0 40px;height:64px;background:rgba(2,4,8,.85);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,229,255,.08)}}
.nav-logo{{display:flex;align-items:center;gap:10px;font-family:'Bebas Neue',sans-serif;font-size:24px;letter-spacing:3px;color:var(--cyan);text-shadow:0 0 20px rgba(0,229,255,.5)}}
.logo-pulse{{width:10px;height:10px;border-radius:50%;background:var(--cyan);box-shadow:0 0 12px var(--cyan);animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{transform:scale(1);opacity:1}}50%{{transform:scale(1.5);opacity:.5}}}}
.nav-status{{display:flex;align-items:center;gap:24px;font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text2)}} .status-dot{{width:6px;height:6px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse 1.5s ease-in-out infinite;display:inline-block;margin-right:6px}} .nav-time{{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--cyan);border:1px solid rgba(0,229,255,.2);padding:4px 12px;border-radius:4px;background:rgba(0,229,255,.04)}}
.wrapper{{padding:88px 40px 60px;max-width:1600px;margin:0 auto}}
.hero{{display:grid;grid-template-columns:1fr auto;align-items:end;gap:40px;margin-bottom:48px;padding-bottom:36px;border-bottom:1px solid var(--edge)}} .hero-eyebrow{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--cyan);margin-bottom:12px;display:flex;align-items:center;gap:8px}} .hero-eyebrow:before{{content:'';width:24px;height:1px;background:var(--cyan)}} .hero-title{{font-family:'Bebas Neue',sans-serif;font-size:clamp(52px,6vw,80px);line-height:.9;letter-spacing:4px;color:#fff;text-shadow:0 0 60px rgba(0,229,255,.15);margin-bottom:10px}} .hero-title span{{color:var(--cyan)}} .hero-sub{{font-size:13px;color:var(--text2);font-family:'JetBrains Mono',monospace;letter-spacing:.5px}}
.system-health{{display:flex;flex-direction:column;align-items:flex-end;gap:8px}} .health-label{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--text3)}} .health-ring{{position:relative;width:100px;height:100px}} .health-ring svg{{width:100%;height:100%;transform:rotate(-90deg)}} .health-ring circle.track{{fill:none;stroke:var(--edge);stroke-width:6}} .health-ring circle.fill{{fill:none;stroke:var(--green);stroke-width:6;stroke-dasharray:251;stroke-dashoffset:25;stroke-linecap:round;filter:drop-shadow(0 0 8px var(--green));transition:stroke-dashoffset 1.5s ease}} .health-num{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:26px;color:var(--green);line-height:1}} .health-num span{{font-size:9px;font-family:'Syne',sans-serif;color:var(--text2)}}
.kpi-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:32px}} .kpi-card{{background:var(--card);border:1px solid var(--edge);border-radius:12px;padding:24px 24px 20px;position:relative;overflow:hidden;cursor:pointer;transition:border-color .3s,transform .2s}} .kpi-card:before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;border-radius:12px 12px 0 0}} .kpi-card.blue:before{{background:linear-gradient(90deg,var(--cyan),transparent)}} .kpi-card.amber:before{{background:linear-gradient(90deg,var(--amber),transparent)}} .kpi-card.red:before{{background:linear-gradient(90deg,var(--red),transparent)}} .kpi-card.green:before{{background:linear-gradient(90deg,var(--green),transparent)}} .kpi-card:after{{content:'';position:absolute;inset:0;border-radius:12px;opacity:0;transition:opacity .3s}} .kpi-card.blue:after{{background:var(--cyan-dim)}} .kpi-card.amber:after{{background:var(--amber-glow)}} .kpi-card.red:after{{background:var(--red-glow)}} .kpi-card.green:after{{background:var(--green-glow)}} .kpi-card:hover{{transform:translateY(-3px)}} .kpi-card:hover:after{{opacity:1}} .kpi-label{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--text2);margin-bottom:16px;position:relative;z-index:1}} .kpi-num{{font-family:'Bebas Neue',sans-serif;font-size:52px;line-height:1;letter-spacing:2px;position:relative;z-index:1}} .blue .kpi-num{{color:var(--cyan)}} .amber .kpi-num{{color:var(--amber)}} .red .kpi-num{{color:var(--red)}} .green .kpi-num{{color:var(--green)}} .kpi-sub{{font-size:11px;color:var(--text2);position:relative;z-index:1;margin-top:8px;display:flex;align-items:center;gap:6px}} .kpi-trend{{font-size:10px;padding:1px 6px;border-radius:3px;font-weight:600}} .trend-up{{background:rgba(0,224,150,.15);color:var(--green)}} .trend-down{{background:rgba(255,61,90,.15);color:var(--red)}} .trend-flat{{background:rgba(255,170,0,.15);color:var(--amber)}}
.main-grid{{display:grid;grid-template-columns:1fr 360px;gap:20px;margin-bottom:20px}} .bottom-grid{{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px}} .panel{{background:var(--card);border:1px solid var(--edge);border-radius:14px;overflow:hidden;transition:border-color .3s}} .panel:hover{{border-color:var(--rim)}} .panel-head{{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid var(--edge);background:rgba(0,0,0,.2)}} .panel-title{{display:flex;align-items:center;gap:10px;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--text)}} .panel-icon{{width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;font-family:'JetBrains Mono',monospace;font-weight:700}} .pi-cyan{{background:var(--cyan-glow);color:var(--cyan)}} .pi-amber{{background:var(--amber-glow);color:var(--amber)}} .pi-red{{background:var(--red-glow);color:var(--red)}} .pi-green{{background:var(--green-glow);color:var(--green)}} .pi-purple{{background:rgba(124,77,255,.12);color:var(--purple)}} .panel-badge{{font-family:'JetBrains Mono',monospace;font-size:10px;padding:3px 10px;border-radius:99px;border:1px solid;font-weight:600}} .pb-cyan{{border-color:rgba(0,229,255,.25);color:var(--cyan);background:var(--cyan-dim)}} .pb-amber{{border-color:rgba(255,170,0,.25);color:var(--amber);background:var(--amber-glow)}} .pb-red{{border-color:rgba(255,61,90,.25);color:var(--red);background:var(--red-glow)}} .pb-green{{border-color:rgba(0,224,150,.25);color:var(--green);background:var(--green-glow)}}
.event-feed{{padding:8px 0}} .event-row,.event-row-head{{display:grid;grid-template-columns:90px 30px 1fr 140px 100px;gap:16px;align-items:center}} .event-row-head{{padding:8px 24px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--text3);border-bottom:1px solid var(--edge)}} .event-row{{padding:12px 24px;border-bottom:1px solid rgba(26,51,85,.5);cursor:pointer;transition:background .2s;position:relative}} .event-row:last-child{{border-bottom:none}} .event-row:hover{{background:rgba(0,229,255,.03)}} .event-row:before{{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;opacity:0;transition:opacity .2s}} .event-row:hover:before{{opacity:1}} .er-github:before{{background:var(--cyan)}} .er-sentry:before{{background:var(--amber)}} .er-pagerduty:before{{background:var(--red)}} .er-slack:before{{background:var(--purple)}} .ev-id{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text2)}} .ev-source{{width:24px;height:24px;border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:9px;font-family:'JetBrains Mono',monospace;font-weight:700}} .src-github{{background:rgba(0,229,255,.1);color:var(--cyan)}} .src-sentry{{background:rgba(255,170,0,.1);color:var(--amber)}} .src-pagerduty{{background:rgba(255,61,90,.1);color:var(--red)}} .src-slack{{background:rgba(124,77,255,.1);color:var(--purple)}} .ev-desc{{font-size:13px;color:var(--text)}} .ev-desc small{{display:block;font-size:11px;color:var(--text2);margin-top:2px;font-family:'JetBrains Mono',monospace}} .ev-service{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--cyan);background:var(--cyan-dim);border:1px solid rgba(0,229,255,.15);padding:3px 8px;border-radius:4px;text-align:center}} .ev-status{{display:flex;align-items:center;gap:6px;font-size:11px;font-weight:600}} .sv-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}} .sv-success{{color:var(--green)}} .sv-success .sv-dot{{background:var(--green);box-shadow:0 0 6px var(--green)}} .sv-critical{{color:var(--red)}} .sv-critical .sv-dot{{background:var(--red);box-shadow:0 0 6px var(--red);animation:pulse 1s infinite}} .sv-warning{{color:var(--amber)}} .sv-warning .sv-dot{{background:var(--amber);box-shadow:0 0 6px var(--amber)}}
.incident-list{{padding:12px 16px;display:flex;flex-direction:column;gap:10px}} .inc-card{{border:1px solid;border-radius:10px;padding:16px;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}} .inc-card:before{{content:'';position:absolute;top:0;left:0;bottom:0;width:3px;border-radius:3px 0 0 3px}} .inc-critical{{border-color:rgba(255,61,90,.3);background:linear-gradient(135deg,rgba(255,61,90,.06),rgba(13,31,53,0))}} .inc-critical:before{{background:var(--red)}} .inc-warning{{border-color:rgba(255,170,0,.3);background:linear-gradient(135deg,rgba(255,170,0,.06),rgba(13,31,53,0))}} .inc-warning:before{{background:var(--amber)}} .inc-resolved{{border-color:rgba(0,224,150,.2);background:linear-gradient(135deg,rgba(0,224,150,.04),rgba(13,31,53,0))}} .inc-resolved:before{{background:var(--green)}} .inc-card:hover{{transform:translateX(3px)}} .inc-top{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px}} .inc-id{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--text3);margin-bottom:4px}} .inc-title{{font-size:13px;font-weight:600;color:var(--text);line-height:1.3}} .inc-sev{{font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:3px 8px;border-radius:4px;white-space:nowrap;flex-shrink:0}} .sev-critical{{background:rgba(255,61,90,.15);color:var(--red);border:1px solid rgba(255,61,90,.3)}} .sev-high{{background:rgba(255,170,0,.15);color:var(--amber);border:1px solid rgba(255,170,0,.3)}} .sev-resolved{{background:rgba(0,224,150,.1);color:var(--green);border:1px solid rgba(0,224,150,.2)}} .inc-service{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text2);margin-bottom:10px}} .inc-bar{{height:3px;border-radius:3px;background:var(--edge);overflow:hidden;margin-bottom:8px}} .inc-bar-fill{{height:100%;border-radius:3px;transition:width 1s ease}} .fill-red{{background:var(--red);box-shadow:0 0 6px var(--red)}} .fill-amber{{background:var(--amber);box-shadow:0 0 6px var(--amber)}} .fill-green{{background:var(--green);box-shadow:0 0 6px var(--green)}} .inc-footer{{display:flex;align-items:center;justify-content:space-between;font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text3)}}
.sla-grid{{padding:20px 24px}} .sla-row{{margin-bottom:18px}} .sla-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}} .sla-name{{font-size:13px;color:var(--text);font-weight:500}} .sla-pct{{font-family:'Bebas Neue',sans-serif;font-size:20px;letter-spacing:1px}} .sla-track{{height:6px;background:var(--edge);border-radius:6px;overflow:hidden}} .sla-fill{{height:100%;border-radius:6px;transition:width 1.5s cubic-bezier(.34,1.56,.64,1)}} .sla-sub{{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--text3);margin-top:4px;display:flex;justify-content:space-between}}
.ai-messages{{padding:16px;display:flex;flex-direction:column;gap:12px;max-height:280px;overflow-y:auto}} .ai-msg{{display:flex;gap:10px;align-items:flex-start}} .ai-avatar{{width:28px;height:28px;border-radius:8px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:10px;font-family:'JetBrains Mono',monospace;font-weight:700}} .av-ai{{background:linear-gradient(135deg,rgba(0,229,255,.2),rgba(124,77,255,.2));border:1px solid rgba(0,229,255,.2);color:var(--cyan)}} .av-sys{{background:var(--edge);color:var(--text2)}} .ai-bubble{{flex:1;padding:10px 14px;border-radius:0 10px 10px 10px;font-size:12.5px;line-height:1.6;color:var(--text)}} .ai-bubble.ai{{background:rgba(0,229,255,.06);border:1px solid rgba(0,229,255,.12)}} .ai-bubble.sys{{background:var(--edge)}} .ai-bubble strong{{color:var(--cyan)}} .ai-ts{{display:block;font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--text3);margin-top:6px}} .ai-input-row{{display:flex;gap:10px;padding:16px;border-top:1px solid var(--edge)}} .ai-input{{flex:1;background:rgba(0,0,0,.3);border:1px solid var(--edge);border-radius:8px;padding:10px 14px;font-family:'Syne',sans-serif;font-size:13px;color:var(--text);outline:none}} .ai-send{{background:linear-gradient(135deg,var(--cyan2),rgba(0,180,217,.6));border:none;border-radius:8px;padding:10px 18px;color:#000;font-family:'Syne',sans-serif;font-size:12px;font-weight:700;cursor:pointer;white-space:nowrap}}
.corr-head,.corr-row{{display:grid;grid-template-columns:1fr 1fr 80px 80px}} .corr-head{{padding:10px 24px;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:var(--text3);border-bottom:1px solid var(--edge)}} .corr-row{{padding:14px 24px;border-bottom:1px solid rgba(26,51,85,.4);font-size:13px;cursor:pointer;transition:background .2s;align-items:center}} .corr-row:hover{{background:rgba(0,229,255,.03)}} .cr-service{{color:var(--cyan);font-weight:600}} .cr-type{{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--text2)}} .cr-sev{{font-size:10px;font-weight:700;padding:2px 8px;border-radius:4px;text-align:center}} .bar-container{{height:4px;background:var(--edge);border-radius:4px;overflow:hidden}} .bar-fill{{height:100%;border-radius:4px}}
.modal-overlay{{position:fixed;inset:0;background:rgba(2,4,8,.78);backdrop-filter:blur(10px);z-index:200;display:none;align-items:center;justify-content:center;padding:24px}} .modal-overlay.open{{display:flex}} .modal{{width:min(520px,100%);background:var(--card);border:1px solid var(--rim);border-radius:14px;padding:26px;box-shadow:0 24px 80px rgba(0,0,0,.45);position:relative}} .modal-close{{position:absolute;right:16px;top:14px;background:transparent;border:0;color:var(--text2);font-size:20px;cursor:pointer}} .modal-title{{font-family:'Bebas Neue',sans-serif;font-size:36px;letter-spacing:2px;color:#fff}} .modal-sub{{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--cyan);margin-bottom:18px}} .modal-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:16px 0}} .modal-field{{background:rgba(0,0,0,.24);border:1px solid var(--edge);border-radius:8px;padding:12px}} .mf-label{{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--text3);margin-bottom:6px}} .mf-val{{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--text)}} .mf-val.red{{color:var(--red)}} .mf-val.amber{{color:var(--amber)}} .mf-val.green{{color:var(--green)}} .toast-container{{position:fixed;right:24px;bottom:96px;display:flex;flex-direction:column;gap:8px;z-index:300}} .toast{{transform:translateX(130%);transition:transform .35s ease;background:var(--card);border:1px solid var(--rim);border-radius:8px;padding:12px 16px;font-size:12px;color:var(--text);box-shadow:0 12px 40px rgba(0,0,0,.35)}} .toast.show{{transform:translateX(0)}} .float-btns{{position:fixed;right:24px;bottom:24px;display:flex;gap:10px;z-index:50}} .fab{{border-radius:10px;padding:12px 16px;font-size:12px;font-weight:700;cursor:pointer;box-shadow:0 12px 40px rgba(0,0,0,.25)}} .fab-primary{{background:var(--cyan);color:#001014}} .fab-secondary{{background:var(--card);border:1px solid var(--rim);color:var(--text)}} .anim{{animation:rise .7s ease both}} .anim-2{{animation-delay:.08s}} .anim-3{{animation-delay:.16s}} .anim-4{{animation-delay:.24s}} .anim-5{{animation-delay:.32s}} @keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(max-width:1100px){{.wrapper{{padding:88px 22px 60px}}.main-grid,.bottom-grid{{grid-template-columns:1fr}}.kpi-row{{grid-template-columns:repeat(2,1fr)}}.event-row,.event-row-head{{grid-template-columns:78px 30px 1fr 120px 90px}}}}
@media(max-width:760px){{nav{{padding:0 18px}}.nav-status span:not(.nav-time){{display:none}}.hero{{grid-template-columns:1fr}}.system-health{{align-items:flex-start}}.kpi-row{{grid-template-columns:1fr}}.event-row,.event-row-head{{grid-template-columns:80px 30px 1fr}}.event-row>*:nth-child(4),.event-row>*:nth-child(5),.event-row-head>*:nth-child(4),.event-row-head>*:nth-child(5){{display:none}}.corr-head,.corr-row{{grid-template-columns:1fr 1fr 76px}}.corr-head span:last-child,.corr-row>div:last-child{{display:none}}.float-btns{{left:18px;right:18px;justify-content:flex-end}}}}
</style>
</head>
<body>
<div class="bg-mesh"></div><div class="scanlines"></div><div class="grid-bg"></div>
<nav>
  <div class="nav-logo"><div class="logo-pulse"></div>PulseOps</div>
  <div class="nav-status"><span><span class="status-dot"></span>ALL SYSTEMS MONITORED</span><span>PIPELINE HEALTHY</span><span class="nav-time" id="navTime">{generated_at}</span></div>
</nav>
<div class="wrapper z1">
  <section class="hero anim">
    <div>
      <div class="hero-eyebrow">Operational Intelligence Platform</div>
      <h1 class="hero-title">Pulse<span>Ops</span></h1>
      <div class="hero-sub">Real-time incident correlation, telemetry validation, and AI-guided operations</div>
    </div>
    <div class="system-health">
      <div class="health-label">System Health</div>
      <div class="health-ring">
        <svg viewBox="0 0 100 100"><circle class="track" cx="50" cy="50" r="40"></circle><circle id="healthCircle" class="fill" cx="50" cy="50" r="40"></circle></svg>
        <div class="health-num"><span style="font-family:'Bebas Neue',sans-serif;font-size:26px;color:var(--green)">{health}</span><span>HEALTH</span></div>
      </div>
    </div>
  </section>
  <div class="kpi-row anim anim-2">
    <div class="kpi-card blue"><div class="kpi-label">Operational Events</div><div class="kpi-num" id="kpiEvents">{len(events)}</div><div class="kpi-sub"><span class="kpi-trend trend-up">+12%</span>live telemetry</div></div>
    <div class="kpi-card amber"><div class="kpi-label">Correlated Incidents</div><div class="kpi-num" id="kpiIncidents">{len(correlations)}</div><div class="kpi-sub"><span class="kpi-trend trend-flat">ACTIVE</span>deployment impact</div></div>
    <div class="kpi-card red"><div class="kpi-label">Critical Events</div><div class="kpi-num" id="kpiCorr">{critical_count}</div><div class="kpi-sub"><span class="kpi-trend trend-down">P1</span>needs review</div></div>
    <div class="kpi-card green"><div class="kpi-label">AI Insights Generated</div><div class="kpi-num" id="kpiAI">{len(insights)}</div><div class="kpi-sub"><span class="kpi-trend trend-up">READY</span>recommendations</div></div>
  </div>
  <div class="main-grid anim anim-3">
    <div class="panel">
      <div class="panel-head"><div class="panel-title"><div class="panel-icon pi-cyan">EV</div>Live Event Feed</div><span class="panel-badge pb-cyan">LIVE</span></div>
      <div class="event-row-head"><span>EVENT ID</span><span></span><span>DESCRIPTION</span><span>SERVICE</span><span>STATUS</span></div>
      <div class="event-feed" id="eventFeed">{event_rows(events)}</div>
    </div>
    <div class="panel">
      <div class="panel-head"><div class="panel-title"><div class="panel-icon pi-red">AL</div>Active Incidents</div><span class="panel-badge pb-red">3 OPEN</span></div>
      <div class="incident-list">
        <div class="inc-card inc-critical" onclick="openModal('EVT-001','P1 - System Instability','checkout-service','CRITICAL','GitHub and Sentry correlation detected. Deployment preceded error spike by 8 minutes.','92%')"><div class="inc-top"><div><div class="inc-id">INC-001 &middot; P1</div><div class="inc-title">Checkout service instability</div></div><div class="inc-sev sev-critical">CRITICAL</div></div><div class="inc-service">// checkout-service &middot; payment-api</div><div class="inc-bar"><div class="inc-bar-fill fill-red" style="width:92%"></div></div><div class="inc-footer"><span>Impact: 92% of checkout flow</span><span>14 mins ago</span></div></div>
        <div class="inc-card inc-warning" onclick="openModal('EVT-005','P2 - Auth Degradation','user-auth','HIGH','Application errors detected post-deploy. Error rate elevated by 340%.','45%')"><div class="inc-top"><div><div class="inc-id">INC-002 &middot; P2</div><div class="inc-title">Auth service error spike</div></div><div class="inc-sev sev-high">HIGH</div></div><div class="inc-service">// user-auth &middot; sentry</div><div class="inc-bar"><div class="inc-bar-fill fill-amber" style="width:45%"></div></div><div class="inc-footer"><span>Error rate: +340%</span><span>31 mins ago</span></div></div>
        <div class="inc-card inc-resolved" onclick="openModal('EVT-008','Resolved - Payment Latency','payment-api','RESOLVED','Auto-resolved after rollback. P95 latency returned to baseline.','100%')"><div class="inc-top"><div><div class="inc-id">INC-003 &middot; RESOLVED</div><div class="inc-title">Payment API high latency</div></div><div class="inc-sev sev-resolved">RESOLVED</div></div><div class="inc-service">// payment-api &middot; cloudwatch</div><div class="inc-bar"><div class="inc-bar-fill fill-green" style="width:100%"></div></div><div class="inc-footer"><span>MTTR: 12 minutes</span><span>1h 02m ago</span></div></div>
      </div>
    </div>
  </div>
  <div class="bottom-grid anim anim-4">
    <div class="panel">
      <div class="panel-head"><div class="panel-title"><div class="panel-icon pi-green">SL</div>SLA Tracking</div><span class="panel-badge pb-green">LIVE</span></div>
      <div class="sla-grid">
        <div class="sla-row"><div class="sla-top"><div class="sla-name">auth-service</div><div class="sla-pct" style="color:var(--green)">99.9%</div></div><div class="sla-track"><div class="sla-fill" style="width:99.9%;background:linear-gradient(90deg,var(--green),var(--cyan));box-shadow:0 0 8px var(--green)"></div></div><div class="sla-sub"><span>Target: 99.5%</span><span>above target</span></div></div>
        <div class="sla-row"><div class="sla-top"><div class="sla-name">checkout-service</div><div class="sla-pct" style="color:var(--red)">94.2%</div></div><div class="sla-track"><div class="sla-fill" style="width:94.2%;background:linear-gradient(90deg,var(--red),var(--amber));box-shadow:0 0 8px var(--red)"></div></div><div class="sla-sub"><span>Target: 99.5%</span><span style="color:var(--red)">SLA BREACH</span></div></div>
        <div class="sla-row"><div class="sla-top"><div class="sla-name">payment-api</div><div class="sla-pct" style="color:var(--amber)">97.8%</div></div><div class="sla-track"><div class="sla-fill" style="width:97.8%;background:linear-gradient(90deg,var(--amber),var(--green));box-shadow:0 0 8px var(--amber)"></div></div><div class="sla-sub"><span>Target: 99.5%</span><span style="color:var(--amber)">below target</span></div></div>
        <div class="sla-row"><div class="sla-top"><div class="sla-name">data-pipeline</div><div class="sla-pct" style="color:var(--cyan)">100%</div></div><div class="sla-track"><div class="sla-fill" style="width:100%;background:linear-gradient(90deg,var(--cyan),var(--green));box-shadow:0 0 8px var(--cyan)"></div></div><div class="sla-sub"><span>Target: 99.5%</span><span style="color:var(--green)">PERFECT</span></div></div>
        <div class="sla-row"><div class="sla-top"><div class="sla-name">reporting-engine</div><div class="sla-pct" style="color:var(--green)">96.1%</div></div><div class="sla-track"><div class="sla-fill" style="width:96.1%;background:linear-gradient(90deg,var(--green),var(--cyan));box-shadow:0 0 6px var(--green)"></div></div><div class="sla-sub"><span>Target: 95.0%</span><span>above target</span></div></div>
      </div>
    </div>
    <div class="panel ai-panel">
      <div class="panel-head"><div class="panel-title"><div class="panel-icon pi-purple">AI</div>Ask PulseOps - AI Layer</div><span class="panel-badge" style="border-color:rgba(124,77,255,.3);color:var(--purple);background:rgba(124,77,255,.08)">RAG &middot; AI</span></div>
      <div class="ai-messages" id="aiMessages">{insight_markup(insights)}</div>
      <div class="ai-input-row"><input class="ai-input" id="aiInput" type="text" placeholder="Ask about incidents, correlations, SLA..." onkeydown="if(event.key==='Enter')sendAI()"/><button class="ai-send" onclick="sendAI()">ASK</button></div>
    </div>
  </div>
  <div class="panel anim anim-5" style="margin-bottom:20px;">
    <div class="panel-head"><div class="panel-title"><div class="panel-icon pi-amber">CO</div>Deployment &rarr; Incident Correlations</div><span class="panel-badge pb-amber">{len(correlations)} CHAINS DETECTED</span></div>
    <div class="corr-head"><span>DEPLOYMENT EVENT</span><span>AFFECTED SERVICE</span><span>SEVERITY</span><span>IMPACT</span></div>
    {correlation_rows(correlations)}
  </div>
</div>
<div class="modal-overlay" id="modalOverlay" onclick="if(event.target===this)closeModal()">
  <div class="modal"><button class="modal-close" onclick="closeModal()">x</button><div class="modal-title" id="mTitle">-</div><div class="modal-sub" id="mSub">-</div><div class="modal-row"><div class="modal-field"><div class="mf-label">Event ID</div><div class="mf-val" id="mId">-</div></div><div class="modal-field"><div class="mf-label">Severity</div><div class="mf-val" id="mSev">-</div></div><div class="modal-field"><div class="mf-label">Impact</div><div class="mf-val" id="mImpact">-</div></div></div><div class="modal-field" style="margin-bottom:16px;"><div class="mf-label">AI Analysis</div><div style="color:var(--text);font-size:13px;line-height:1.6;margin-top:6px;" id="mAnalysis">-</div></div><div style="display:flex;gap:10px;margin-top:20px;"><button onclick="showToast('Opening runbook...');closeModal();" style="flex:1;padding:11px;border-radius:8px;background:var(--cyan-glow);border:1px solid rgba(0,229,255,.3);color:var(--cyan);font-family:'Syne',sans-serif;font-weight:700;font-size:13px;cursor:pointer;">View Runbook</button><button onclick="showToast('Incident logged to ServiceNow');closeModal();" style="flex:1;padding:11px;border-radius:8px;background:var(--edge);border:1px solid var(--rim);color:var(--text);font-family:'Syne',sans-serif;font-weight:600;font-size:13px;cursor:pointer;">Escalate to ServiceNow</button></div></div>
</div>
<div class="toast-container" id="toastContainer"></div>
<div class="float-btns z1"><div class="fab fab-primary" onclick="showToast('Refreshing data pipeline...')">Refresh Pipeline</div><div class="fab fab-secondary" onclick="showToast('Generating PDF report...')">Export Report</div></div>
<script>
function updateClock(){{const n=new Date();document.getElementById('navTime').textContent=String(n.getUTCHours()).padStart(2,'0')+':'+String(n.getUTCMinutes()).padStart(2,'0')+':'+String(n.getUTCSeconds()).padStart(2,'0')+' UTC';}}
setInterval(updateClock,1000);updateClock();
function openModal(id,title,svc,sev,analysis,impact){{document.getElementById('mTitle').textContent=title;document.getElementById('mSub').textContent='// '+svc;document.getElementById('mId').textContent=id;const s=document.getElementById('mSev');s.textContent=sev;s.className='mf-val '+(sev==='CRITICAL'?'red':sev==='HIGH'?'amber':'green');document.getElementById('mImpact').textContent=impact;document.getElementById('mAnalysis').textContent=analysis;document.getElementById('modalOverlay').classList.add('open');}}
function closeModal(){{document.getElementById('modalOverlay').classList.remove('open');}}
function showToast(msg){{const tc=document.getElementById('toastContainer');const t=document.createElement('div');t.className='toast';t.textContent=msg;tc.appendChild(t);requestAnimationFrame(()=>t.classList.add('show'));setTimeout(()=>{{t.classList.remove('show');setTimeout(()=>t.remove(),400);}},3000);}}
const aiResponses=["checkout-service shows the strongest deployment-impact chain. Review deployment logs and validate rollback readiness.","Two services are below target SLA: checkout-service at 94.2% and payment-api at 97.8%.","Data quality checks pass with 100% validation and no duplicate event ids.","Recommended action: rollback review, Sentry monitoring, and ServiceNow escalation for the P1 chain."];
let aiIdx=0;
function sendAI(){{const inp=document.getElementById('aiInput');const q=inp.value.trim();if(!q)return;const msgs=document.getElementById('aiMessages');msgs.innerHTML += '<div class="ai-msg" style="flex-direction:row-reverse;"><div class="ai-avatar av-sys">YOU</div><div class="ai-bubble sys" style="border-radius:10px 0 10px 10px;text-align:right;">'+q+'<span class="ai-ts">now</span></div></div>';setTimeout(()=>{{msgs.innerHTML += '<div class="ai-msg"><div class="ai-avatar av-ai">AI</div><div class="ai-bubble ai">'+aiResponses[aiIdx++%aiResponses.length]+'<span class="ai-ts">PulseOps AI</span></div></div>';msgs.scrollTop=msgs.scrollHeight;}},350);inp.value='';msgs.scrollTop=msgs.scrollHeight;}}
</script>
</body>
</html>
"""


def main() -> None:
    st.set_page_config(page_title="PulseOps", page_icon="PO", layout="wide", initial_sidebar_state="collapsed")
    st.markdown(
        """
        <style>
        #MainMenu, header, footer { visibility: hidden; }
        .stApp { background: #020408; }
        .block-container { padding: 0; max-width: none; }
        iframe { display: block; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    payload = build_pipeline()
    components.html(render_dashboard(payload), height=1320, scrolling=True)


if __name__ == "__main__":
    main()
