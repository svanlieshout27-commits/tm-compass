import os
from supabase import create_client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_KEY"])
oai = OpenAI()

def hybrid_search(query: str, k: int = 10):
    emb = oai.embeddings.create(model="text-embedding-3-small", input=[query]).data[0].embedding
    return sb.rpc("hybrid_search", {
        "query_text": query,
        "query_embedding": emb,
        "match_count": k,
    }).execute().data