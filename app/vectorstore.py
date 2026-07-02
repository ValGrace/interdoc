import chromadb
from chromadb.utils import embedding_functions

# persistent storage (chromadb is a vector database)
client = chromadb.PersistentClient(path="./data/chroma_db")

# embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.get_or_create_collection(name="documents")

def add_chunks(doc_id: str, chunks: list[str]):
    # create a unique id for every chunk
    ids = [f"{doc_id} {i}" for i in range(len(chunks))]
    metadatas = [{"source": doc_id, "chunk_index": i} for i in range(len(chunks))]

    collection.add(documents=chunks, metadatas=metadatas, ids=ids)

    return len(chunks)
# search chunks() - finding the closest chunks to a question

def search_chunks(query: str, top_k: int = 4):
    return collection.query(query_texts=[query], n_results=top_k)


