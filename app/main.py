from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ingestion import extract_text, chunk_text
from app.vectorstore import add_chunks, search_chunks
from app.rag import generate_response

app = FastAPI(title="Document Intelligence API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str     
    top_k: int = 4

@app.get("/")
def root():
    return {
        "status": "alive"
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    text = extract_text(file.filename, contents)
    chunks = chunk_text(text)
    n = add_chunks(doc_id=file.filename, chunks=chunks)
    # json response 
    return {
        "filename": file.filename,
        "chunks_created": n
    }

@app.post("/query")
async def query_documents(request: QueryRequest):
    results = search_chunks(request.question, top_k=request.top_k)
    return generate_response(request.question, results)