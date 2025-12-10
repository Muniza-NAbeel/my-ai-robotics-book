---
id: 1
title: "rag-backend-constitution"
stage: "constitution"
date: "2025-12-09"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "backend", "rag", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
prompt_text: |
  You are a senior AI backend architect.

  We are building a Retrieval-Augmented Generation (RAG) chatbot backend for a Docusaurus book .

  Project goals:
  - User asks questions about book content
  - Bot answers using embeddings + vector search
  - Bot can answer ONLY based on user-selected text when provided

  Tech stack (must be used):
  - FastAPI (Python)
  - OpenAI Agents or ChatKit SDK
  - Qdrant Cloud (Free Tier) for vector database
  - Cohere

  Backend responsibilities:
  - Ingest book content
  - Create embeddings
  - Store vectors in Qdrant
  - Provide API endpoints for chatbot

  Create a formal engineering constitution for this project.
response_text: |
  Created a comprehensive engineering constitution for the RAG chatbot backend project, including core principles around data integrity, API design clarity, system reproducibility, engineering rigor, and security. Defined backend architecture requirements, tech stack governance, performance requirements, and code quality standards.
outcome: "Successfully created engineering constitution for RAG chatbot backend project"
evaluation: "Constitution addresses all specified requirements and provides clear governance for the project"
---

# RAG Chatbot Backend Constitution

## Core Principles

### Data Integrity and Source Verification
All responses must be grounded in verified document content from the vector database. The system MUST only provide answers based on user-selected text when provided, and MUST NOT hallucinate or generate responses outside the provided context. All retrieved content must be properly attributed to source documents.

### API Design Clarity and Documentation
All API endpoints must be well-documented with clear request/response schemas. The backend MUST follow RESTful principles with consistent error handling. All endpoints must include OpenAPI documentation and follow FastAPI best practices for type safety and validation.

### System Reproducibility and Deployment Consistency
The backend deployment must be reproducible through infrastructure as code. All environment variables, dependencies, and configurations must be version-controlled. The system MUST be deployable in multiple environments (development, staging, production) with consistent behavior.

### Engineering Rigor and Performance Standards
All components must include proper error handling, logging, and monitoring. The system MUST meet defined performance requirements including response time under 2 seconds for typical queries. All code must include appropriate unit and integration tests with minimum 80% coverage.

### Security and Data Privacy Compliance
The system MUST protect user data and document content. All API endpoints must implement appropriate authentication and authorization. Sensitive configuration (API keys, database credentials) must be stored securely and never committed to version control.

## Backend Architecture Requirements

- Ingestion pipeline for Docusaurus book content
- Embedding generation using Cohere
- Vector storage and retrieval using Qdrant Cloud
- FastAPI-based REST API with OpenAPI documentation
- Proper separation of concerns between ingestion, storage, and query components
- Error handling and logging for all operations
- Health check endpoints for monitoring

## Tech Stack Governance

- FastAPI for web framework and API endpoints
- Cohere for text embeddings generation
- Qdrant Cloud (Free Tier) for vector database operations
- OpenAI Agents or ChatKit SDK for conversation handling
- Python 3.9+ for backend implementation
- All dependencies must be specified in requirements.txt with version constraints

## Performance and Scalability Requirements

- Query response time: < 2 seconds for 95th percentile
- Vector search must return relevant results within 100ms
- System must handle concurrent requests without degradation
- Embedding generation must process documents efficiently
- Memory usage must be optimized for Free Tier Qdrant limitations

## Code Quality Standards

- Follow PEP 8 style guidelines
- Type hints for all function parameters and return values
- Comprehensive logging with appropriate log levels
- Proper error handling with meaningful error messages
- Unit tests for all business logic components
- Integration tests for API endpoints

## Governance

All code changes must pass automated tests before merging.
All API changes must be documented in OpenAPI specification.
Performance benchmarks must be maintained and monitored.
Constitution supersedes all other practices; Amendments require documentation and approval.
All PRs/reviews must verify compliance with these principles.
Dependencies must be kept up-to-date with security patches.
Use CLAUDE.md for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09