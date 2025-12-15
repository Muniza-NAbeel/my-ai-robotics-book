---
id: 005
title: Multi-Agent AI System Plan Update
stage: plan
date: 2025-12-12
surface: agent
model: claude-opus-4-5-20251101
feature: sub-agent-skills
branch: 001-sub-agent-skills
user: SubhanCoputers
command: /sp.plan
labels: ["multi-agent", "openai-agents-sdk", "gemini", "fastapi", "react", "chatbot", "architecture"]
links:
  spec: specs/sub-agent-skills/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/sub-agent-skills/plan.md
  - specs/sub-agent-skills/research.md
  - specs/sub-agent-skills/data-model.md
  - specs/sub-agent-skills/quickstart.md
  - specs/sub-agent-skills/contracts/api-contracts.yaml
tests:
  - N/A (planning phase, no code tests)
---

## Prompt

You are helping me build a fully production-ready **AI-Native Textbook System** using a multi-agent architecture.

GOAL
Generate a complete, working, ready-to-run system including:

1) Sub-Agents
2) BaseSkillAgent
3) Main Orchestrator Agent
4) FastAPI Backend (POST /api/chatbot)
5) Frontend React Chatbot UI (TypeScript)
6) Directory / File Structure
7) Instructions to run everything
8) Use of **OpenAI-Agents-SDK** with **Gemini model (OpenAI-compatible mode)**
9) The React file must MODIFY an existing:
      /src/components/Chatbot/index.tsx
   → Do NOT create a new file, only output updated code.

REQUIRED FILE STRUCTURE

/agents/
    base-skill-agent.py
    glossary-agent.py
    diagram-agent.py
    translate-agent.py
    exercises-agent.py
    main-orchestrator-agent.py

/api/
    chatbot.py    # FastAPI POST route

## Response snapshot

Updated the implementation plan for the AI-native Textbook Multi-Agent System to reflect:

**Key Architecture Changes (from template-based to AI-powered):**
1. **OpenAI-Agents-SDK Integration**: BaseSkillAgent now uses OpenAI-Agents-SDK with Gemini model in OpenAI-compatible mode
2. **Unified API Endpoint**: Single `/api/chatbot` endpoint with skill routing (replaces separate skill endpoints)
3. **Chatbot with Skill Buttons**: React component modified to show 4 skill buttons initially, which disappear after first click
4. **MainOrchestratorAgent**: Routes requests to appropriate sub-agent based on skill parameter

**Artifacts Generated/Updated:**
- `plan.md` - Full implementation plan with component designs
- `research.md` - Updated with OpenAI-Agents-SDK patterns and decisions
- `data-model.md` - Updated entity definitions with LLM integration
- `quickstart.md` - Updated setup and testing instructions
- `contracts/api-contracts.yaml` - New unified `/api/chatbot` endpoint (v2.0.0)

**Technical Stack:**
- Python 3.11+ with FastAPI + openai-agents-sdk
- Gemini 2.5 Flash via OpenAI-compatible mode
- React 19 + TypeScript
- Docusaurus 3.9.2

## Outcome

- Impact: Complete architecture redesign from templates to AI-powered agents
- Tests: N/A (planning phase)
- Files: 5 planning documents updated
- Next prompts: `/sp.tasks` to generate implementation task breakdown
- Reflection: Major pivot from template-based to LLM-based approach aligns with user's explicit OpenAI-Agents-SDK requirement

## Evaluation notes (flywheel)

- Failure modes observed: None - plan successfully updated
- Graders run and results (PASS/FAIL): Manual review PASS (all artifacts consistent)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with /sp.tasks to validate task breakdown
