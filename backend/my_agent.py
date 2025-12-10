from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient

load_dotenv()
set_tracing_disabled(True)

# ---------------- Provider / Model ----------------
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)

# ---------------- Cohere & Qdrant ----------------
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

cohere_client = cohere.Client(COHERE_API_KEY)

qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

# ---------------- Embedding function ----------------
def get_embedding(text):
    response = cohere_client.embed(
        model="embed-multilingual-v2.0",
        texts=[text],
    )
    return response.embeddings[0]

# ---------------- Retrieve function ----------------
@function_tool
def retrieve(query):
    embedding = get_embedding(query)
    result = qdrant.query_points(
        collection_name="my-ai_robotics_book",
        query=embedding,
        limit=5,
    )
    return [point.payload["text"] for point in result.points]

# ---------------- Agent definition ----------------
agent = Agent(
    name="AI Robotics Tutor",
    instructions="""
    You are an AI tutor for the AI Robotics Book. To answer user questions:
    1️⃣ Call the tool `retrieve` with the user query.
    2️⃣ Use ONLY the retrieved content to form your answer.
    3️⃣ Give step-by-step reasoning before the final answer.
    4️⃣ If the answer is not in retrieved content, respond with "I don't know".
    """,
    model=model,
    tools=[retrieve],
)

