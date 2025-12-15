---
title: AI Robotics Book Backend
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# RAG Chatbot Backend

This is a production-ready FastAPI backend for a Retrieval-Augmented Generation (RAG) chatbot that processes Docusaurus book content.

## Features

- **Markdown Ingestion**: Upload and process markdown files
- **Text Chunking**: Split documents into manageable chunks with overlap
- **Embedding Generation**: Create embeddings using Cohere
- **Vector Storage**: Store embeddings in Qdrant vector database
- **Semantic Search**: Query vectors using semantic similarity
- **OpenAI Integration**: Answer questions using OpenAI Agents
- **Dual Answer Modes**: Support for normal and selected-text-only answering
- **Comprehensive Logging**: Full logging for requests, errors, and embeddings

## Architecture

```
backend/
├── rag_chatbot_backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entrypoint
│   │   ├── config.py            # Environment variable loading
│   │   ├── embeddings.py        # Cohere embeddings functions
│   │   ├── qdrant_client.py     # Qdrant operations
│   │   ├── agent.py             # RAG agent with OpenAI
│   │   ├── tools/
│   │   │   └── retrieve.py      # Retrieval tool
│   │   ├── routes/
│   │   │   └── chat.py          # API endpoints
│   │   └── ingestion/
│   │       ├── ingest.py        # Document ingestion
│   │       └── chunking.py      # Text chunking
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Setup

1. Clone the repository and navigate to the backend directory
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the environment template and fill in your API keys:
   ```bash
   cp .env.example .env
   # Edit .env with your actual API keys
   ```
5. Run the application:
   ```bash
   cd rag_chatbot_backend/app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `POST /api/v1/ingest/upload` - Upload and process markdown documents
- `POST /api/v1/chat/session` - Create a new chat session
- `POST /api/v1/chat/message` - Send a message and get a response
- `GET /api/v1/health` - Health check
- `GET /api/v1/stats` - Get vector store statistics

## Environment Variables

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_API_KEY`: Your Qdrant API key
- `QDRANT_HOST`: Your Qdrant Cloud endpoint
- `OPENAI_API_KEY`: Your OpenAI API key
- `DEBUG`: Enable debug mode (default: False)
- `LOG_LEVEL`: Logging level (default: INFO)
- `QDRANT_COLLECTION_NAME`: Name of the Qdrant collection (default: documents)
- `CHUNK_SIZE`: Size of text chunks (default: 1200)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 100)

## Usage

1. Upload a markdown document using the `/api/v1/ingest/upload` endpoint
2. Create a chat session using `/api/v1/chat/session`
3. Send questions using `/api/v1/chat/message` with the session ID

## Security

- All sensitive configuration is loaded from environment variables
- API keys are never hardcoded in the source code
- Input validation is performed on all endpoints
- CORS is configured (though set to allow all origins in development)