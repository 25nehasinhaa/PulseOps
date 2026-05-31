"use client";

import { Search } from "lucide-react";

export function QueryBar({
  value,
  loading,
  onChange,
  onSubmit
}: {
  value: string;
  loading: boolean;
  onChange: (value: string) => void;
  onSubmit: () => void;
}) {
  return (
    <div className="query-bar">
      <Search size={18} />
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter") onSubmit();
        }}
        placeholder="Ask: Why did our API go down last Tuesday?"
      />
      <button onClick={onSubmit} disabled={loading || value.trim().length < 3}>
        Ask CoralOps
      </button>
    </div>
  );
}
