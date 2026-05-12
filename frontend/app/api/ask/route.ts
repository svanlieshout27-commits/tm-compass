import { NextRequest, NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";
import OpenAI from "openai";
import Anthropic from "@anthropic-ai/sdk";

const sb = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_KEY!);
const oai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

export async function POST(req: NextRequest) {
  try {
    const { query } = await req.json();

    const emb = await oai.embeddings.create({
      model: "text-embedding-3-small",
      input: [query],
    });

    const { data: hits } = await sb.rpc("hybrid_search", {
      query_text: query,
      query_embedding: emb.data[0].embedding,
      match_count: 8,
    });

    const sources = (hits || []).map((h: any, i: number) => ({
      n: i + 1,
      ...h,
    }));

    const context = sources
      .map((s: any) =>
        `[${s.n}] ${s.mark_text} (${s.application_number}, filed ${s.filing_date}, classes ${s.nice_classes}, applicant ${s.applicant_name})`
      )
      .join("\n");

    const msg = await anthropic.messages.create({
     model: "claude-sonnet-4-6",
      max_tokens: 800,
      messages: [
        {
          role: "user",
          content: `You are a trademark research assistant. Answer the question using ONLY the sources below. Cite sources with [n] inline. If sources don't contain the answer, say so clearly.

Sources:
${context}

Question: ${query}`,
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