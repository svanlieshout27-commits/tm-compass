import os
from supabase import create_client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
oai = OpenAI()

def build_text(row):
    classes = ", ".join(str(c) for c in (row.get("nice_classes") or []))
    return f"{row['mark_text']} | classes {classes} | {row.get('goods_services') or ''}"[:8000]

PAGE = 200
offset = 0
while True:
    rows = (sb.table("trademarks")
              .select("id, mark_text, nice_classes, goods_services")
              .is_("embedding", "null")
              .range(offset, offset + PAGE - 1)
              .execute()).data
    if not rows:
        break
    texts = [build_text(r) for r in rows]
    resp = oai.embeddings.create(model="text-embedding-3-small", input=texts)
    for r, e in zip(rows, resp.data):
        sb.table("trademarks").update({"embedding": e.embedding}).eq("id", r["id"]).execute()
    print(f"embedded {offset}..{offset+len(rows)}")
    offset += PAGE