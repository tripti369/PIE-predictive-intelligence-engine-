"""
/api/knowledge
==============
RAG-style search across the markdown knowledge base in data/knowledge/,
used by the frontend's "Ask Enterprise AI" chat box.
"""

from fastapi import APIRouter, Query
import os

from dotenv import load_dotenv

try:
    from google import genai
except ImportError:  # Optional locally; deployment installs backend requirements.
    genai = None

from app.agents.rag_agent import RAGAgent

router = APIRouter()
rag_agent = RAGAgent()
rag_agent.build_index()
load_dotenv()


def _gemini_answer(question: str, context: str) -> str | None:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here" or genai is None:
        return None

    prompt = (
        "You are the business intelligence assistant for the Predictive Intelligence Engine. "
        "Answer using the retrieved local evidence below. Be concise and do not invent metrics. "
        "If the evidence is insufficient, say so clearly.\n\n"
        f"Retrieved evidence:\n{context}\n\nQuestion: {question}"
    )
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        return response.text.strip() if response.text else None
    except Exception:
        return None


@router.get("/knowledge")
def knowledge(q: str = Query("", description="Natural language question")):
    if not q.strip():
        return {"query": q, "results": []}
    return rag_agent.answer(q, top_k=3)


@router.get("/ask")
def ask(q: str = Query("", description="Question about the business data")):
    if not q.strip():
        return {"question": q, "answer": "", "ai_engine": "none", "sources": []}

    rag_result = rag_agent.answer(q, top_k=3)
    sources = rag_result.get("results", [])
    context = "\n\n".join(
        f"Source: {item['doc_id']}\n{item['excerpt']}" for item in sources
    )
    answer = _gemini_answer(q, context)
    return {
        "question": q,
        "answer": answer or (sources[0]["excerpt"] if sources else "No evidence found."),
        "ai_engine": "Gemini AI" if answer else "Local RAG",
        "sources": sources,
    }
