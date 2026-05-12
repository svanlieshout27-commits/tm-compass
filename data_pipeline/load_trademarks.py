import json, os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(".env")
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])

def normalize(tm):
    return {
        "application_number": str(tm.get("id")),
        "mark_text": tm.get("markName") or "",
        "mark_type": tm.get("markType"),
        "office": tm.get("office"),
        "applicant_name": tm.get("applicant"),
        "filing_date": tm.get("applicationDate"),
        "status": tm.get("status"),
        "nice_classes": tm.get("niceClasses", []),
        "goods_services": tm.get("goodsAndServices"),
        "source_url": tm.get("sourceUrl") or "",
    }

batch = []
for line in Path("data/raw/trademarks.jsonl").open(encoding="utf-8"):
    row = normalize(json.loads(line))
    if not row["application_number"] or not row["mark_text"]:
        continue
    batch.append(row)
    if len(batch) >= 500:
        sb.table("trademarks").upsert(batch, on_conflict="application_number").execute()
        batch.clear()
if batch:
    sb.table("trademarks").upsert(batch, on_conflict="application_number").execute()
print("done")