# Quickstart: AI-native Textbook Multi-Agent System

**Feature**: 001-sub-agent-skills
**Date**: 2025-12-12 (Updated)

## Overview

This guide shows how to run and test the AI-native Multi-Agent System with OpenAI-Agents-SDK and Gemini model, featuring a chatbot with skill buttons.

---

## Prerequisites

1. **Python 3.11+** installed
2. **Node.js 20+** installed
3. **Gemini API Key** from Google AI Studio
4. Existing project dependencies installed:
   - Backend: `cd backend && pip install -r requirements.txt`
   - Frontend: `cd my-ai-robotics-book && npm install`

---

## Environment Setup

### 1. Configure Environment Variables

Create or update `backend/.env`:

```env
# Gemini Configuration (OpenAI-compatible mode)
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Existing variables (keep as-is)
QDRANT_API_KEY=...
QDRANT_URL=...
COHERE_API_KEY=...
```

---

## Quick Start (5 minutes)

### 1. Start Backend Server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Verify: Open http://localhost:8000 - should see `{"status": "FastAPI is running"}`

### 2. Start Frontend (separate terminal)

```bash
cd my-ai-robotics-book
npm start
```

Opens http://localhost:3000 automatically.

---

## Test the Chatbot API

### Test with Skill Parameter

```bash
# Glossary skill
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a Robot?", "skill": "glossary"}'

# Diagram skill
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": "Robot Architecture", "skill": "diagram"}'

# Translate skill
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": "A robot is a machine", "skill": "translate"}'

# Exercises skill
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": "Introduction to Sensors", "skill": "exercises"}'
```

### Test without Skill (General Chat)

```bash
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about AI in robotics"}'
```

Expected response format:
```json
{"response": "AI in robotics combines artificial intelligence with..."}
```

---

## Test Error Handling

### Empty Query

```bash
curl -X POST http://localhost:8000/api/chatbot \
  -H "Content-Type: application/json" \
  -d '{"query": ""}'
```

Expected:
```json
{"error": "Query cannot be empty"}
```

---

## Chatbot UI Features

When you open the chatbot in the frontend:

1. **Initial State**: Four skill buttons displayed, no messages
   - Glossary
   - Diagram
   - Translate
   - Exercises

2. **Click Skill Button**:
   - Predefined query sent with skill parameter
   - Buttons disappear
   - "Thinking..." indicator shows
   - Response appears as bot message

3. **Continue Chatting**:
   - Use input box to send follow-up messages
   - Messages sent without skill parameter (general chat)
   - User and bot message bubbles displayed

---

## Use Skills Programmatically (Python)

```python
from skill_agents import (
    GlossaryAgent,
    DiagramAgent,
    TranslateAgent,
    ExercisesAgent
)

# Initialize agents
glossary = GlossaryAgent()
diagram = DiagramAgent()
translate = TranslateAgent()
exercises = ExercisesAgent()

# Call each skill
result1 = glossary.run("What is a Sensor?")
print(result1["response"])

result2 = diagram.run("Neural Network")
print(result2["response"])

result3 = translate.run("Hello world")
print(result3["response"])

result4 = exercises.run("Introduction to AI")
print(result4["response"])
```

### Using the Orchestrator

```python
from main_orchestrator import orchestrator

# Route to specific skill
result = orchestrator.route("What is a Robot?", skill="glossary")
print(result["response"])

# General query (no skill)
result = orchestrator.route("Tell me about robotics")
print(result["response"])
```

---

## File Locations

| Component | Path |
|-----------|------|
| BaseSkillAgent | `backend/skill_agents/base_agent.py` |
| Sub-agents | `backend/skill_agents/*.py` |
| Orchestrator | `backend/main_orchestrator.py` (or `main_agent.py`) |
| Chatbot route | `backend/main.py` (or separate file) |
| Chatbot component | `my-ai-robotics-book/src/components/Chatbot/index.tsx` |
| API contracts | `specs/sub-agent-skills/contracts/api-contracts.yaml` |

---

## Troubleshooting

### CORS Errors

If you see CORS errors in browser console:
1. Ensure backend is running on port 8000
2. Check `main.py` has CORS middleware configured for `localhost:3000`

### Empty or Error Responses

1. Check backend logs for errors
2. Verify `GEMINI_API_KEY` is set correctly in `.env`
3. Test API directly with curl
4. Check Gemini API quota/limits

### Gemini API Errors

1. Verify API key is valid
2. Check base URL is correct: `https://generativelanguage.googleapis.com/v1beta/openai/`
3. Ensure model name is correct: `gemini-2.5-flash`

### Chatbot Skill Buttons Not Working

1. Check browser DevTools Network tab
2. Verify API URL is correct (`http://localhost:8000`)
3. Check for JavaScript console errors
4. Verify backend is running

---

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chatbot` | POST | Main chatbot with skill routing |
| `/api/skills/glossary` | POST | Legacy: glossary only (deprecated) |
| `/api/skills/diagram` | POST | Legacy: diagram only (deprecated) |
| `/api/skills/translate` | POST | Legacy: translate only (deprecated) |
| `/api/skills/exercises` | POST | Legacy: exercises only (deprecated) |

---

## Next Steps

1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd my-ai-robotics-book && npm start`
3. Open chatbot and test skill buttons
4. Continue conversation with follow-up questions
5. Customize skill button queries as needed
