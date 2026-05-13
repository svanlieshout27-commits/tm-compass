export const dynamic = "force-dynamic";
import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
import OpenAI from "openai";
import Anthropic from "@anthropic-ai/sdk";

function extractKeywords(query: string): string {
  const stopWords = new Set([
    'what','which','who','where','when','how','why',
    'has','have','had','is','are','was','were','be','been','do','does','did',
    'the','a','an','in','of','for','on','with','to','by','from','at',
    'and','or','but','any','all','some','their','its','me','my',
    'show','tell','list','find','give','please','search',
    'trademark','trademarks','mark','marks','filing','filings',
    'filed','registered','register','since','after','before','about',
  ]);
  const keywords = query
    .toLowerCase()
    .replace(/[^a-z0-9 ]/g, ' ')
    .split(/\s+/)
    .filter(w => w.length > 1 && !stopWords.has(w));
  return keywords.length > 0
    ? keywords.join(' | ')
    : query.toLowerCase().replace(/[^a-z0-9]/g, ' ').trim();
}

export async function POST(req: NextRequest) {
  try {
    const sb = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!);
    const oai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
    const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

    const { query } = await req.json();

    const emb = await oai.embeddings.create({
      model: "text-embedding-3-small",
      input: [query],
    });

    const keywords = extractKeywords(query);

    const { data: hits, error: rpcError } = await sb.rpc("hybrid_search", {
      query_text: keywords,
      query_embedding: `[${emb.data[0].embedding.join(",")}]`,
      match_count: 8,
    });

    if (rpcError) console.error("RPC Error:", rpcError);

    const sources = (hits || []).map((h: any, i: number) => ({
      n: i + 1,
      ...h,
    }));

    const context = sources
      .map((s: any) =>
        `[${s.n}] ${s.mark_text} (${s.application_number}, filed ${s.filing_date}, classes ${(s.nice_classes||[]).join(',')}, applicant ${s.applicant_name})`
      )
      .join("\n");

    const msg = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 800,
      messages: [
        {
          role: "user",
          content: `You are a trademark research assistant. Answer the question using ONLY the sources below. Cite sources with [n] inline. If the sources don't contain the answer, say so clearly.\n\nSources:\n${context}\n\nQuestion: ${query}`,
        },
      ],
    });

    const answer = msg.content[0].type === "text" ? msg.content[0].text : "";
    return NextResponse.json({ answer, sources });

  } catch (error: any) {
    console.error("API Error:", error?.message || error);
    return NextResponse.json({ error: error?.message || "Unknown error" }, { status: 500 });
  }
}
