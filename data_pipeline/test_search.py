import os
from supabase import create_client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
oai = OpenAI()

def search(query, k=10):
    emb = oai.embeddings.create(model="text-embedding-3-small", input=[query]).data[0].embedding
    return sb.rpc("match_trademarks", {"query_embedding": emb, "match_count": k}).execute().data

if __name__ == "__main__":
    for q in [
        "athletic clothing brands registered after 2022",
        "smart watch electronics in class 9",
        "training and education services for AI",
        "luxury fashion houses based in Italy",
    ]:
        print(f"\n--- {q} ---")
        for hit in search(q, 5):
            print(f"  {hit['mark_text']} | {hit['filing_date']} | classes={hit['nice_classes']}")