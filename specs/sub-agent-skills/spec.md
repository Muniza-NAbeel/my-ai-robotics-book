# Feature Specification: AI-native Textbook Multi-Agent System

**Feature Branch**: `001-sub-agent-skills`
**Created**: 2025-12-11
**Updated**: 2025-12-12
**Status**: Draft
**Input**: User description: "Build an AI-native Textbook System with modular Agents including sub-agents, BaseSkillAgent, Main Orchestrator, FastAPI backend, and React chatbot with skill buttons using OpenAI-Agents-SDK with Gemini model"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Glossary via Chatbot Skill Button (Priority: P1)

As a textbook reader, I want to click a "Glossary" skill button in the chatbot to get a simple definition of a technical term so that I can understand unfamiliar concepts quickly.

**Why this priority**: Glossary definitions are the most commonly needed feature for educational content. Users frequently encounter unfamiliar terms and need quick explanations.

**Independent Test**: Can be fully tested by clicking the Glossary button, the system sends a predefined query with `skill: "glossary"`, and a simple definition is returned in the chat.

**Acceptance Scenarios**:

1. **Given** a reader opens the chatbot, **When** they see the initial view, **Then** four skill buttons are displayed (Glossary, Diagram, Translate, Exercises) with no default messages
2. **Given** a reader clicks the "Glossary" button, **When** the button is clicked, **Then** a predefined query is automatically sent with `skill: "glossary"` and the buttons disappear
3. **Given** the glossary request is processing, **When** the user waits, **Then** a "Thinking..." indicator is displayed
4. **Given** the glossary agent responds, **When** the response arrives, **Then** a simple definition appears as a bot message in the chat

---

### User Story 2 - Generate ASCII Diagram via Chatbot (Priority: P1)

As a textbook reader, I want to click a "Diagram" skill button to generate a visual ASCII diagram for a topic so that I can better understand structures and relationships.

**Why this priority**: Visual diagrams significantly improve comprehension of technical topics and are essential for educational content about robotics and AI.

**Independent Test**: Can be fully tested by clicking the Diagram button, the system sends a predefined query with `skill: "diagram"`, and an ASCII diagram is returned.

**Acceptance Scenarios**:

1. **Given** a reader clicks the "Diagram" button, **When** the button is clicked, **Then** a predefined query is automatically sent with `skill: "diagram"` to the backend
2. **Given** the diagram agent processes the request, **When** processing completes, **Then** an ASCII block diagram showing components and relationships appears in the chat
3. **Given** the request is processing, **When** the user waits, **Then** a "Thinking..." indicator is shown until completion

---

### User Story 3 - Translate to Urdu via Chatbot (Priority: P2)

As a textbook reader who prefers Urdu, I want to click a "Translate" skill button to translate English text to Urdu so that I can understand the content in my native language.

**Why this priority**: Translation support enables wider accessibility of the educational content to Urdu-speaking audiences.

**Independent Test**: Can be fully tested by clicking the Translate button, the system sends a query with `skill: "translate"`, and Urdu translation is returned.

**Acceptance Scenarios**:

1. **Given** a reader clicks the "Translate" button, **When** the button is clicked, **Then** a predefined query is automatically sent with `skill: "translate"`
2. **Given** translation completes, **When** the response arrives, **Then** Urdu translation appears as a bot message
3. **Given** an error occurs, **When** the backend fails, **Then** an appropriate error message is shown in the chat

---

### User Story 4 - Generate Practice Exercises via Chatbot (Priority: P2)

As a textbook reader studying a chapter, I want to click an "Exercises" skill button to generate practice questions at different difficulty levels so that I can test my understanding.

**Why this priority**: Practice exercises reinforce learning and allow readers to self-assess their understanding.

**Independent Test**: Can be fully tested by clicking the Exercises button, the system sends a query with `skill: "exercises"`, and three questions at different levels are returned.

**Acceptance Scenarios**:

1. **Given** a reader clicks the "Exercises" button, **When** the button is clicked, **Then** a predefined query is automatically sent with `skill: "exercises"`
2. **Given** exercises are generated, **When** the response arrives, **Then** three questions labeled easy, medium, and advanced appear in the chat
3. **Given** the system processes, **When** the user waits, **Then** a thinking indicator is displayed

---

### User Story 5 - Continue Conversation After Skill Button (Priority: P1)

As a textbook reader, after clicking a skill button and receiving a response, I want to continue the conversation normally with text input so that I can ask follow-up questions.

**Why this priority**: Seamless conversation flow is essential for a good chatbot experience.

**Independent Test**: Can be tested by clicking any skill button, receiving a response, then typing a follow-up message and receiving a response.

**Acceptance Scenarios**:

1. **Given** a skill button was clicked and buttons have disappeared, **When** the reader types a message in the input box, **Then** the message is sent to the backend
2. **Given** a message is sent, **When** the backend responds, **Then** the response appears as a new bot message bubble
3. **Given** the chat is active, **When** multiple messages are exchanged, **Then** all user and bot messages display in correct chronological order

---

### User Story 6 - Main Orchestrator Agent Routes to Sub-Agents (Priority: P3)

As a developer integrating the system, I want a main orchestrator agent that routes requests to the appropriate sub-agent based on the skill parameter so that skills are modular and extensible.

**Why this priority**: Clean architecture enables maintainability but is not directly user-facing.

**Independent Test**: Can be tested by calling the orchestrator with different skill values and verifying the correct sub-agent is invoked.

**Acceptance Scenarios**:

1. **Given** a request with `skill: "glossary"`, **When** the orchestrator receives it, **Then** the GlossaryAgent is invoked
2. **Given** a request with `skill: "diagram"`, **When** the orchestrator receives it, **Then** the DiagramAgent is invoked
3. **Given** a request with `skill: "translate"`, **When** the orchestrator receives it, **Then** the TranslateAgent is invoked
4. **Given** a request with `skill: "exercises"`, **When** the orchestrator receives it, **Then** the ExercisesAgent is invoked

---

### Edge Cases

- What happens when a user provides an empty query? System returns a friendly error message prompting for valid input.
- How does system handle very long input text? System processes up to a reasonable limit (2000 characters) and truncates with notice if exceeded.
- What happens when the API endpoint is unavailable? Frontend displays a connection error message in the chat.
- How does the system handle special characters in input? System sanitizes input and handles Unicode characters properly for Urdu support.
- What happens if the skill parameter is invalid or missing? System defaults to general chatbot behavior or returns an error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a BaseSkillAgent class with reusable helpers and shared LLM call functionality using OpenAI-Agents-SDK
- **FR-002**: System MUST provide a GlossaryAgent that extends BaseSkillAgent and returns simple, clear definitions for terms
- **FR-003**: System MUST provide a DiagramAgent that extends BaseSkillAgent and returns ASCII/pseudo diagrams for topics
- **FR-004**: System MUST provide a TranslateAgent that extends BaseSkillAgent and returns Urdu translations of English text
- **FR-005**: System MUST provide an ExercisesAgent that extends BaseSkillAgent and returns 3 practice questions for a chapter/topic
- **FR-006**: System MUST provide a MainOrchestratorAgent that routes requests to the appropriate sub-agent based on skill parameter
- **FR-007**: System MUST configure OpenAI-Agents-SDK to use Gemini model in OpenAI-compatible mode
- **FR-008**: System MUST provide a FastAPI POST route `/api/chatbot` that accepts JSON with `query` and `skill` fields
- **FR-009**: The FastAPI route MUST call the MainOrchestratorAgent and return the response as JSON
- **FR-010**: System MUST provide a React + TypeScript chatbot component with four skill buttons: Glossary, Diagram, Translate, Exercises
- **FR-011**: When a skill button is clicked, the component MUST automatically send a predefined query with the corresponding skill value
- **FR-012**: After a skill button is clicked, the skill buttons MUST disappear and chat continues normally
- **FR-013**: The chatbot component MUST display message bubbles for both user and bot messages
- **FR-014**: The chatbot component MUST display a "Thinking..." indicator while waiting for backend response
- **FR-015**: The chatbot component MUST include an input box and send button for user text input
- **FR-016**: The chatbot component MUST use a configurable backend URL (placeholder: YOUR_BACKEND_URL)

### Key Entities

- **BaseSkillAgent**: Abstract base class providing shared LLM call functionality and reusable helpers for all sub-agents
- **GlossaryAgent**: Sub-agent responsible for generating simple term definitions
- **DiagramAgent**: Sub-agent responsible for generating ASCII diagrams for topics
- **TranslateAgent (TranslationAgent)**: Sub-agent responsible for English to Urdu translation
- **ExercisesAgent**: Sub-agent responsible for generating difficulty-graded practice questions
- **MainOrchestratorAgent**: Central agent that receives requests and routes to appropriate sub-agent based on skill
- **ChatbotRequest**: API request payload containing `query` (string) and `skill` (enum: glossary | diagram | translate | exercises)
- **ChatbotResponse**: API response payload containing the generated content from the sub-agent
- **ChatbotComponent**: React UI component managing chat state, skill buttons, and message display

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can generate a glossary definition within 5 seconds of clicking the Glossary button
- **SC-002**: Users can generate an ASCII diagram within 5 seconds of clicking the Diagram button
- **SC-003**: Users can translate text to Urdu within 5 seconds of clicking the Translate button
- **SC-004**: Users can generate 3 practice exercises within 5 seconds of clicking the Exercises button
- **SC-005**: 100% of skill button clicks result in the buttons disappearing and chat continuing normally
- **SC-006**: The "Thinking..." indicator appears within 100ms of any request being initiated
- **SC-007**: All API requests return valid JSON responses with appropriate content
- **SC-008**: All 4 sub-agents are correctly routed through the main orchestrator agent
- **SC-009**: The chatbot displays all exchanged messages in correct chronological order
- **SC-010**: System integrates with Gemini model via OpenAI-Agents-SDK in OpenAI-compatible mode

## Assumptions

- The book content is primarily educational material about robotics and AI
- The target audience includes Urdu-speaking readers
- OpenAI-Agents-SDK supports Gemini model in OpenAI-compatible mode
- Developers have access to Gemini API credentials
- The React frontend can make HTTP requests to the FastAPI backend
- Backend URL will be configured at deployment time (using placeholder YOUR_BACKEND_URL during development)

## Scope

### In Scope

**Backend (Python)**:
- `/agents/base-skill-agent.py` - BaseSkillAgent class with shared LLM functionality
- `/agents/glossary-agent.py` - GlossaryAgent extending BaseSkillAgent
- `/agents/diagram-agent.py` - DiagramAgent extending BaseSkillAgent
- `/agents/translate-agent.py` - TranslateAgent extending BaseSkillAgent
- `/agents/exercises-agent.py` - ExercisesAgent extending BaseSkillAgent
- `/agents/main-orchestrator-agent.py` - MainOrchestratorAgent routing to sub-agents
- `/api/chatbot.py` - FastAPI POST route for chatbot

**Frontend (React + TypeScript)**:
- `/src/components/Chatbot/index.tsx` - Full chatbot component with skill buttons

**Features**:
- Basic error handling for empty/invalid input
- "Thinking..." loading state in UI
- Message bubbles for user and bot
- Skill-based routing via orchestrator
- OpenAI-Agents-SDK with Gemini model integration

### Out of Scope

- Authentication/authorization for API routes
- Rate limiting
- Persistent storage of chat history
- Session management across page reloads
- Internationalization beyond English-Urdu
- Unit tests (can be added in future iteration)
- WebSocket real-time updates (using standard HTTP requests)
- Multiple Gemini model variants (using single configured model)

## File Structure Reference

```
/agents/
    base-skill-agent.py      # BaseSkillAgent with shared LLM call
    glossary-agent.py        # Term definitions
    diagram-agent.py         # ASCII diagrams
    translate-agent.py       # English to Urdu
    exercises-agent.py       # Practice questions
    main-orchestrator-agent.py  # Routes to sub-agents

/api/
    chatbot.py               # FastAPI POST /api/chatbot

/src/components/Chatbot/
    index.tsx                # React + TypeScript chatbot component
```
