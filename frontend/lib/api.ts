import type { IncidentsResponse, ReadinessResponse, StreamEvent } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8010";

export async function fetchIncidents(): Promise<IncidentsResponse> {
  const response = await fetch(`${API_URL}/incidents`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch incidents: ${response.status}`);
  }
  return response.json();
}

export async function fetchReadiness(): Promise<ReadinessResponse> {
  const response = await fetch(`${API_URL}/readiness`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Failed to fetch readiness: ${response.status}`);
  }
  return response.json();
}

export async function streamEndpoint(
  path: "/diagnose" | "/query" | "/postmortem",
  body: Record<string, unknown>,
  onEvent: (event: StreamEvent) => void
) {
  const response = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });

  if (!response.ok || !response.body) {
    throw new Error(`Stream failed: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop() || "";

    for (const raw of events) {
      const line = raw.split("\n").find((item) => item.startsWith("data: "));
      if (!line) continue;
      onEvent(JSON.parse(line.slice(6)) as StreamEvent);
    }
  }
}
