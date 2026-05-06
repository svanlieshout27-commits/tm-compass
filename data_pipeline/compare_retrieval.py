from search import hybrid_search
from test_search import search as vector_only

QUERIES = [
    "Aurora",                                # proper noun — hybrid should win
    "athletic apparel brands",               # concept — both should do well
    "Inditex",                               # applicant lookup — hybrid wins
    "AI training services",                  # concept — vector wins
    "marks filed by NIKE",                   # mixed — hybrid wins
]

for q in QUERIES:
    print(f"\n=== {q} ===")
    print("VECTOR:", [r["mark_text"] for r in vector_only(q, 5)])
    print("HYBRID:", [r["mark_text"] for r in hybrid_search(q, 5)])