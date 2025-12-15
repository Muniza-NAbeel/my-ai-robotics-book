---
id: 004
title: Update Multi-Agent Textbook System Spec
stage: spec
date: 2025-12-12
surface: agent
model: claude-opus-4-5-20251101
feature: sub-agent-skills
branch: 001-sub-agent-skills
user: SubhanCoputers
command: /sp.specify
labels: ["multi-agent", "chatbot", "openai-agents-sdk", "gemini", "fastapi", "react"]
links:
  spec: specs/sub-agent-skills/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/sub-agent-skills/spec.md
  - specs/sub-agent-skills/checklists/requirements.md
tests:
  - N/A (spec update, no tests)
---

## Prompt

You are helping me build an AI-native Textbook System with modular Agents.

🎯 GOAL:
Generate a fully complete, production-ready, multi-agent architecture that includes:

1) Sub-Agents
2) BaseSkillAgent
3) Main Orchestrator Agent
4) FastAPI Backend Route
5) Frontend React Chatbot Integration
6) File Structure + Instructions
7) Use of OpenAI-Agents-SDK with Gemini model (OpenAI-compatible mode)

────────────────────────────────────────
📁 REQUIRED FILE STRUCTURE
────────────────────────────────────────

/agents/
    base-skill-agent.py
    glossary-agent.py
    diagram-agent.py
    translate-agent.py
    exercises-agent.py
    main-orchestrator-agent.py

/api/
    chatbot.py    # FastAPI POST route

🎯 TASK:
Generate a complete React + TypeScript chatbot component:

File: /src/components/Chatbot/index.tsx

─────────────────────────────
UI REQUIREMENTS
─────────────────────────────

1. When chatbot opens → NO default messages.
2. Instead show four skill buttons: Glossary, Diagram, Translate, Exercises
3. When user clicks a button → automatically send predefined question with skill value
4. After clicking a button → Buttons disappear, chat continues normally
5. Chat should have: Message bubbles, "Thinking…" indicator, Input box + send button
6. Replace backend URL with placeholder: YOUR_BACKEND_URL

────────────────────────────────────────
🧠 SUB-AGENT DEFINITIONS
────────────────────────────────────────

GlossaryAgent: input term → output definition
DiagramAgent: input topic → output ASCII diagram
TranslationAgent: input English text → output Urdu translation
ExercisesAgent: input chapter/topic → output 3 practice questions

BaseSkillAgent: reusable helpers, shared LLM call, OpenAI-Agents-SDK usage

## Response snapshot

Updated the feature specification for the AI-native Textbook Multi-Agent System to incorporate:

1. **New Architecture**: Added BaseSkillAgent class, MainOrchestratorAgent, and updated file structure with `/agents/` and `/api/` directories
2. **Chatbot Integration**: Added new user stories for skill button interaction, conversation continuation, and "Thinking..." indicator
3. **Technology Stack**: Added requirements for OpenAI-Agents-SDK with Gemini model in OpenAI-compatible mode
4. **16 Functional Requirements**: Covering all agents, API routes, and React chatbot component
5. **10 Success Criteria**: Measurable outcomes for response times, UI behavior, and system integration
6. **File Structure Reference**: Clear mapping of all required files for implementation

Specification validated against quality checklist - all items pass.

## Outcome

- ✅ Impact: Comprehensive spec update aligning with new multi-agent architecture requirements
- 🧪 Tests: N/A (spec document, no code tests)
- 📁 Files: specs/sub-agent-skills/spec.md, specs/sub-agent-skills/checklists/requirements.md
- 🔁 Next prompts: `/sp.plan` to design implementation architecture, `/sp.tasks` to generate task breakdown
- 🧠 Reflection: Spec now covers end-to-end flow from React chatbot buttons through FastAPI to orchestrated sub-agents

## Evaluation notes (flywheel)

- Failure modes observed: None - spec update successful
- Graders run and results (PASS/FAIL): Manual validation PASS (all checklist items verified)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with /sp.plan to validate architecture decisions
