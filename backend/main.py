import requests
from fastapi import FastAPI
import xml.etree.ElementTree as ET
import trafilatura
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import cohere 
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from my_agent import agent, Runner 


class QueryRequest(BaseModel):
    question: str
    selected_text: str | None = None

load_dotenv()
app = FastAPI()   # ✅ ADD THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # yahan tumhara frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# CONFIGURATION

SITEMAP_URL = "https://my-ai-robotics-book.vercel.app/sitemap.xml"
COLLECTION_NAME = "my-ai_robotics_book"

cohere_client = cohere.Client(COHERE_API_KEY)
EMBED_MODEL = "embed-multilingual-v2.0"

qdrant = QdrantClient(
    url = QDRANT_URL,
    api_key = QDRANT_API_KEY
)


# ---------------- HELPER FUNCTION ----------------
def search_qdrant(query_text, top_k=3):
    # Temporary dummy chunks for testing
    return [
        {"text": "This is a dummy chunk about Physical AI.", "url": "https://example.com"},
        {"text": "Another chunk of text from the book.", "url": "https://example.com"},
    ]

# ---------------- API ROUTE ----------------

@app.get("/")
def home():
    return {"status": "FastAPI is running"}

@app.post("/ingest")
def run_ingestion():
    ingest_book()
    return {"message": "Ingestion started"}


@app.post("/api/query")
def query_bot(req: QueryRequest):
    question = req.question
    selected_text = req.selected_text

    if selected_text:
        question = f"{question}\nContext: {selected_text}"

    # Run agent
    result = Runner.run_sync(agent, input=question)

    return {"answer": result.final_output}


#=============================================
# STEP 1 - EXTRACT URLS FROM SITEMAP
def get_all_urls(sitemap_url):
    xml = requests.get(sitemap_url).text
    root = ET.fromstring(xml)

    urls = []
    for child in root:
        loc_tag = child.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        if loc_tag is not None:
            urls.append(loc_tag.text)

    print("\n FOUND ULS:")
    for u in urls:
        print(" -", u)
    return urls

#=============================================
# STEP 2 - DOWNLOAD PAGE & EXTRACT TEXT
#=============================================

def extract_text_from_url(url):
    html = requests.get(url).text
    text = trafilatura.extract(html)

    if not text:
        print("[WARNING] No text extracted from:", url)

    return text

#=============================================
# STEP 3 - CHUNK THE TEXT
#=============================================

def chunk_text(text, max_chars=1200):
    chunks = []
    while len(text) > max_chars:
        split_pos = text[:max_chars].rfind('. ')
        
        if split_pos == -1:
            split_pos = max_chars
        else:
            split_pos += 2  # period + space ko include karo

        chunk = text[:split_pos].strip()
        if chunk:
            chunks.append(chunk)

        text = text[split_pos:].strip()

    if text:
        chunks.append(text)

    return chunks


#=============================================
# STEP 4 - Create Embeddings
#=============================================

def embed(text):
    response = cohere_client.embed(
        model=EMBED_MODEL,
        texts=[text]
    )
    return response.embeddings[0]

#=============================================
# STEP 5 - Store in Qdrant
#=============================================

def create_collection():
    print("\n Creating collection in Qdrant...")
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=768,
            distance=Distance.COSINE
        )
    )

#=============================================
# SAVE CHUNKS TO QDRANT
#=============================================

def save_chunks_to_qdrant(chunk, chunk_id, url):
    vector = embed(chunk)

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=chunk_id,
                vector=vector,
                payload={
                    "url": url,
                    "text": chunk,
                    "chunk_id": chunk_id
                }
            )
        ]
    )

#=============================================
# MAIN PROCESS
#=============================================

def ingest_book():
    urls = get_all_urls(SITEMAP_URL)

    create_collection()

    global_id = 1

    for url in urls:
        print("\n Processing URL:", url)
        text = extract_text_from_url(url)

        if not text:
            continue

        chunks = chunk_text(text)

        for ch in chunks:
            save_chunks_to_qdrant(ch, global_id, url)
            print(f"Saved chunk {global_id}")
            global_id += 1

    print("\n INGESTION PROCESS COMPLETE.")
    print("\n Ingestion complete. Total chunks stored:", global_id - 1)

#if __name__ == "__main__":
#    ingest_book()