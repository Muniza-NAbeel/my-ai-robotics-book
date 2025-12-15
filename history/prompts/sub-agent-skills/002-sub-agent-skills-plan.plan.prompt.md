---
id: 002
title: Sub-Agent Skills System Implementation Plan
stage: plan
date: 2025-12-11
surface: agent
model: claude-opus-4.5
feature: 001-sub-agent-skills
branch: 001-sub-agent-skills
user: SubhanCoputers
command: /sp.plan
labels: ["planning", "architecture", "sub-agents", "skills-system", "api-design"]
links:
  spec: specs/001-sub-agent-skills/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-sub-agent-skills/plan.md
  - specs/001-sub-agent-skills/research.md
  - specs/001-sub-agent-skills/data-model.md
  - specs/001-sub-agent-skills/quickstart.md
  - specs/001-sub-agent-skills/contracts/api-contracts.yaml
tests:
  - N/A (planning phase, no tests)
---

## Prompt

I want a **high-level plan** before generating code.

Project: My-ai-robotics-book .

Goal: Generate a complete Sub-Agent + Agent Skills system + frontend integration.

=====================================================================
Requirements to include in the plan:

1. One main agent
2. Four sub-agents (glossary, diagrams, translation, exercises)
3. Clean folder and file structure
4. Reusable skills callable from frontend
5. Buttons in the frontend UI to trigger skills
6. API routes to call each sub-agent
7. Integration instructions for Docusaurus pages
8. Output must be modular, extendable, and easy to maintain

=====================================================================
Plan format I want:

1. **Folder structure**
   - List all folders and files

2. **Sub-agent description**
   - Purpose of each agent
   - Input / Output specification

3. **Main agent**
   - How it imports sub-agents
   - Skills object explanation
   - Example run() usage

4. **API routes**
   - Purpose

## Response snapshot

Generated a comprehensive implementation plan for the Sub-Agent Skills System including:

1. **Folder Structure**: Defined `backend/agents/` for Python sub-agents with 5 files (base, glossary, diagram, translation, exercises), `main_agent.py`, `skills_routes.py`. Frontend components at `my-ai-robotics-book/src/components/SkillButtons/` with 4 button components.

2. **Sub-Agent Descriptions**:
   - GlossaryAgent: Term → Definition format
   - DiagramAgent: Topic → ASCII diagram
   - TranslationAgent: English text → Urdu translation
   - ExercisesAgent: Chapter → Easy/Medium/Advanced questions

3. **Main Agent**: Uses `Skills` dataclass to expose all sub-agents via `main_agent.skills.{agent_name}.run()` pattern.

4. **API Routes**: 4 POST endpoints under `/api/skills/` prefix (glossary, diagram, translate, exercises).

5. **Additional Artifacts**: research.md, data-model.md, quickstart.md, api-contracts.yaml (OpenAPI spec).

## Outcome

- ✅ Impact: Complete architectural blueprint for Sub-Agent Skills System
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 5 artifacts created (plan.md, research.md, data-model.md, quickstart.md, api-contracts.yaml)
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation task list
- 🧠 Reflection: Template-based approach chosen per FR-012 (no external API keys); CORS already configured in existing codebase

## Evaluation notes (flywheel)

- Failure modes observed: None - all technical decisions resolved
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): Standard /sp.plan command
- Next experiment (smallest change to try): Execute /sp.tasks to create implementation checklist
