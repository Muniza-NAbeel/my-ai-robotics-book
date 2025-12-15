# Research: AI-native Textbook Multi-Agent System

**Feature**: 001-sub-agent-skills
**Date**: 2025-12-12
**Status**: Complete (Updated)

## Research Summary

This document captures research findings for building an AI-powered multi-agent system for the My AI Robotics Book project. **Updated to use OpenAI-Agents-SDK with Gemini model** instead of the previous template-based approach.

---

## 1. OpenAI-Agents-SDK with Gemini Model Integration

### Decision: Use OpenAI-Agents-SDK with Gemini in OpenAI-Compatible Mode

**Rationale**: The user requirement explicitly specifies using OpenAI-Agents-SDK with Gemini model. The existing codebase (`backend/my_agent.py`) already demonstrates this pattern successfully.

**Implementation Pattern** (from existing code):
```python
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=gemini_base_url  # Gemini OpenAI-compatible endpoint
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=provider
)
```

**Alternatives Considered**:
1. **Template-based generation** (previous approach)
   - Rejected: User explicitly requires AI-powered generation via OpenAI-Agents-SDK
2. **Direct Gemini API** (google-generativeai library)
   - Rejected: User specified OpenAI-compatible mode via OpenAI-Agents-SDK
3. **OpenAI API directly**
   - Rejected: User specified Gemini model

---

## 2. Agent Architecture Pattern

### Decision: BaseSkillAgent + Sub-Agents with Main Orchestrator

**Rationale**: Clean separation of concerns with:
- `BaseSkillAgent`: Abstract class with shared LLM call functionality
- 4 Sub-agents: Each specialized for one skill with custom prompts
- `MainOrchestratorAgent`: Routes requests based on `skill` parameter

**Key Design Points**:
1. Each sub-agent creates its own `Agent` instance with skill-specific instructions
2. BaseSkillAgent provides shared model configuration and helper methods
3. MainOrchestrator uses a skill-to-agent mapping dictionary

**Alternatives Considered**:
1. **Single agent with all skills** - One agent handles all prompts
   - Rejected: Less modular, harder to maintain and extend
2. **OpenAI-Agents-SDK function tools** - Skills as function tools
   - Rejected: Simpler to have dedicated agents per skill
3. **Flat registry without orchestrator** - Direct agent lookup
   - Rejected: Orchestrator provides cleaner API interface

---

## 3. API Route Structure

### Decision: Single Unified `/api/chatbot` POST Endpoint

**Rationale**: Per spec requirement FR-008, a single endpoint accepts `query` and `skill` parameters. This simplifies frontend integration and allows skill-based routing.

**Request Format**:
```json
{
  "query": "What is a Robot?",
  "skill": "glossary"
}
```

**Response Format**:
```json
{
  "response": "A robot is a machine capable of..."
}
```

**Routing Logic**:
- `skill: "glossary"` → GlossaryAgent
- `skill: "diagram"` → DiagramAgent
- `skill: "translate"` → TranslateAgent
- `skill: "exercises"` → ExercisesAgent
- No skill or invalid → MainOrchestratorAgent (general response)

**Alternatives Considered**:
1. **Separate endpoints per skill** (`/api/skills/glossary`, etc.)
   - Rejected: Spec specifies single `/api/chatbot` endpoint
2. **WebSocket connection**
   - Rejected: Spec specifies HTTP POST requests
3. **GraphQL**
   - Rejected: Over-engineering for this use case

---

## 4. Chatbot UI with Skill Buttons

### Decision: Integrated Chatbot Component with Initial Skill Buttons

**Rationale**: Per spec requirements FR-010 to FR-016, the chatbot shows 4 skill buttons initially (no default messages), which disappear after first click.

**UI Flow**:
1. Chatbot opens → Shows 4 skill buttons, no messages
2. User clicks skill button → Predefined query sent with skill, buttons disappear
3. "Thinking..." indicator while waiting
4. Response appears as bot message
5. Normal chat continues with input box

**Button Configuration**:
| Button | Icon | Predefined Query | Skill Value |
|--------|------|------------------|-------------|
| Glossary | book | "Explain this term to me" | "glossary" |
| Diagram | chart | "Show me a diagram for this topic" | "diagram" |
| Translate | globe | "Translate this to Urdu" | "translate" |
| Exercises | edit | "Generate practice questions" | "exercises" |

**Alternatives Considered**:
1. **Separate skill button components** (existing SkillButtons/)
   - Rejected: Spec requires integrated chatbot with buttons
2. **Persistent buttons throughout chat**
   - Rejected: Spec says buttons disappear after click (FR-012)
3. **Modal/popup for skill results**
   - Rejected: Spec requires results in chat message bubbles

---

## 5. Sub-Agent Prompt Engineering

### Decision: Specialized Prompts per Agent

**GlossaryAgent Prompt**:
```
You are a glossary expert for an AI and robotics textbook. When given a term or topic:
1. Provide a simple, clear definition
2. Use plain language suitable for students
3. Keep the explanation concise (2-3 sentences)
4. Include an example if helpful
```

**DiagramAgent Prompt**:
```
You are a diagram generator for an AI and robotics textbook. When given a topic:
1. Create an ASCII art diagram showing the main components
2. Use boxes, arrows, and labels to show relationships
3. Keep the diagram readable in a fixed-width font
4. Add a brief explanation below the diagram
```

**TranslateAgent Prompt**:
```
You are a translator for an AI and robotics textbook. When given English text:
1. Translate the text to Urdu
2. Preserve technical terms where appropriate
3. Maintain the meaning and context
4. Use clear, readable Urdu script
```

**ExercisesAgent Prompt**:
```
You are an exercise generator for an AI and robotics textbook. When given a chapter or topic:
1. Generate exactly 3 practice questions
2. Label them: Easy, Medium, Advanced
3. Easy: Basic recall/definition questions
4. Medium: Application/explanation questions
5. Advanced: Analysis/design questions
```

---

## 6. Error Handling Strategy

### Decision: Graceful Degradation with User-Friendly Messages

**Backend Errors**:
- Empty query → 400 with `{"error": "Query cannot be empty"}`
- Invalid skill → Use general response (no error)
- LLM timeout → 504 with `{"error": "Request timed out. Please try again."}`
- LLM error → 500 with `{"error": "Could not generate response. Please try again."}`

**Frontend Handling**:
- Network error → Display "Connection error. Please check your network."
- Timeout → Display "Request timed out. Please try again."
- Any error → Show in chat as system message, allow retry

---

## 7. Environment Configuration

### Decision: Use Existing .env Pattern

**Required Environment Variables**:
```
GEMINI_API_KEY=your-gemini-api-key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

**Frontend Configuration**:
- Backend URL as configurable constant (placeholder: YOUR_BACKEND_URL)
- Default to localhost:8000 for development

---

## 8. Integration with Existing Codebase

### Decision: Minimal Changes to Existing Files

**Files to Add**:
- `backend/skill_agents/` directory (already partially exists)
- Update `backend/main.py` to add chatbot route if needed

**Files to Modify**:
- `my-ai-robotics-book/src/components/Chatbot/index.tsx` - Add skill buttons

**Files Unchanged**:
- `backend/my_agent.py` - Keep RAG agent separate
- `backend/skills_routes.py` - Keep existing skill routes (optional)
- Existing SkillButtons components (may coexist)

---

## 9. CORS Configuration

### Decision: Use Existing CORS Middleware

**Current Setup** (from `main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Verification**: New routes inherit this CORS config automatically.

---

## Unresolved Items

None. All technical decisions align with spec requirements and existing codebase patterns.

---

## References

- Feature spec: `specs/sub-agent-skills/spec.md`
- Existing agent pattern: `backend/my_agent.py`
- Existing skill agents: `backend/skill_agents/`
- Existing chatbot: `my-ai-robotics-book/src/components/Chatbot/index.tsx`
- Constitution: `.specify/memory/constitution.md`
