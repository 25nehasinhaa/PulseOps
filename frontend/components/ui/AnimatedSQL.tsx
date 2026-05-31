"use client";

export function AnimatedSQL({ sql }: { sql: string }) {
  return (
    <pre className="sql-block">
      <code>{sql || "SELECT * FROM github.pull_requests JOIN sentry.issues JOIN slack.messages LIMIT 20;"}</code>
    </pre>
  );
}
