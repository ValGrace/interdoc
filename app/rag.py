# handles prompt building and LLM call

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def build_prompt(question: str, chunks: list[str], metadatas: list[dict]):
    blocks = []

    for i, (chunk, meta) in enumerate(zip(chunks, metadatas), start=1):
        blocks.append(f"[Source {i}: {meta["source"]}, chunk {meta["chunk_index"]}]\n{chunk}")
    
    context = "\n\n".join(blocks)
    return (
        "Answer the question using only the context below."
        "Cite so, say you dont have enough information - do not guess.\n\nrces using [Source N]. If the answer is not in the"
        "context, say you dont have enough information - do not guess.\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    )

def generate_response(question: str, search_results: dict):
    chunks = search_results["documents"][0]
    metadatas = search_results["metadatas"][0]
    if not chunks:
        return {
            "answer": "No documents have been uploaded yet",
            "sources": []
        }
    prompt = build_prompt(question, chunks, metadatas)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    answer_text = response.choices[0].message.context
    sources = [{"sources": m["source"], "chunk_index": m["chunk_index"]} for m in metadatas]

    return {"answer": answer_text, "sources": sources}