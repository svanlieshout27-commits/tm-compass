# TM Compass

Trademark RAG assistant — natural-language Q&A over EUIPO trademark filings with cited sources.

## Status (Weekend 1)
- Data pipeline pulls EU records via TMview API (~5,000 records, classes 9/25/35/41, since 2020).
- Embedded with OpenAI `text-embedding-3-small` (1536-dim) into Supabase pgvector.
- Basic semantic search via `test_search.py` working.

## Next
- Weekend 2: hybrid retrieval (vector + BM25 + RRF).
- Weekend 3: Next.js chat UI + Claude answer synthesis.
- Weekend 4: 30-query eval harness with precision@5 / recall@5.

## Built by
Sebastiaan van Lieshout — Brand Protection Specialist transitioning to AI engineering.