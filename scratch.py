from app.vectorstore import search_chunks

results = search_chunks("What is data governance?", top_k=3)

for doc, meta, dist in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
    ):
    print(f"[{meta['source']} chunk {meta['chunk_index']}] (distances={dist:.2f})")
    print(doc[:150] )


