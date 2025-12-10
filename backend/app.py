import cohere 
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")


cohere_client = cohere.Client(COHERE_API_KEY)

qdrant = QdrantClient(
    url = QDRANT_URL,
    api_key = QDRANT_API_KEY
)

#=============================================
# EMBEDDING FUNCTION
#=============================================

def get_embedding(text):
    """Get embedding vector from Cohere Embed v2."""
    response = cohere_client.embed(
        model = "embed-multilingual-v2.0",
        texts = [text],
    )
    return response.embeddings[0]

#=============================================
# RETRIEVE FUNCTION
#=============================================

def retrieve(query):
    embedding = get_embedding(query)
    
    results = qdrant.search_points(
        collection_name="my-ai_robotics_book",
        query_vector=embedding,
        limit=5
    )
    
    return [point.payload["text"] for point in results]
