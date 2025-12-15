# Tasks: AI-native Textbook Multi-Agent System

**Input**: Design documents from `/specs/sub-agent-skills/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, ADR-001
**Architecture Decision**: ADR-001 - OpenAI-Agents-SDK with Gemini (gemini-2.5-flash)

**Tests**: Tests are OUT OF SCOPE per specification. Manual testing via API and UI.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US6)

## Path Conventions

- **Backend**: `backend/` - Python FastAPI
- **Frontend**: `my-ai-robotics-book/src/` - React/Docusaurus

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify environment and dependencies are ready

- [x] T001 Verify Python 3.11+ installed and virtual environment active
- [x] T002 [P] Verify `openai-agents-sdk` is installed (`pip install openai-agents-sdk`)
- [x] T003 [P] Verify `.env` contains `GEMINI_API_KEY` and `GEMINI_BASE_URL`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

### [x] T004 [US6] Update `backend/skill_agents/base_agent.py` with LLM Integration

**File**: `backend/skill_agents/base_agent.py`
**Action**: UPDATE (replace entire file)

```python
"""Base class for all skill agents with LLM integration."""

from abc import ABC, abstractmethod
from typing import Dict
import os

from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI


class BaseSkillAgent(ABC):
    """Abstract base class for all skill agents.

    Provides shared Gemini model configuration via OpenAI-Agents-SDK.
    All sub-agents must inherit and define name, description, instructions.
    """

    name: str = "base"
    description: str = "Base skill agent"
    instructions: str = "You are a helpful assistant."

    def __init__(self):
        """Initialize the agent with Gemini model via OpenAI-compatible API."""
        self.provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
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

    def run(self, query: str) -> Dict[str, str]:
        """Execute the agent's skill with LLM.

        Args:
            query: The user's input query

        Returns:
            Dict with 'response' key containing the generated output.

        Raises:
            ValueError: If query is empty.
        """
        query = self.validate_input(query, "query")
        result = Runner.run_sync(self.agent, input=query)
        return {"response": result.final_output}

    def validate_input(self, value: str, field_name: str) -> str:
        """Validate and sanitize input.

        - Strips whitespace
        - Raises ValueError if empty
        - Truncates to 2000 chars with notice

        Args:
            value: The input value to validate
            field_name: Name of the field for error messages

        Returns:
            Sanitized input string

        Raises:
            ValueError: If input is empty or None
        """
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")

        value = value.strip()
        if len(value) > 2000:
            value = value[:2000] + "... [truncated]"

        return value
```

---

### [x] T005 [P] [US6] Create `backend/skill_agents/main_orchestrator.py`

**File**: `backend/skill_agents/main_orchestrator.py`
**Action**: CREATE (new file)

```python
"""Main Orchestrator Agent that routes requests to sub-agents."""

import os
from typing import Dict, Optional

from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from .glossary_agent import GlossaryAgent
from .diagram_agent import DiagramAgent
from .translation_agent import TranslationAgent
from .exercises_agent import ExercisesAgent


class MainOrchestratorAgent:
    """Routes requests to appropriate sub-agents based on skill parameter."""

    def __init__(self):
        """Initialize orchestrator with all sub-agents."""
        self.agents = {
            "glossary": GlossaryAgent(),
            "diagram": DiagramAgent(),
            "translate": TranslationAgent(),
            "exercises": ExercisesAgent(),
        }
        self.default_agent = self._create_default_agent()

    def _create_default_agent(self) -> Agent:
        """Create a default agent for general queries."""
        provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        )
        model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=provider
        )
        return Agent(
            name="default_assistant",
            instructions="""You are a helpful assistant for an AI and robotics textbook.
Answer questions about AI, robotics, and related topics in a clear, educational manner.
Keep responses concise and suitable for students.""",
            model=model
        )

    def route(self, query: str, skill: Optional[str] = None) -> Dict[str, str]:
        """Route query to appropriate agent based on skill.

        Args:
            query: The user's input query
            skill: Optional skill identifier (glossary, diagram, translate, exercises)

        Returns:
            Dict with 'response' key containing the generated output.
        """
        if not query or not query.strip():
            return {"response": "Please provide a question or topic."}

        # Route to specific skill agent if skill is provided
        if skill and skill in self.agents:
            return self.agents[skill].run(query)

        # Use default agent for general queries
        result = Runner.run_sync(self.default_agent, input=query)
        return {"response": result.final_output}
```

---

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Access Glossary via Chatbot (Priority: P1)

**Goal**: Click Glossary button, get simple term definition in chat

**Independent Test**: Click Glossary button → predefined query sent with `skill: "glossary"` → definition appears

### [x] T006 [US1] Update `backend/skill_agents/glossary_agent.py` with LLM

**File**: `backend/skill_agents/glossary_agent.py`
**Action**: UPDATE (replace entire file)

```python
"""Glossary Agent for generating term definitions."""

from .base_agent import BaseSkillAgent


class GlossaryAgent(BaseSkillAgent):
    """Agent that provides simple, clear definitions for technical terms."""

    name = "glossary_agent"
    description = "Provides glossary definitions for AI and robotics terms"
    instructions = """You are a glossary expert for an AI and robotics textbook.

When given a term or topic:
1. Provide a simple, clear definition in 2-3 sentences
2. Use plain language suitable for students
3. Include a brief example if helpful
4. Avoid jargon unless defining that jargon

Format: Start with the term, then a colon, then the definition.
Example: "Robot: A machine capable of carrying out complex actions automatically, especially one programmable by a computer. For example, a robotic arm in a factory that assembles car parts."
"""
```

---

## Phase 4: User Story 2 - Generate ASCII Diagram (Priority: P1)

**Goal**: Click Diagram button, get ASCII diagram showing components/relationships

**Independent Test**: Click Diagram button → predefined query sent with `skill: "diagram"` → ASCII diagram appears

### [x] T007 [US2] Update `backend/skill_agents/diagram_agent.py` with LLM

**File**: `backend/skill_agents/diagram_agent.py`
**Action**: UPDATE (replace entire file)

```python
"""Diagram Agent for generating ASCII diagrams."""

from .base_agent import BaseSkillAgent


class DiagramAgent(BaseSkillAgent):
    """Agent that creates ASCII art diagrams for topics."""

    name = "diagram_agent"
    description = "Generates ASCII diagrams for AI and robotics concepts"
    instructions = """You are a diagram generator for an AI and robotics textbook.

When given a topic:
1. Create an ASCII art diagram showing the main components
2. Use boxes made with +, -, | characters
3. Use arrows (-->, <--, <-->) to show relationships
4. Label each component clearly
5. Keep the diagram readable in a monospace font
6. Add a brief 1-2 sentence explanation below the diagram

Example format:
```
+------------+       +------------+
|   Sensor   | ----> | Controller |
+------------+       +------------+
                           |
                           v
                     +------------+
                     |  Actuator  |
                     +------------+
```
This shows how sensor data flows to the controller, which then commands the actuator.
"""
```

---

## Phase 5: User Story 3 - Translate to Urdu (Priority: P2)

**Goal**: Click Translate button, get Urdu translation of English text

**Independent Test**: Click Translate button → predefined query sent with `skill: "translate"` → Urdu text appears

### [x] T008 [US3] Update `backend/skill_agents/translation_agent.py` with LLM

**File**: `backend/skill_agents/translation_agent.py`
**Action**: UPDATE (replace entire file)

```python
"""Translation Agent for English to Urdu translation."""

from .base_agent import BaseSkillAgent


class TranslationAgent(BaseSkillAgent):
    """Agent that translates English text to Urdu."""

    name = "translation_agent"
    description = "Translates English text to Urdu"
    instructions = """You are a translator for an AI and robotics textbook.

When given English text:
1. Translate the text to Urdu
2. Preserve technical terms in English where appropriate (in parentheses)
3. Maintain the original meaning and context
4. Use clear, readable Urdu script
5. If the input is a single word, provide both the translation and a brief definition in Urdu

Output format:
- For sentences: Provide the Urdu translation directly
- For single terms: Term (English): ترجمہ - مختصر تعریف

Example:
Input: "Artificial Intelligence"
Output: مصنوعی ذہانت (Artificial Intelligence) - کمپیوٹر سسٹمز جو انسانی ذہانت جیسے کام کر سکتے ہیں۔
"""
```

---

## Phase 6: User Story 4 - Generate Practice Exercises (Priority: P2)

**Goal**: Click Exercises button, get 3 practice questions at different difficulty levels

**Independent Test**: Click Exercises button → predefined query with `skill: "exercises"` → 3 questions appear

### [x] T009 [US4] Update `backend/skill_agents/exercises_agent.py` with LLM

**File**: `backend/skill_agents/exercises_agent.py`
**Action**: UPDATE (replace entire file)

```python
"""Exercises Agent for generating practice questions."""

from .base_agent import BaseSkillAgent


class ExercisesAgent(BaseSkillAgent):
    """Agent that generates difficulty-graded practice questions."""

    name = "exercises_agent"
    description = "Generates practice exercises for AI and robotics topics"
    instructions = """You are an exercise generator for an AI and robotics textbook.

When given a chapter or topic:
1. Generate exactly 3 practice questions
2. Label each question clearly with its difficulty level
3. Follow this format:

**Easy (Recall):** A basic question testing definition or recall of facts.

**Medium (Application):** A question requiring understanding and application of concepts.

**Advanced (Analysis):** A question requiring critical thinking, design, or problem-solving.

Make questions specific to the given topic and suitable for students learning AI and robotics.
"""
```

---

## Phase 7: User Story 5 & 6 - Integration (Priority: P1, P3)

**Goal**: Unified API endpoint and orchestrator routing

### [x] T010 [US5] [US6] Update `backend/skill_agents/__init__.py` exports

**File**: `backend/skill_agents/__init__.py`
**Action**: UPDATE (replace entire file)

```python
"""Skill agents package exports."""

from .base_agent import BaseSkillAgent
from .glossary_agent import GlossaryAgent
from .diagram_agent import DiagramAgent
from .translation_agent import TranslationAgent
from .exercises_agent import ExercisesAgent
from .main_orchestrator import MainOrchestratorAgent

__all__ = [
    "BaseSkillAgent",
    "GlossaryAgent",
    "DiagramAgent",
    "TranslationAgent",
    "ExercisesAgent",
    "MainOrchestratorAgent",
]
```

---

### [x] T011 [US5] [US6] Update `backend/main.py` with `/api/chatbot` route

**File**: `backend/main.py`
**Action**: UPDATE (add imports, model, and route)

**Step 1**: Add import after line 13 (after `from skills_routes import skills_router`):

```python
from skill_agents import MainOrchestratorAgent
```

**Step 2**: Add new Pydantic model after `QueryRequest` class (around line 18):

```python
class ChatbotRequest(BaseModel):
    query: str
    skill: str | None = None
```

**Step 3**: Add global orchestrator after line 31 (after `app.include_router(skills_router)`):

```python
# Initialize main orchestrator agent
orchestrator = MainOrchestratorAgent()
```

**Step 4**: Add new endpoint before the existing routes (around line 62):

```python
@app.post("/api/chatbot")
def chatbot_query(req: ChatbotRequest):
    """Unified chatbot endpoint with skill-based routing.

    Args:
        req: ChatbotRequest with query and optional skill

    Returns:
        JSON with 'response' key containing generated text
    """
    try:
        if not req.query or not req.query.strip():
            return {"response": "Please provide a question or topic."}

        result = orchestrator.route(req.query, req.skill)
        return result
    except ValueError as e:
        return {"response": str(e)}
    except Exception as e:
        return {"response": "An error occurred. Please try again."}
```

---

## Phase 8: Frontend - Skill Buttons in Chatbot

**Goal**: Chatbot shows 4 skill buttons initially, disappear after first click

### [x] T012 [US1-5] Update `my-ai-robotics-book/src/components/Chatbot/index.tsx`

**File**: `my-ai-robotics-book/src/components/Chatbot/index.tsx`
**Action**: UPDATE (replace entire file)

```tsx
import React, { useState, useCallback, useRef, useEffect } from 'react';
import styles from './Chatbot.module.css';

// Configure your backend URL here
const API_BASE_URL = 'YOUR_BACKEND_URL' || 'http://localhost:8000';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
}

interface SkillButton {
  label: string;
  icon: string;
  skill: string;
  query: string;
}

const SKILL_BUTTONS: SkillButton[] = [
  { label: 'Glossary', icon: '📘', skill: 'glossary', query: 'Explain this term to me' },
  { label: 'Diagram', icon: '📊', skill: 'diagram', query: 'Show me a diagram for this topic' },
  { label: 'Translate', icon: '🌐', skill: 'translate', query: 'Translate this to Urdu' },
  { label: 'Exercises', icon: '✏️', skill: 'exercises', query: 'Generate practice questions' },
];

function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSkillButtons, setShowSkillButtons] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = useCallback(() => {
    setIsOpen((prev) => !prev);
  }, []);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      setInputMessage(e.target.value);
    },
    []
  );

  const sendMessage = useCallback(
    async (query: string, skill: string | null = null) => {
      if (!query.trim()) return;

      const userMessage: Message = {
        id: Date.now(),
        text: query,
        sender: 'user',
      };

      setMessages((prev) => [...prev, userMessage]);
      setInputMessage('');
      setIsLoading(true);

      // Hide skill buttons after first interaction
      if (showSkillButtons) {
        setShowSkillButtons(false);
      }

      try {
        const response = await fetch(`${API_BASE_URL}/api/chatbot`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            query,
            skill,
          }),
        });

        if (!response.ok) throw new Error(`HTTP error ${response.status}`);

        const data = await response.json();

        const botMessage: Message = {
          id: Date.now() + 1,
          text: data.response,
          sender: 'bot',
        };

        setMessages((prev) => [...prev, botMessage]);
      } catch (error) {
        console.error('Error sending:', error);

        const errorMessage: Message = {
          id: Date.now() + 1,
          text: 'Connection error. Please check your network and try again.',
          sender: 'bot',
        };

        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [showSkillButtons]
  );

  const handleSkillClick = useCallback(
    (skill: SkillButton) => {
      sendMessage(skill.query, skill.skill);
    },
    [sendMessage]
  );

  const handleKeyPress = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === 'Enter' && !isLoading) {
        sendMessage(inputMessage);
      }
    },
    [inputMessage, isLoading, sendMessage]
  );

  const handleSendClick = useCallback(() => {
    sendMessage(inputMessage);
  }, [inputMessage, sendMessage]);

  return (
    <div className={styles.chatbotContainer}>
      <button className={styles.chatIcon} onClick={toggleChat}>
        💬
      </button>

      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Book Chatbot</h3>
            <button onClick={toggleChat} className={styles.closeButton}>
              ×
            </button>
          </div>

          <div className={styles.chatMessages}>
            {/* Skill buttons shown only at start */}
            {showSkillButtons && messages.length === 0 && (
              <div className={styles.skillButtonsContainer}>
                {SKILL_BUTTONS.map((skill) => (
                  <button
                    key={skill.skill}
                    className={styles.skillButton}
                    onClick={() => handleSkillClick(skill)}
                    disabled={isLoading}
                  >
                    <span className={styles.skillIcon}>{skill.icon}</span>
                    <span className={styles.skillLabel}>{skill.label}</span>
                  </button>
                ))}
              </div>
            )}

            {/* Chat messages */}
            {messages.map((msg) => (
              <div
                key={msg.id}
                className={`${styles.message} ${styles[msg.sender]}`}
              >
                {msg.text}
              </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className={`${styles.message} ${styles.bot}`}>
                Thinking...
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className={styles.chatInputContainer}>
            <input
              type="text"
              className={styles.chatInput}
              placeholder="Ask a question about the book..."
              value={inputMessage}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
            />

            <button
              onClick={handleSendClick}
              className={styles.sendButton}
              disabled={isLoading || !inputMessage.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default Chatbot;
```

---

### [x] T013 [P] [US1-5] Update `my-ai-robotics-book/src/components/Chatbot/Chatbot.module.css`

**File**: `my-ai-robotics-book/src/components/Chatbot/Chatbot.module.css`
**Action**: UPDATE (add skill button styles to end of file)

```css
/* Skill Buttons Container */
.skillButtonsContainer {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  padding: 15px;
}

.skillButton {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px 10px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 70px;
}

.skillButton:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #007bff;
}

.skillButton:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.skillIcon {
  font-size: 24px;
  margin-bottom: 5px;
}

.skillLabel {
  font-size: 12px;
  font-weight: 500;
  color: #333;
}

/* Dark mode support */
[data-theme='dark'] .skillButton {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  border-color: #4a5568;
}

[data-theme='dark'] .skillLabel {
  color: #e2e8f0;
}

[data-theme='dark'] .skillButton:hover {
  border-color: #63b3ed;
}
```

---

## Phase 9: Verification & Integration Testing

**Purpose**: Verify complete flow works end-to-end

- [x] T014 Verify `.env` has required variables: `GEMINI_API_KEY`, `GEMINI_BASE_URL`
- [ ] T015 [P] Start backend: `cd backend && uvicorn main:app --reload`
- [ ] T016 [P] Start frontend: `cd my-ai-robotics-book && npm start`
- [ ] T017 Test Glossary skill button → verify definition appears
- [ ] T018 Test Diagram skill button → verify ASCII diagram appears
- [ ] T019 Test Translate skill button → verify Urdu text appears
- [ ] T020 Test Exercises skill button → verify 3 questions appear
- [ ] T021 Test follow-up conversation → verify normal chat works
- [ ] T022 Test error handling → verify friendly error messages

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ─────────────────────────────────────────────────┐
       │                                                          │
       v                                                          │
Phase 2 (Foundational: T004, T005) ───────────────────────────────┤
       │                                                          │
       ├────────────────────────────────────────────────────┐     │
       │                                                    │     │
       v                                                    v     │
Phase 3-6 (Skill Agents: T006-T009) [PARALLEL]    Phase 8 (Frontend)
       │                                                    │     │
       v                                                    │     │
Phase 7 (Integration: T010, T011)                          │     │
       │                                                    │     │
       └────────────────────────────────────────────────────┘     │
                              │                                   │
                              v                                   │
                    Phase 9 (Testing: T014-T022) ─────────────────┘
```

### Task Execution Order

| Order | Tasks | Can Run Parallel | Description |
|-------|-------|------------------|-------------|
| 1 | T001 | No | Verify Python |
| 2 | T002, T003 | Yes | Verify deps and .env |
| 3 | T004, T005 | Yes | BaseSkillAgent + Orchestrator |
| 4 | T006, T007, T008, T009 | Yes | All 4 skill agents |
| 5 | T010, T011 | No (sequential) | Package exports + main.py route |
| 6 | T012, T013 | Yes | Frontend TSX + CSS |
| 7 | T014-T022 | Sequential | Testing |

### Parallel Opportunities

| Tasks | Can Run Together | Reason |
|-------|------------------|--------|
| T002, T003 | Yes | Different checks, no file conflicts |
| T004, T005 | Yes | Different files: base_agent.py, main_orchestrator.py |
| T006, T007, T008, T009 | Yes | Different files: glossary, diagram, translation, exercises |
| T012, T013 | Yes | Different files: index.tsx, Chatbot.module.css |
| T015, T016 | Yes | Different processes: backend server, frontend server |

---

## Implementation Strategy

### MVP First Approach

1. **Phase 1-2**: Setup + Foundational (T001-T005)
2. **Phase 3**: User Story 1 - Glossary (T006)
3. **Phase 7-8**: Integration + Frontend (T010-T013)
4. **VALIDATE**: Test glossary button works end-to-end
5. **Deploy/Demo**: MVP ready!

### Full Implementation Order

```bash
# 1. Setup
T001: Verify Python 3.11+
T002, T003: Verify deps (parallel)

# 2. Foundational (parallel)
T004: Update base_agent.py
T005: Create main_orchestrator.py

# 3. Skill Agents (all parallel)
T006: Update glossary_agent.py
T007: Update diagram_agent.py
T008: Update translation_agent.py
T009: Update exercises_agent.py

# 4. Integration (sequential)
T010: Update __init__.py
T011: Update main.py

# 5. Frontend (parallel)
T012: Update index.tsx
T013: Update Chatbot.module.css

# 6. Testing (sequential)
T014-T022: End-to-end verification
```

---

## Summary

| Phase | Tasks | Parallel | Purpose |
|-------|-------|----------|---------|
| Phase 1: Setup | 3 | 2 | Environment verification |
| Phase 2: Foundational | 2 | 2 | BaseSkillAgent + Orchestrator |
| Phase 3: US1 Glossary | 1 | 0 | Glossary agent |
| Phase 4: US2 Diagram | 1 | 0 | Diagram agent |
| Phase 5: US3 Translate | 1 | 0 | Translation agent |
| Phase 6: US4 Exercises | 1 | 0 | Exercises agent |
| Phase 7: US5+6 Integration | 2 | 0 | Exports + API route |
| Phase 8: Frontend | 2 | 2 | Chatbot with skill buttons |
| Phase 9: Testing | 9 | 2 | End-to-end verification |
| **Total** | **22** | **8** | |

---

## Notes

- [P] tasks can run in parallel (different files, no dependencies)
- All agent files UPDATE existing template-based files with LLM-powered versions
- Only `main_orchestrator.py` is a NEW file
- Frontend uses `YOUR_BACKEND_URL` placeholder - configure at deployment
- "Thinking..." indicator shows during LLM processing (2-5 seconds typical)
- No unit tests per spec (out of scope)
- Backend runs on port 8000, frontend on port 3000
- CORS is pre-configured in existing `main.py`
- Architecture follows ADR-001: OpenAI-Agents-SDK + Gemini (gemini-2.5-flash)
