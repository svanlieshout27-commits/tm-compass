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
    <div style={{ minHeight: "100vh", background: "#f0f2f5", fontFamily: "sans-serif", display: "flex", flexDirection: "column" }}>
      <main style={{ maxWidth: 720, width: "100%", margin: "0 auto", padding: "48px 16px 32px", flex: 1 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>TM Compass</h1>
        <p style={{ color: "#666", marginBottom: 32 }}>Natural-language search over EU trademark filings with cited answers.</p>

        <div style={{ background: "#fff", border: "1px solid #e0e0e0", borderRadius: 10, padding: "24px 24px 28px" }}>
          <form onSubmit={handleSubmit} style={{ display: "flex", gap: 8, marginBottom: 0 }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Has anyone registered Aurora in class 25 since 2020?"
              style={{ flex: 1, padding: "10px 14px", border: "1px solid #ccc", borderRadius: 8, fontSize: 14 }}
            />
            <button
              type="submit"
              disabled={loading}
              style={{ background: "#2563eb", color: "#fff", padding: "10px 20px", border: "none", borderRadius: 8, fontSize: 14, cursor: "pointer" }}
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </form>
        </div>

        {answer && (
          <div style={{ background: "#eff6ff", border: "1px solid #bfdbfe", borderRadius: 8, padding: 20, marginTop: 20 }}>
            <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 8, color: "#1e40af" }}>Answer</h2>
            <p style={{ fontSize: 14, lineHeight: 1.7, whiteSpace: "pre-wrap" }}>{answer}</p>
          </div>
        )}

        {sources.length > 0 && (
          <div style={{ marginTop: 24 }}>
            <h2 style={{ fontSize: 15, fontWeight: 600, marginBottom: 12, color: "#374151" }}>Sources</h2>
            {sources.map((s) => (
              <div key={s.n} style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 8, padding: 16, marginBottom: 10 }}>
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

      <footer style={{ maxWidth: 720, width: "100%", margin: "0 auto", padding: "20px 16px 40px", textAlign: "center" }}>
        <p style={{ fontSize: 12, color: "#6b7280", lineHeight: 1.6 }}>
          TM Compass is a portfolio demo built on synthetic EUIPO-style data. It is intended to illustrate a hybrid RAG architecture, not as a production legal research tool. Results should not be relied upon for trademark clearance or legal advice.
        </p>
        <p style={{ fontSize: 12, color: "#6b7280", marginTop: 8 }}>
          Built by{" "}
          <a href="https://www.linkedin.com/in/sebastiaan-van-lieshout" target="_blank" rel="noopener noreferrer" style={{ color: "#2563eb" }}>
            Sebastiaan van Lieshout
          </a>{" "}
          — Brand Protection Specialist transitioning into AI engineering.
        </p>
      </footer>
    </div>
  );
}
