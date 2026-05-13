# TM Compass — EU Trademark RAG Assistant

**Live demo:** [tmcompass.vercel.app](https://tmcompass.vercel.app)

Natural-language search over EU trademark filings with cited answers. Ask in plain English — get sourced results from 3,500+ EUIPO-style trademark records.

---

## What it does

Type a question like *"Which trademark classes does Nike cover?"* or *"Has anyone registered a mark called Aurora in class 25 since 2020?"* and TM Compass returns a Claude-generated answer with inline citations and a source list showing the applicant, filing date, and Nice classes for each result.

## Architecture

```
User query
    │
    ├─► OpenAI text-embedding-3-small  →  1536-dim vector
    │
    ├─► Keyword extraction (stop-word filter + OR logic)
    │
    └─► Supabase hybrid_search() RPC
            ├─ pgvector cosine similarity   (semantic)
            └─ BM25 full-text search        (keyword)
                    │
                    └─ Reciprocal Rank Fusion (RRF) → top 8 results
                            │
                            └─► Claude claude-sonnet-4-6
                                    └─► Cited answer + source cards
```

**Hybrid search** combines vector similarity (catches synonyms and paraphrases) with BM25 full-text ranking (catches exact brand names), merged via Reciprocal Rank Fusion. This gives better recall than either approach alone.

## Tech stack

| Layer | Tool |
|-------|------|
| Frontend | Next.js 14 (App Router) |
| Database | Supabase (PostgreSQL + pgvector) |
| Embeddings | OpenAI `text-embedding-3-small` |
| LLM | Anthropic `claude-sonnet-4-6` |
| Full-text search | PostgreSQL `tsvector` / `to_tsquery` |
| Hosting | Vercel |

## Data

3,553 synthetic EUIPO-style trademark records across Nice classes 9, 25, 35, and 41. Each record includes mark name, applicant, filing date, status, and goods/services description. Embeddings were built from concatenated mark text + class + goods fields.

> **Note:** This is a portfolio demo built on synthetic data. It is not a substitute for real trademark clearance searches on EUIPO TMview or national registers.

## Running locally

```bash
git clone https://github.com/svanlieshout27-commits/tm-compass
cd tm-compass/frontend
npm install
```

Create `.env.local`:

```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

```bash
npm run dev
```

## Key implementation details

- **Keyword extraction** strips stop words and joins with `|` (OR) to avoid BM25 AND-logic failures on multi-word queries
- **Embedding serialization** passes vectors as strings `"[x1,x2,...]"` to Supabase RPC — raw JS arrays are silently miscast
- **`export const dynamic = "force-dynamic"`** prevents Next.js from pre-rendering the API route at build time
- All SDK clients initialised inside the request handler, not at module level

## About

Built by [Sebastiaan van Lieshout](https://www.linkedin.com/in/sebastiaan-van-lieshout) — Brand Protection Specialist transitioning into AI engineering.

Portfolio project #2. See also [CounterCheck](https://countercheck-eight.vercel.app) — hybrid ML + LLM counterfeit listing detector.
