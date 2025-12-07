from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import uuid  # For generating unique IDs for Qdrant points
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Conditional imports ---
try:
    from openai import AsyncOpenAI  # Gemini is OpenAI-compatible
except ImportError:
    AsyncOpenAI = None

try:
    import cohere
except ImportError:
    cohere = None

try:
    from qdrant_client import QdrantClient, models
except ImportError:
    QdrantClient = None
    models = None

# --- API Keys and Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL")  # Optional, if needed
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
QDRANT_API_URL = os.getenv("QDRANT_API_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Initialize Gemini client
gemini_client = None
cohere_client = None
qdrant_client = None

# Embedding dimension
EMBEDDING_DIM = 1536
COLLECTION_NAME = "book_chunks"

# --- Initialize Gemini Client ---
if GEMINI_API_KEY and AsyncOpenAI:
    gemini_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)
    print("Gemini client initialized.")
elif COHERE_API_KEY and cohere:
    cohere_client = cohere.Client(api_key=COHERE_API_KEY)
    EMBEDDING_DIM = 768
    print("Cohere client initialized.")
else:
    print("Warning: Neither Gemini nor Cohere API key is configured. Embedding and generation will not work.")

# --- Initialize Qdrant client ---
if QDRANT_API_URL and QDRANT_API_KEY and QdrantClient:
    qdrant_client = QdrantClient(url=QDRANT_API_URL, api_key=QDRANT_API_KEY)
    print("Qdrant client initialized.")
else:
    print("Warning: Qdrant client not initialized. Qdrant URL or API key missing.")

# --- FastAPI app setup ---
app = FastAPI(
    title="RAG Chatbot Backend",
    description="Backend for the RAG chatbot using Gemini & Cohere",
    version="1.0.0",
)

origins = ["http://localhost:3000", "http://localhost:8000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Models ---
class IngestRequest(BaseModel):
    chunks: List[str]

class QueryRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    chat_history: Optional[List[Dict[str, str]]] = None

class QueryResponse(BaseModel):
    answer: str

# --- Endpoints ---
@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot Backend is running!"}

@app.post("/api/ingest")
async def ingest_content(request: IngestRequest):
    if not qdrant_client or (not gemini_client and not cohere_client):
        raise HTTPException(status_code=500, detail="Embedding model or Qdrant not initialized.")

    try:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=EMBEDDING_DIM, distance=models.Distance.COSINE),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create Qdrant collection: {e}")

    points = []
    for i, chunk in enumerate(request.chunks):
        embedding = None
        if gemini_client:
            response = gemini_client.embeddings.create(input=[chunk], model="text-embedding-3-small")
            embedding = response.data[0].embedding
        elif cohere_client:
            response = cohere_client.embed(texts=[chunk], model="multilingual-22-12")
            embedding = response.embeddings[0]

        if embedding:
            points.append(models.PointStruct(id=str(uuid.uuid4()), vector=embedding, payload={"content": chunk}))
        else:
            print(f"Warning: Could not generate embedding for chunk {i}.")

    if points:
        try:
            qdrant_client.upsert(collection_name=COLLECTION_NAME, wait=True, points=points).wait()
            return {"status": "success", "message": f"Successfully ingested {len(points)} chunks."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to ingest points: {e}")
    else:
        return {"status": "failure", "message": "No embeddings generated."}

@app.post("/api/query")
async def query_chatbot(request: QueryRequest):
    if not qdrant_client or (not gemini_client and not cohere_client):
        raise HTTPException(status_code=500, detail="Embedding/generation model or Qdrant not initialized.")

    # Generate query embedding
    query_embedding = None
    if gemini_client:
        response = gemini_client.embeddings.create(input=[request.question], model="text-embedding-3-small")
        query_embedding = response.data[0].embedding
    elif cohere_client:
        response = cohere_client.embed(texts=[request.question], model="multilingual-22-12")
        query_embedding = response.embeddings[0]

    if not query_embedding:
        raise HTTPException(status_code=500, detail="Failed to generate query embedding.")

    context_chunks = [request.selected_text] if request.selected_text else []

    try:
        search_result = qdrant_client.search(collection_name=COLLECTION_NAME, query_vector=query_embedding, limit=5)
        for hit in search_result:
            if hit.payload and "content" in hit.payload:
                context_chunks.append(hit.payload["content"])
    except Exception as e:
        print(f"Qdrant search error: {e}. Proceeding without context.")

    context = "\n".join(context_chunks)
    prompt = f"Based on the following context, answer the question:\n\nContext: {context}\n\nQuestion: {request.question}\nAnswer:" if context else f"Answer the following question: {request.question}\nAnswer:"

    answer = ""
    try:
        if gemini_client:
            chat_completion = gemini_client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = chat_completion.choices[0].message.content
        elif cohere_client:
            response = cohere_client.generate(model="command", prompt=prompt, max_tokens=200)
            answer = response.generations[0].text
    except Exception as e:
        answer = f"Error generating answer: {e}"

    return QueryResponse(answer=answer)
