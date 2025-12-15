# Data Model: AI-native Textbook Multi-Agent System

**Feature**: 001-sub-agent-skills
**Date**: 2025-12-12
**Status**: Complete (Updated)

## Overview

This document defines the data structures for the AI-native Multi-Agent System. The system uses **OpenAI-Agents-SDK with Gemini model** for AI-powered responses via a chatbot interface with skill buttons.

---

## 1. Python Backend Entities

### 1.1 BaseSkillAgent (Abstract Base with LLM Integration)

```python
from abc import ABC, abstractmethod
from typing import Dict
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
import os

class BaseSkillAgent(ABC):
    """Base class for all skill agents with shared LLM functionality.

    Provides:
    - Shared model configuration (Gemini via OpenAI-compatible API)
    - Common run execution pattern
    - Input validation helpers
    """

    name: str  # Agent identifier
    description: str  # Human-readable description
    instructions: str  # Agent-specific prompt/instructions

    def __init__(self):
        """Initialize the agent with Gemini model via OpenAI-Agents-SDK."""
        self.provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com/v1beta/openai/")
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
        """Execute the agent with the given query.

        Args:
            query: User input text

        Returns:
            {"response": "...generated output..."}
        """
        query = self.validate_input(query, "query")
        result = Runner.run_sync(self.agent, input=query)
        return {"response": result.final_output}

    def validate_input(self, value: str, field_name: str) -> str:
        """Validate and sanitize input."""
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        value = value.strip()
        if len(value) > 2000:
            value = value[:2000] + "... [truncated]"
        return value
```

---

### 1.2 GlossaryAgent

```python
class GlossaryAgent(BaseSkillAgent):
    name = "glossary"
    description = "Generate simple definitions for technical terms"
    instructions = """You are a glossary expert for an AI and robotics textbook.
    When given a term or topic:
    1. Provide a simple, clear definition
    2. Use plain language suitable for students
    3. Keep the explanation concise (2-3 sentences)
    4. Include an example if helpful"""
```

---

### 1.3 DiagramAgent

```python
class DiagramAgent(BaseSkillAgent):
    name = "diagram"
    description = "Generate ASCII block diagrams for topics"
    instructions = """You are a diagram generator for an AI and robotics textbook.
    When given a topic:
    1. Create an ASCII art diagram showing the main components
    2. Use boxes, arrows, and labels to show relationships
    3. Keep the diagram readable in a fixed-width font
    4. Add a brief explanation below the diagram"""
```

---

### 1.4 TranslateAgent

```python
class TranslateAgent(BaseSkillAgent):
    name = "translate"
    description = "Translate English text to Urdu"
    instructions = """You are a translator for an AI and robotics textbook.
    When given English text:
    1. Translate the text to Urdu
    2. Preserve technical terms where appropriate
    3. Maintain the meaning and context
    4. Use clear, readable Urdu script"""
```

---

### 1.5 ExercisesAgent

```python
class ExercisesAgent(BaseSkillAgent):
    name = "exercises"
    description = "Generate practice exercises at different difficulty levels"
    instructions = """You are an exercise generator for an AI and robotics textbook.
    When given a chapter or topic:
    1. Generate exactly 3 practice questions
    2. Label them: Easy, Medium, Advanced
    3. Easy: Basic recall/definition questions
    4. Medium: Application/explanation questions
    5. Advanced: Analysis/design questions"""
```

---

### 1.6 MainOrchestratorAgent

```python
from typing import Optional

class MainOrchestratorAgent:
    """Main orchestrator that routes requests to appropriate sub-agents."""

    def __init__(self):
        """Initialize all sub-agents."""
        self.agents = {
            "glossary": GlossaryAgent(),
            "diagram": DiagramAgent(),
            "translate": TranslateAgent(),
            "exercises": ExercisesAgent(),
        }

        # Default agent for general queries
        self.default_agent = self._create_default_agent()

    def _create_default_agent(self) -> Agent:
        """Create default agent for non-skill queries."""
        provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL")
        )
        model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=provider
        )
        return Agent(
            name="general",
            instructions="You are a helpful assistant for an AI and robotics textbook.",
            model=model
        )

    def route(self, query: str, skill: Optional[str] = None) -> Dict[str, str]:
        """Route query to appropriate agent based on skill.

        Args:
            query: User input text
            skill: Skill name (glossary, diagram, translate, exercises) or None

        Returns:
            {"response": "...generated output..."}
        """
        if skill and skill.lower() in self.agents:
            return self.agents[skill.lower()].run(query)
        else:
            # Use default agent for general queries
            result = Runner.run_sync(self.default_agent, input=query)
            return {"response": result.final_output}


# Singleton instance
orchestrator = MainOrchestratorAgent()
```

---

## 2. API Request/Response Models (Pydantic)

### 2.1 Chatbot Request Model

```python
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class SkillType(str, Enum):
    GLOSSARY = "glossary"
    DIAGRAM = "diagram"
    TRANSLATE = "translate"
    EXERCISES = "exercises"

class ChatbotRequest(BaseModel):
    """Request model for /api/chatbot endpoint."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User query or message"
    )
    skill: Optional[SkillType] = Field(
        None,
        description="Skill to invoke (glossary, diagram, translate, exercises)"
    )
```

### 2.2 Response Models

```python
class ChatbotResponse(BaseModel):
    """Success response from chatbot."""
    response: str = Field(..., description="Generated response from agent")

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
```

---

## 3. TypeScript Frontend Types

```typescript
// types.ts

// Skill types
export type SkillType = 'glossary' | 'diagram' | 'translate' | 'exercises';

// Skill button configuration
export interface SkillButtonConfig {
  id: SkillType;
  label: string;
  icon: string;
  predefinedQuery: string;
}

// API Request/Response
export interface ChatbotRequest {
  query: string;
  skill?: SkillType;
}

export interface ChatbotResponse {
  response: string;
}

export interface ErrorResponse {
  error: string;
}

// Chat message
export interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
}

// Chatbot component state
export interface ChatbotState {
  messages: Message[];
  inputMessage: string;
  isLoading: boolean;
  showSkillButtons: boolean;
}
```

---

## 4. Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MainOrchestratorAgent                             │
│                                                                      │
│   route(query, skill) → routes to appropriate agent                  │
│                                                                      │
│   ┌──────────────────────────────────────────────────────────────┐  │
│   │                      Sub-Agents                               │  │
│   │                                                               │  │
│   │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐     │  │
│   │  │ GlossaryAgent │  │ DiagramAgent  │  │TranslateAgent │     │  │
│   │  │               │  │               │  │               │     │  │
│   │  │ run(query)    │  │ run(query)    │  │ run(query)    │     │  │
│   │  │ → Agent(LLM)  │  │ → Agent(LLM)  │  │ → Agent(LLM)  │     │  │
│   │  └───────────────┘  └───────────────┘  └───────────────┘     │  │
│   │                                                               │  │
│   │  ┌───────────────┐  ┌───────────────┐                        │  │
│   │  │ExercisesAgent │  │ DefaultAgent  │ (for general queries)  │  │
│   │  │               │  │               │                        │  │
│   │  │ run(query)    │  │ run(query)    │                        │  │
│   │  │ → Agent(LLM)  │  │ → Agent(LLM)  │                        │  │
│   │  └───────────────┘  └───────────────┘                        │  │
│   └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ called by
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FastAPI Route                                 │
│                                                                      │
│  POST /api/chatbot                                                   │
│    Request:  { query: string, skill?: SkillType }                   │
│    Response: { response: string }                                    │
│                                                                      │
│  Routing logic:                                                      │
│    skill="glossary"  → GlossaryAgent.run(query)                     │
│    skill="diagram"   → DiagramAgent.run(query)                      │
│    skill="translate" → TranslateAgent.run(query)                    │
│    skill="exercises" → ExercisesAgent.run(query)                    │
│    skill=null        → DefaultAgent.run(query)                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ called by
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   React Chatbot Component                            │
│                                                                      │
│  Initial State:                                                      │
│    - 4 skill buttons visible                                         │
│    - No messages                                                     │
│                                                                      │
│  On Skill Button Click:                                              │
│    - Send predefined query with skill                                │
│    - Hide skill buttons                                              │
│    - Show "Thinking..." indicator                                    │
│    - Display response as bot message                                 │
│                                                                      │
│  Normal Chat:                                                        │
│    - Input box + send button                                         │
│    - User/bot message bubbles                                        │
│    - Sends query without skill parameter                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Validation Rules

| Field | Type | Validation |
|-------|------|------------|
| query | string | Required, 1-2000 chars, trimmed |
| skill | enum | Optional, one of: glossary, diagram, translate, exercises |
| response | string | Always present in success response |
| error | string | Always present in error response |

---

## 6. State Transitions

### Chatbot UI State Machine

```
┌─────────────────┐
│   INITIAL       │
│  showButtons=T  │
│  messages=[]    │
└────────┬────────┘
         │ click skill button
         ▼
┌─────────────────┐
│   LOADING       │
│  showButtons=F  │
│  isLoading=T    │
│  messages=[user]│
└────────┬────────┘
         │ response received
         ▼
┌─────────────────┐
│   ACTIVE_CHAT   │◄────────────────┐
│  showButtons=F  │                 │
│  isLoading=F    │ send message    │
│  messages=[...] ├─────────────────┘
└─────────────────┘
```

### Agent Processing (Backend)

All agents are stateless - each request is independent with no side effects.

```
Request → Validate → Route → Agent.run() → Response
```

---

## 7. Skill Button Configuration

```typescript
const SKILL_BUTTONS: SkillButtonConfig[] = [
  {
    id: 'glossary',
    label: 'Glossary',
    icon: '📘',
    predefinedQuery: 'Explain this term to me'
  },
  {
    id: 'diagram',
    label: 'Diagram',
    icon: '📊',
    predefinedQuery: 'Show me a diagram for this topic'
  },
  {
    id: 'translate',
    label: 'Translate',
    icon: '🌐',
    predefinedQuery: 'Translate this to Urdu'
  },
  {
    id: 'exercises',
    label: 'Exercises',
    icon: '✏️',
    predefinedQuery: 'Generate practice questions'
  }
];
```
