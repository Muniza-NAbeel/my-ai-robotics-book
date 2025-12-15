---
id: 004
title: Update Spec with Chatbot Onboarding
stage: spec
date: 2025-12-14
surface: agent
model: claude-opus-4-5-20251101
feature: auth-user-profile
branch: 003-auth-user-profile
user: local
command: /sp.specify
labels: ["spec", "chatbot", "onboarding", "authentication"]
links:
  spec: specs/auth-user-profile/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/auth-user-profile/spec.md
  - specs/auth-user-profile/checklists/requirements.md
tests:
  - null
---

## Prompt

/sp.specify

You are an expert system designer helping build a hackathon-ready, AI-Native Textbook Platform.

PROJECT CONTEXT
We are building an AI-Native Textbook system for teaching Physical AI & Humanoid Robotics using:
- FastAPI backend
- React / Docusaurus frontend
- Multi-agent AI system (TutorAgent, GlossaryAgent, QuizAgent, etc.)
- A conversational chatbot already exists in the system

HACKATHON REQUIREMENT (CRITICAL)
Participants can earn up to 50 bonus points by implementing:
- Signup & Signin using https://www.better-auth.com/
- During signup, the system must ask users about their software and hardware background
- This background must be used to personalize the learning content

CORE DESIGN IDEA
Authentication is NOT just login security.
Authentication is an intelligent onboarding system powered by a chatbot.

The chatbot must:
- Act as a Signup Assistant
- Ask background questions conversationally
- Store answers in the user profile
- Enable AI personalization after login

GOALS
Specify a complete, production-ready system that:
1. Integrates Better Auth for signup & login
2. Uses the chatbot during signup to collect:
   - Software background level
   - Programming languages known
   - Hardware / robotics experience
   - Learning goals
3. Links Better Auth user identity with a UserProfile
4. Makes AI agents aware of the logged-in user and their background
5. Improves learning experience through personalization

## Response snapshot

Updated existing specification at `specs/auth-user-profile/spec.md` to incorporate chatbot-driven onboarding flow:

**Key Changes:**
1. Added Core Design Concept section emphasizing chatbot as intelligent onboarding system
2. Created User Story 2: Chatbot Conversation Flow (P1) with detailed question sequence
3. Added FR-008 to FR-015 for chatbot onboarding behavior
4. Added OnboardingSession entity for conversation state management
5. Added learning goals collection (FR-018)
6. Updated edge cases for chatbot-specific scenarios
7. Added success criteria SC-006 and SC-007 for chatbot experience

**Spec now includes:**
- 5 User Stories (up from 4)
- 27 Functional Requirements (up from 19)
- 7 Success Criteria (up from 6)
- 3 Key Entities (User, UserProfile, OnboardingSession)

## Outcome

- ✅ Impact: Spec now fully captures chatbot-driven onboarding as core design concept
- 🧪 Tests: N/A (spec phase)
- 📁 Files: 2 files updated (spec.md, requirements.md checklist)
- 🔁 Next prompts: `/sp.plan` to create implementation architecture
- 🧠 Reflection: Previous spec used static form approach; updated to conversational chatbot flow per user requirement

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual checklist validation - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to /sp.plan for implementation design
