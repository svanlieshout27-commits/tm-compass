"use client";
import { useState } from "react";

type Source = {
  n: number;
  mark_text: string;
  applicant_name: string;
  filing_date: string;
  nice_classes: number[];
  source_url: string;
};

export default function Home() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setAnswer("");
    setSources([]);
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setAnswer(data.answer);
    setSources(data.sources || []);
    setLoading(false);
  }

  return (
    <main style={{ maxWidth: 720, margin: "0 auto", padding: "48px 16px", fontFamily: "sans-serif" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>TM Compass</h1>
      <p style={{ color: "#666", marginBottom: 32 }}>Natural-language search over EU trademark filings with cited answers.</p>
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: 8, marginBottom: 32 }}>
        <input type="text" value={query} onChange={(e) => setQuery(e.target.value)}
          placeholder="Has anyone registered Aurora in class 25 since 2020?"
          style={{ flex: 1, padding: "10px 14px", border: "1px solid #ccc", borderRadius: 8, fontSize: 14 }} />
        <button type="submit" disabled={loading}
          style={{ background: "#2563eb", color: "#fff", padding: "10px 20px", border: "none", borderRadius: 8, fontSize: 14, cursor: "pointer" }}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>
      {answer && (
        <div style={{ background: "#eff6ff", border: "1px solid #bfdbfe", borderRadius: 8, padding: 20, marginBottom: 32 }}>
          <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 8, color: "#1e40af" }}>Answer</h2>
          <p style={{ fontSize: 14, lineHeight: 1.7, whiteSpace: "pre-wrap" }}>{answer}</p>
        </div>
      )}
      {sources.length > 0 && (
        <div>
          <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 12, color: "#374151" }}>Sources</h2>
          {sources.map((s) => (
            <div key={s.n} style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 10 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <span style={{ fontWeight: 600, color: "#2563eb", fontSize: 14 }}>[{s.n}] {s.mark_text}</span>
                {s.source_url && (
                  <a href={s.source_url} target="_blank" rel="noopener noreferrer" style={{ fontSize: 12, color: "#2563eb" }}>View on TMview</a>
                )}
              </div>
              <p style={{ fontSize: 13, color: "#6b7280", marginTop: 4 }}>
                {s.applicant_name} · Filed {s.filing_date} · Classes {(s.nice_classes || []).join(", ")}
              </p>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
