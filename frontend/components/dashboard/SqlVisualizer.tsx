import { AnimatedSQL } from "@/components/ui/AnimatedSQL";

export function SqlVisualizer({ sql }: { sql: string }) {
  return (
    <section className="panel">
      <div className="panel-head">
        <div>
          <span className="panel-kicker">Coral query</span>
          <h2>Cross-source SQL</h2>
        </div>
        <span className="pill">GitHub + Sentry + Slack</span>
      </div>
      <AnimatedSQL sql={sql} />
    </section>
  );
}
