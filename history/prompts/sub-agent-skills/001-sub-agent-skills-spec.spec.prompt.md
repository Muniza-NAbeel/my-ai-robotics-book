---
id: 001
title: Sub-Agent Skills System Specification
stage: spec
date: 2025-12-11
surface: agent
model: claude-opus-4-5-20251101
feature: 001-sub-agent-skills
branch: 001-sub-agent-skills
user: SubhanCoputers
command: /sp.specify
labels: ["sub-agents", "skills", "docusaurus", "frontend", "api"]
links:
  spec: specs/001-sub-agent-skills/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-sub-agent-skills/spec.md
  - specs/001-sub-agent-skills/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

Generate a complete Sub-Agent + Agent Skills system for my book.

I need:
1. One main agent
2. Four sub-agents (skills)
3. Clean folder and file structure
4. Reusable skills callable from my Docusaurus frontend
5. Simple logic in each agent
6. Buttons in the frontend UI to trigger skills

=====================================================================
Folder Structure (Must create exactly):

/agents/
   main-agent.py
   glossary-agent.py
   diagrams-agent.py
   translate-agent.py
   exercises-agent.py

/src/components/AIButtons/
   GlossaryButton.tsx
   DiagramButton.tsx
   TranslateButton.tsx
   ExercisesButton.tsx

/api/
   glossary.ts
   diagram.ts
   translate.ts
   exercises.ts

=====================================================================
Sub-Agent Requirements (Generate Code):

1) Glossary Agent
- Input: term
- Output: simple glossary definition
- Example return:
  "Glossary: [term] ka matlab yeh hai ... (simple explanation)"

2) Diagram Agent
- Input: topic
- Output: ASCII or pseudo block diagram
- Example:
    [Robot Head]
         |
    [Sensors]
         |
     [Actuators]

3) Translation Agent
- Input: English text
- Output: Urdu translation
- Example:
  "Urdu Translation:\n[translated Urdu text]"

4) Exercises Agent
- Input: chapter text
- Output: 3 questions: easy, medium, advanced

=====================================================================
Main Agent Requirements:

- Import all 4 sub-agents
- Expose them under a unified `skills` object
- run() method must show how to call each skill

=====================================================================
API Routes (Frontend Calls):

Create 4 API routes that accept POST request, read JSON body, call corresponding sub-agent, return JSON response.

=====================================================================
Docusaurus Frontend Buttons:

Create simple React components with props for text, term, topic, chapter.
On button click: send POST request, show loading state, show returned result.

## Response snapshot

Created feature specification for Sub-Agent Skills System with:
- 5 user stories covering glossary, diagram, translate, exercises, and main agent orchestration
- 12 functional requirements (FR-001 to FR-012)
- 8 measurable success criteria
- Clear scope boundaries and assumptions
- Edge cases identified for empty input, long text, API unavailability, and special characters

Branch created: 001-sub-agent-skills
Spec file: specs/001-sub-agent-skills/spec.md
Checklist: specs/001-sub-agent-skills/checklists/requirements.md

## Outcome

- Impact: Created comprehensive specification for sub-agent skills system
- Tests: N/A (specification phase)
- Files: spec.md, checklists/requirements.md created
- Next prompts: /sp.clarify or /sp.plan to proceed with implementation planning
- Reflection: Specification covers all requested components with clear acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All checklist items PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase
