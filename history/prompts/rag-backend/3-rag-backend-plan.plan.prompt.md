---
id: 3
title: "rag-backend-plan"
stage: "plan"
date: "2025-12-09"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "rag-backend"
branch: "001-rag-backend"
user: "user"
command: "/sp.plan"
labels: ["plan", "backend", "rag", "architecture"]
links:
  spec: "specs/001-rag-backend/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-rag-backend/plan.md"
  - "specs/001-rag-backend/research.md"
  - "specs/001-rag-backend/data-model.md"
  - "specs/001-rag-backend/quickstart.md"
  - "specs/001-rag-backend/contracts/chat-api.yaml"
tests: []
prompt_text: |
  – RAG Chatbot Backend Engineering Plan
  1. Environment

  Backend: Python + FastAPI

  Vector DB: Qdrant Cloud

  Embeddings: Cohere

  LLM Layer: OpenAI Agents / ChatKit SDK

  Frontend Integration: Docusaurus site (React-based) consumes backend APIs

  2. Folder Structure
  rag_chatbot_backend/
  ├─ app/
  │  ├─ main.py              # FastAPI app entrypoint
  │  ├─ config.py            # Load API keys, env variables
  │  ├─ embeddings.py        # Cohere embeddings functions
  │  ├─ qdrant_client.py     # Qdrant connection & queries
  │  ├─ agent.py             # Agent creation using OpenAI Agents SDK
  │  ├─ tools/
  │  │  └─ retrieve.py       # Retrieval function (tool)
  │  ├─ routes/
  │  │  └─ chat.py           # FastAPI routes for chatbot (Docusaurus frontend consumes this)
  │  └─ ingestion/
  │     ├─ ingest.py         # Sitemap scraping & ingestion
  │     └─ chunking.py       # Text chunking functions
  ├─ tests/                  # Unit & integration tests
  ├─ requirements.txt        # Python dependencies
  └─ .env                    # API keys, endpoints

  3. File Responsibilities
  File    Responsibility
  main.py    FastAPI startup, register routes (serve API endpoints for Docusaurus frontend)
  config.pyg OpenAI Agents SDK and integrate retrieve tool

  Add FastAPI routes (routes/chat.py) for chat requests from Docusaurus frontend

  Test Docusaurus frontend ↔ backend API connection

  Write unit & integration tests

  Run local testing & debug end-to-end RAG workflow

  5. Milestones

  M1: Environment setup + Qdrant connection verified

  M2: Cohere embeddings working with dummy text

  M3: Full ingestion pipeline working with sitemap → Qdrant

  M4: Retrieval tool tested independently

  M5: Agent integrated with retrieval + FastAPI endpoint

  M6: Docusaurus frontend successfully connected to backend API

  M7: End-to-end test: user question → retrieved content → agent answer

  M8: Documentation & unit tests complete

      Load
response_text: |
  Created comprehensive implementation plan for the RAG chatbot backend, including technical context, constitution check, project structure, research findings, data model, quickstart guide, and API contracts. All artifacts created according to the /sp.plan workflow.
outcome: "Successfully created implementation plan for RAG chatbot backend project"
evaluation: "Plan addresses all required components and provides clear technical approach with proper documentation and contracts"
---

# Implementation Plan: RAG Chatbot Backend

**Branch**: `001-rag-backend` | **Date**: 2025-12-09 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-rag-backend/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a Retrieval-Augmented Generation (RAG) chatbot backend that enables users to upload Docusaurus book content, process it through embedding generation and vector storage in Qdrant, then answer questions using OpenAI Agents with semantic search capabilities. The system supports both normal answering mode and selected-text-only mode for precise content responses.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: FastAPI, Cohere, Qdrant, OpenAI Agents SDK
**Storage**: Qdrant Cloud vector database
**Testing**: pytest
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web backend API
**Performance Goals**: Query response time < 2 seconds for 95th percentile, Vector search returns relevant results within 100ms
**Constraints**: <200ms p95 response time, Memory usage optimized for Free Tier Qdrant limitations, Must handle concurrent requests without degradation
**Scale/Scope**: Support 1000+ concurrent users, Process 100-page markdown books within 5 minutes

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Data Integrity and Source Verification**: System must only provide answers based on verified document content from vector database and NOT hallucinate responses outside provided context
- **API Design Clarity and Documentation**: All API endpoints must be well-documented with clear request/response schemas following RESTful principles and OpenAPI specification
- **System Reproducibility and Deployment Consistency**: Backend deployment must be reproducible through version-controlled configuration with consistent behavior across environments
- **Engineering Rigor and Performance Standards**: All components must include proper error handling, logging, and monitoring; system must meet performance requirements with minimum 80% test coverage
- **Security and Data Privacy Compliance**: System must protect user data and document content with appropriate authentication/authorization; sensitive config must be stored securely

## Project Structure

### Documentation (this feature)

```text
specs/001-rag-backend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
rag_chatbot_backend/
├─ app/
│  ├─ main.py              # FastAPI app entrypoint
│  ├─ config.py            # Load API keys, env variables
│  ├─ embeddings.py        # Cohere embeddings functions
│  ├─ qdrant_client.py     # Qdrant connection & queries
│  ├─ agent.py             # Agent creation using OpenAI Agents SDK
│  ├─ tools/
│  │  └─ retrieve.py       # Retrieval function (tool)
│  ├─ routes/
│  │  └─ chat.py           # FastAPI routes for chatbot (Docusaurus frontend consumes this)
│  └─ ingestion/
│     ├─ ingest.py         # Sitemap scraping & ingestion
│     └─ chunking.py       # Text chunking functions
├─ tests/                  # Unit & integration tests
├─ requirements.txt        # Python dependencies
└─ .env                    # API keys, endpoints
```

**Structure Decision**: Web application backend structure selected to support FastAPI-based REST API for Docusaurus frontend consumption, with clear separation of concerns between ingestion, storage, retrieval, and API layers.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |