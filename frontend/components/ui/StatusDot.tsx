export function StatusDot({ tone = "ok" }: { tone?: "ok" | "warn" | "bad" }) {
  return <span className={`status-dot ${tone}`} aria-hidden="true" />;
}
