# Implementation Plan: AI-native Textbook Multi-Agent System

**Branch**: `001-sub-agent-skills` | **Date**: 2025-12-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/sub-agent-skills/spec.md`

## Summary

Build an AI-powered multi-agent system for the "My AI Robotics Book" project using **OpenAI-Agents-SDK with Gemini model** (OpenAI-compatible mode). The system provides four specialized sub-agents (glossary, diagrams, translation, exercises) with a main orchestrator, unified `/api/chatbot` endpoint, and React chatbot component with skill buttons.

## Technical Context

**Language/Version**: Python 3.11+ (backend agents), TypeScript 5.6+ (frontend components)
**Primary Dependencies**: FastAPI 0.104.1, React 19, Docusaurus 3.9.2, pydantic 2.5.0, openai-agents-sdk
**Storage**: N/A (stateless, no persistence)
**Testing**: Manual testing via API endpoints and UI (unit tests out of scope per spec)
**Target Platform**: Docusaurus static site (frontend) + FastAPI server (backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <5 seconds response time per agent call (SC-001 to SC-004)
**Constraints**: Requires Gemini API key, OpenAI-Agents-SDK for LLM calls
**Scale/Scope**: 5 sub-agents (4 skill + 1 default), 1 orchestrator, 1 API route, 1 React component

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance Status | Notes |
|-----------|-------------------|-------|
| Accuracy through primary-source verification | N/A | Feature generates educational aids, not factual claims |
| Clarity for academic audience | PASS | Output formats are clear (glossary, diagrams, translations, exercises) |
| Reproducibility | PASS | Same query to same skill returns consistent response pattern |
| Rigor | N/A | This is a tooling feature, not content creation |
| Zero plagiarism tolerance | PASS | AI generates original explanations based on prompts |
| Complexity must be justified | PASS | Minimal complexity - modular agents, single endpoint, integrated chatbot |

**Gate Status**: PASS - No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/sub-agent-skills/
├── plan.md              # This file
├── research.md          # Phase 0 output (updated)
├── data-model.md        # Phase 1 output (updated)
├── quickstart.md        # Phase 1 output (updated)
├── contracts/           # Phase 1 output
│   └── api-contracts.yaml
├── checklists/
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
backend/
├── skill_agents/                # Sub-agent modules (UPDATE)
│   ├── __init__.py              # Package exports
│   ├── base_agent.py            # BaseSkillAgent with LLM integration
│   ├── glossary_agent.py        # GlossaryAgent
│   ├── diagram_agent.py         # DiagramAgent
│   ├── translation_agent.py     # TranslateAgent
│   └── exercises_agent.py       # ExercisesAgent
├── main_agent.py                # EXISTING: Update with orchestrator (optional)
├── chatbot_route.py             # NEW: /api/chatbot endpoint
├── main.py                      # EXISTING: Register chatbot route
├── my_agent.py                  # EXISTING: RAG agent (unchanged)
├── skills_routes.py             # EXISTING: Legacy routes (keep)
├── requirements.txt             # EXISTING: Add openai-agents-sdk if needed
└── .env                         # EXISTING: Add GEMINI_API_KEY, GEMINI_BASE_URL

my-ai-robotics-book/
├── src/
│   ├── components/
│   │   ├── Chatbot/             # UPDATE: Add skill buttons
│   │   │   ├── index.tsx        # Modify with skill buttons + state
│   │   │   └── Chatbot.module.css
│   │   ├── SkillButtons/        # EXISTING: May keep for standalone use
│   │   └── HomepageFeatures/    # EXISTING
│   ├── pages/                   # EXISTING
│   └── theme/                   # EXISTING
├── docs/                        # EXISTING: Book content
└── package.json                 # EXISTING: No new dependencies needed
```

**Structure Decision**: Web application structure. Backend agents use OpenAI-Agents-SDK with Gemini. Frontend chatbot modified to include skill buttons.

## Component Design

### 1. BaseSkillAgent (with LLM Integration)

```python
from abc import ABC, abstractmethod
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
import os

class BaseSkillAgent(ABC):
    """Base class with shared Gemini model configuration."""

    name: str
    description: str
    instructions: str

    def __init__(self):
        self.provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL")
        )
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.provider
        )
        self.agent = Agent(
            name=self.name,
            instructions=self.instructions,
            model=self.model
        )

    def run(self, query: str) -> dict:
        result = Runner.run_sync(self.agent, input=query)
        return {"response": result.final_output}
```

### 2. Sub-Agent Definitions

| Agent | Purpose | Instructions Summary |
|-------|---------|---------------------|
| GlossaryAgent | Simple term definitions | Provide clear, concise definitions for students |
| DiagramAgent | ASCII diagrams | Create readable ASCII art with boxes and arrows |
| TranslateAgent | English to Urdu | Translate preserving technical terms |
| ExercisesAgent | Practice questions | Generate Easy, Medium, Advanced questions |

### 3. MainOrchestratorAgent

```python
class MainOrchestratorAgent:
    def __init__(self):
        self.agents = {
            "glossary": GlossaryAgent(),
            "diagram": DiagramAgent(),
            "translate": TranslateAgent(),
            "exercises": ExercisesAgent(),
        }
        self.default_agent = self._create_default_agent()

    def route(self, query: str, skill: str = None) -> dict:
        if skill and skill in self.agents:
            return self.agents[skill].run(query)
        result = Runner.run_sync(self.default_agent, input=query)
        return {"response": result.final_output}
```

### 4. API Route

| Route | Method | Request | Response |
|-------|--------|---------|----------|
| `/api/chatbot` | POST | `{"query": "...", "skill": "glossary\|diagram\|translate\|exercises"}` | `{"response": "..."}` |

### 5. React Chatbot with Skill Buttons

**Initial State**:
- Show 4 skill buttons (Glossary, Diagram, Translate, Exercises)
- No messages displayed

**On Skill Button Click**:
1. Hide buttons
2. Send predefined query with skill parameter
3. Show "Thinking..." indicator
4. Display response as bot message

**After First Interaction**:
- Normal chat with input box
- User/bot message bubbles
- Queries sent without skill parameter

---

## Complexity Tracking

> No violations identified. Design follows smallest viable change principle.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| AI vs Templates | OpenAI-Agents-SDK + Gemini | User explicitly requires AI-powered generation |
| Agent structure | BaseSkillAgent inheritance | Clean code reuse, single model config |
| API design | Single /api/chatbot endpoint | Spec requires unified endpoint with skill routing |
| Frontend | Modify existing Chatbot | User said modify, not create new |

---

## Risk Analysis

1. **Gemini API Latency**: AI responses may take 2-5 seconds.
   *Mitigation*: "Thinking..." indicator in UI; graceful timeout handling.

2. **API Key Exposure**: Gemini key must be protected.
   *Mitigation*: Store in .env; never commit to git; use environment variables.

3. **Model Availability**: Gemini may have rate limits or downtime.
   *Mitigation*: Error handling with retry messaging; consider fallback.

---

## Implementation Order

1. **Backend Agents**: Update BaseSkillAgent with LLM, update sub-agents
2. **Orchestrator**: Create/update MainOrchestratorAgent
3. **API Route**: Add `/api/chatbot` endpoint
4. **Frontend**: Modify Chatbot component with skill buttons
5. **Integration Test**: Test full flow via UI

---

## Follow-up Actions

- [ ] Generate `/sp.tasks` to create implementation task list
- [ ] Add unit tests in future iteration (out of current scope)
- [ ] Consider caching for common queries if performance is an issue
- [ ] Document Gemini API usage limits and billing
