---
id: 4
title: "rag-backend-tasks"
stage: "tasks"
date: "2025-12-09"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "rag-backend"
branch: "001-rag-backend"
user: "user"
command: "/sp.tasks"
labels: ["tasks", "backend", "rag", "implementation"]
links:
  spec: "specs/001-rag-backend/spec.md"
  plan: "specs/001-rag-backend/plan.md"
  ticket: null
  adr: null
  pr: null
files:
  - "specs/001-rag-backend/tasks.md"
tests: []
prompt_text: |
  – Backend + Frontend Tasks for RAG Chatbot
  1. Ingestion & Data Preparation

  Task 1: Fetch all URLs from Docusaurus sitemap

  Task 2: Extract text from each page using trafilatura

  Task 3: Chunk text into 1200-character segments

  Task 4: Generate embeddings for each chunk using Cohere

  Task 5: Store chunk embeddings in Qdrant Cloud

  2. Backend Setup

  Task 6: Setup FastAPI project and environment variables (.env)

  Task 7: Implement config.py to load keys (Cohere, Qdrant, Gemini/OpenAI)

  Task 8: Implement Qdrant client (qdrant_client.py) with query and upsert functions

  Task 9: Implement Cohere embedding functions (embeddings.py)

  Task 10: Build retrieval tool (tools/retrieve.py)

  3. Agent & API

  Task 11: Implement RAG agent (agent.py) using OpenAI Agents / ChatKit SDK

  Task 12: Integrate retrieve tool with agent

  Task 13: Create FastAPI routes (routes/chat.py) for frontend consumption

  4. Frontend Integration

  Task 14: Connect Docusaurus frontend to FastAPI chat endpoints

  Task 15: Test end-to-end flow: user question → retrieved chunks → agent answer

  5. Testing & Deployment

  Task 16: Write unit tests for embeddings, Qdrant client, retrieval tool, and agent

  Task 17: Run integration tests with FastAPI + Docusaurus

  Task 18: Deploy backend to cloud (e.g., Vercel / Render)

  Task 19: Configure environment variables in deployment
response_text: |
  Created comprehensive task list for RAG chatbot backend implementation, organized by user stories with clear dependencies and parallel execution opportunities. Tasks cover all required functionality from ingestion through deployment.
outcome: "Successfully created detailed task breakdown for RAG chatbot backend project"
evaluation: "Tasks are well-organized by user story priority with clear dependencies and implementation path"
---

---
description: "Task list for RAG Chatbot Backend implementation"
---

# Tasks: RAG Chatbot Backend

**Input**: Design documents from `/specs/001-rag-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `rag_chatbot_backend/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 [P] Initialize Python project with FastAPI, Cohere, Qdrant, OpenAI Agents dependencies in requirements.txt
- [ ] T003 [P] Create .env file structure for API keys and configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup FastAPI project structure in rag_chatbot_backend/app/
- [ ] T005 [P] Implement config.py to load API keys (Cohere, Qdrant, OpenAI)
- [ ] T006 [P] Setup environment configuration management
- [ ] T007 Create base models/entities that all stories depend on
- [ ] T008 Configure error handling and logging infrastructure
- [ ] T009 Setup Qdrant client (qdrant_client.py) with basic connection

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Upload and Process Book Content (Priority: P1) 🎯 MVP

**Goal**: Enable users to upload their Docusaurus book content in markdown format to the system, process the content by parsing the markdown, chunking it into manageable pieces, and storing it in a vector database for retrieval.

**Independent Test**: Can be fully tested by uploading a sample markdown file and verifying that it gets properly chunked and stored in the vector database, delivering the ability to search through the content.

### Implementation for User Story 1

- [ ] T010 [P] Create ingestion module structure in rag_chatbot_backend/app/ingestion/
- [ ] T011 [P] Implement chunking.py with 1200-character segment logic
- [ ] T012 [P] Implement ingest.py with sitemap fetching functionality
- [ ] T013 Implement text extraction using trafilatura in rag_chatbot_backend/app/ingestion/ingest.py
- [ ] T014 Implement Cohere embedding functions in rag_chatbot_backend/app/embeddings.py
- [ ] T015 [P] Update Qdrant client with upsert functionality for storing chunk embeddings
- [ ] T016 Create API endpoint for document upload in rag_chatbot_backend/app/routes/ingest.py
- [ ] T017 Add validation for uploaded markdown files

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ask Questions About Book Content (Priority: P1)

**Goal**: Enable users to ask questions about their book content through the chatbot interface, where the system retrieves relevant information from the processed book content and generates accurate answers based on the source material.

**Independent Test**: Can be fully tested by asking questions about uploaded content and receiving accurate answers based on the source material, delivering the primary RAG functionality.

### Implementation for User Story 2

- [ ] T018 [P] Build retrieval tool (tools/retrieve.py) for semantic search
- [ ] T019 [P] Implement RAG agent (agent.py) using OpenAI Agents SDK
- [ ] T020 Integrate retrieve tool with agent
- [ ] T021 Create FastAPI routes (routes/chat.py) for chatbot functionality
- [ ] T022 Add semantic search functionality in Qdrant client
- [ ] T023 Implement answer generation with source attribution
- [ ] T024 Add API endpoint for chat messages with proper request/response handling

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Configure Answer Source (Priority: P2)

**Goal**: Enable users to control whether the chatbot answers using all available content or only specific selected text, providing options to switch between these modes for different use cases.

**Independent Test**: Can be fully tested by configuring the system to use selected text only and verifying that responses are restricted to that source, delivering controlled answer generation.

### Implementation for User Story 3

- [ ] T025 [P] Update chat session model to include mode configuration
- [ ] T026 Modify RAG agent to support normal vs selected-text-only modes
- [ ] T027 Update retrieval tool to filter based on selected text constraints
- [ ] T028 Add mode selection parameter to chat API endpoints
- [ ] T029 Implement answer generation that respects selected text constraints

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Frontend Integration

**Goal**: Connect Docusaurus frontend to FastAPI chat endpoints and test end-to-end flow.

- [ ] T030 [P] Create API client for Docusaurus frontend to communicate with backend
- [ ] T031 Implement chat interface in Docusaurus site
- [ ] T032 Test end-to-end flow: user question → retrieved chunks → agent answer
- [ ] T033 Add error handling and user feedback in frontend

---

## Phase 7: Testing & Deployment

**Goal**: Complete testing and prepare for deployment.

- [ ] T034 [P] Write unit tests for embeddings module
- [ ] T035 [P] Write unit tests for Qdrant client
- [ ] T036 [P] Write unit tests for retrieval tool
- [ ] T037 [P] Write unit tests for RAG agent
- [ ] T038 Run integration tests with FastAPI + Docusaurus
- [ ] T039 Prepare deployment configuration for cloud platform
- [ ] T040 Configure environment variables in deployment
- [ ] T041 Deploy backend to cloud (e.g., Vercel / Render)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T042 [P] Documentation updates in docs/
- [ ] T043 Code cleanup and refactoring
- [ ] T044 Performance optimization across all stories
- [ ] T045 [P] Additional unit tests (if requested) in tests/unit/
- [ ] T046 Security hardening
- [ ] T047 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Frontend Integration (Phase 6)**: Depends on User Stories 1 and 2 completion
- **Testing & Deployment (Phase 7)**: Depends on all desired user stories being complete
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on User Story 1 completion (needs processed content) - May integrate with US1
- **User Story 3 (P2)**: Depends on User Story 2 completion (needs chat functionality) - May integrate with US1/US2

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1 and 2 can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members after dependencies are met

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Upload and Process)
4. Complete Phase 4: User Story 2 (Ask Questions)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 together
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test with US1 → Deploy/Demo
4. Add User Story 3 → Test with US1/US2 → Deploy/Demo
5. Add Frontend Integration → Test end-to-end → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3 (after US1/US2)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence