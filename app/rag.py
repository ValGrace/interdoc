# handles prompt building and LLM call

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = None
if os.getenv("GROQ_API_KEY"):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def build_prompt(question: str, chunks: list[str], metadatas: list[dict]):
    blocks = []

    for i, (chunk, meta) in enumerate(zip(chunks, metadatas), start=1):
        blocks.append(f"[Source {i}: {meta['source']}, chunk {meta['chunk_index']}]\n{chunk}")

    context = "\n\n".join(blocks)
    return (
        "Answer the question using only the context below. "
        "Cite sources using [Source N]. If the answer is not in the context, "
        "say you don't have enough information - do not guess.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )


def generate_response(question: str, search_results: dict):
    chunks = search_results.get("documents", [[]])[0]
    metadatas = search_results.get("metadatas", [[]])[0]
    if not chunks:
        return {
            "answer": "No documents have been uploaded yet",
            "sources": []
        }

    sources = [{"source": m["source"], "chunk_index": m["chunk_index"]} for m in metadatas]

    if client is None:
        return {
            "answer": "The backend is missing GROQ_API_KEY, so I cannot generate a grounded answer yet.",
            "sources": sources
        }

    try:
        prompt = build_prompt(question, chunks, metadatas)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        answer_text = response.choices[0].message.content
    except Exception:
        answer_text = "The answer service is temporarily unavailable. Please try again in a moment."

    return {"answer": answer_text, "sources": sources}