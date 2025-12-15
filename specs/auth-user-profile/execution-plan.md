# Hackathon Execution Plan: AI-Native Textbook Platform

**Branch**: `003-auth-user-profile`
**Created**: 2025-12-14
**Purpose**: Step-by-step execution plan for hackathon demo-ready implementation

---

## Executive Summary

This execution plan prioritizes a **demo-ready flow** that showcases:
1. **Better Auth + Chatbot Signup** (50 bonus points eligibility)
2. **AI-Powered Learning Personalization** (core innovation)
3. **Skill Agents** (Glossary, Diagram, Translate, Quiz)

### Current Implementation Status

| Component | Status | Notes |
|-----------|--------|-------|
| Backend FastAPI | Done | All routes configured |
| Auth Routes (Better Auth compatible) | Done | `/api/auth/*` endpoints working |
| User Profile Storage | Done | SQLite + JSON columns |
| Skill Agents (4 agents) | Done | Glossary, Diagram, Translate, Quiz |
| Main Orchestrator | Done | Routing to sub-agents |
| Frontend Auth Components | Done | SignupForm, SigninForm, Questionnaire |
| AuthProvider Context | Done | Session management |
| Chatbot with Skills | Done | Skill buttons + quiz MCQ |
| **Chatbot Onboarding** | NOT DONE | Core hackathon feature missing |
| **Personalization Integration** | NOT DONE | Chatbot doesn't use profile |
| **Navbar Auth Buttons** | Partial | Needs integration |

---

## Critical Path: Demo-Ready in 3 Phases

### PHASE 1: Chatbot Onboarding Integration (CRITICAL - Bonus Points)

**Goal**: Chatbot guides signup conversation instead of form-based questionnaire

**Why Critical**:
- This IS the core innovation for hackathon
- Qualifies for 50 bonus points (Better Auth + chatbot signup)
- Creates the "WOW" moment for judges

#### Tasks (Implementation Order)

**1.1 Backend: Onboarding State Machine**
```
Files to Create/Modify:
- backend/auth/onboarding.py (NEW)
- backend/auth/routes.py (MODIFY)
```

Create onboarding endpoints:
- `POST /api/auth/onboarding/start` - Validate credentials, create temp session
- `GET /api/auth/onboarding/question` - Get current question
- `POST /api/auth/onboarding/answer` - Submit answer, advance state
- `GET /api/auth/onboarding/summary` - Get collected answers
- `POST /api/auth/onboarding/complete` - Create user + profile atomically

**1.2 Backend: Question Flow Configuration**
```
File: backend/config/onboarding_questions.py (NEW)
```

Define the conversational flow:
```python
ONBOARDING_QUESTIONS = [
    {
        "id": "welcome",
        "type": "greeting",
        "bot_message": "Welcome! I'm excited to help you learn AI and Robotics. Let's personalize your experience!",
        "next": "programming_level"
    },
    {
        "id": "programming_level",
        "type": "single_select",
        "bot_message": "First, how would you describe your programming experience?",
        "options": ["Beginner", "Intermediate", "Advanced"],
        "field": "software_background.programming_level",
        "next": "languages_known"
    },
    # ... more questions
]
```

**1.3 Frontend: OnboardingChatbot Component**
```
File: my-ai-robotics-book/src/components/Chatbot/OnboardingChatbot.tsx (NEW)
```

- Reuse existing chatbot styling
- Show credential form first (email/password)
- After validation, switch to chatbot conversation mode
- Display questions with clickable option buttons
- Show typing indicator between questions
- Confirmation summary before account creation

**1.4 Integration: Replace SignupForm**
```
Files to Modify:
- my-ai-robotics-book/src/pages/signup.tsx
- my-ai-robotics-book/src/components/Auth/index.tsx
```

Replace traditional form with OnboardingChatbot component.

---

### PHASE 2: Personalization Connection (Core Innovation)

**Goal**: Chatbot uses user profile to personalize responses

**Why Critical**: This is the PAYOFF of collecting profile data

#### Tasks

**2.1 Backend: Profile-Aware Agent Context**
```
Files to Modify:
- backend/skill_agents/base_agent.py
- backend/personalization/interfaces.py
```

Add method to inject user context:
```python
def run_with_profile(self, query: str, user_profile: dict) -> dict:
    """Execute with personalization context."""
    personalized_query = self._build_personalized_prompt(query, user_profile)
    return self.run(personalized_query)
```

**2.2 Backend: Personalized Chatbot Endpoint**
```
File: backend/main.py (MODIFY)
```

Update `/api/chatbot` to:
1. Check for authentication (optional)
2. If authenticated, fetch user profile
3. Pass profile to orchestrator for personalized response

**2.3 Frontend: Profile-Aware Chatbot**
```
File: my-ai-robotics-book/src/components/Chatbot/index.tsx (MODIFY)
```

- Send auth token with chatbot requests
- Show personalized greeting for logged-in users
- Prompt guest users to sign up for personalization

---

### PHASE 3: Polish & Demo Flow (Final Touch)

**Goal**: Seamless demo experience for judges

#### Tasks

**3.1 Navbar Integration**
```
Files to Modify:
- my-ai-robotics-book/src/theme/NavbarItem/NavbarAuthButtons.tsx
- my-ai-robotics-book/src/theme/Root.tsx
```

- Show "Get Started" / "Sign In" for guests
- Show user email + "Sign Out" for authenticated users

**3.2 Demo Route**
```
File: my-ai-robotics-book/src/pages/demo.tsx (NEW - optional)
```

Create a guided demo page that:
1. Explains the innovation
2. Has "Start Demo" button leading to signup
3. Shows before/after personalization comparison

**3.3 Error Handling & Loading States**
- Network error recovery
- Session timeout handling
- Graceful degradation for API failures

---

## Milestones

### Milestone 1: MVP Demo (Phases 1-2)
**Deliverable**: Chatbot signup + personalized responses
**Definition of Done**:
- [ ] User can sign up through chatbot conversation
- [ ] Profile data is collected conversationally
- [ ] After login, chatbot greets user by background
- [ ] Responses show personalization based on skill level

### Milestone 2: Bonus Points Ready (Phase 1 Complete)
**Deliverable**: Better Auth + chatbot signup working
**Definition of Done**:
- [ ] Credentials validated through Better Auth compatible API
- [ ] Chatbot conducts onboarding conversation
- [ ] Account created with complete profile
- [ ] Session cookie set properly

### Milestone 3: Final Polish (Phase 3)
**Deliverable**: Demo-ready platform
**Definition of Done**:
- [ ] Navbar shows auth state correctly
- [ ] Smooth transitions between states
- [ ] Error messages are user-friendly
- [ ] Demo flow can run without errors

---

## Risk Management

### What MUST NOT Be Skipped

| Feature | Why Critical |
|---------|-------------|
| Chatbot onboarding flow | Core innovation, bonus points |
| Profile data collection | Enables personalization |
| Better Auth compatibility | Required for bonus points |
| Working demo flow | Judges need to see it work |

### What CAN Be Simplified (If Time Runs Short)

| Feature | Simplification |
|---------|---------------|
| Question flow | Reduce to 3-4 key questions instead of full sequence |
| Personalization depth | Basic greeting only instead of context-aware responses |
| Error handling | Console errors OK, just don't crash |
| Session recovery | Skip refresh persistence, acceptable for demo |
| Navbar polish | Basic buttons OK, dropdown menu optional |

### Fallback Plan

If chatbot onboarding proves too complex:
1. Keep existing questionnaire form
2. Add chatbot greeting after signup
3. Still demo: "After signup, chatbot knows your background"
4. Still earns partial innovation credit

---

## Demo Flow Script (For Judges)

### Step 1: Guest User Lands on Site
"This is our AI-Native Robotics Textbook. As a guest, the chatbot provides generic responses."

*Demo action*: Click chatbot, ask a question, show generic response.

### Step 2: Start Signup
"But when you sign up, something special happens. Instead of a boring form, our chatbot onboards you conversationally."

*Demo action*: Click "Get Started", enter email/password.

### Step 3: Chatbot Onboarding (THE WOW MOMENT)
"The chatbot now asks about your background in a friendly conversation. This creates engagement and ensures we collect complete profile data."

*Demo action*:
- Answer programming level question (click option)
- Answer languages question (multi-select)
- Continue through 2-3 more questions
- See summary, confirm

### Step 4: Account Created
"Your account is now created with a complete learning profile."

*Demo action*: Show redirect to content area.

### Step 5: Personalized Experience
"Now when you interact with the chatbot, it uses your background to personalize responses."

*Demo action*:
- Ask the same question as before
- Show how response is different (simpler or more advanced based on profile)
- Highlight the personalization

### Step 6: Skills in Action
"The chatbot also has specialized skills for learning."

*Demo action*:
- Click Glossary button, get definition
- Click Quiz button, show MCQ experience
- Show Urdu translation (if relevant)

---

## Implementation Order Summary

```
DAY 1 / FIRST PRIORITY:
========================
1. Create onboarding question configuration
2. Create OnboardingChatbot component
3. Wire up to signup page
4. Test end-to-end flow

DAY 2 / SECOND PRIORITY:
========================
5. Add profile context to chatbot API
6. Update chatbot to use profile
7. Add personalized greeting
8. Navbar auth integration

DAY 3 / POLISH (if time allows):
================================
9. Error handling improvements
10. Loading state polish
11. Demo page creation
12. Practice demo flow
```

---

## Technical Context (Manual Generation)

```json
{
  "FEATURE_SPEC": "specs/auth-user-profile/spec.md",
  "IMPL_PLAN": "specs/auth-user-profile/plan.md",
  "SPECS_DIR": "specs/auth-user-profile/",
  "BRANCH": "003-auth-user-profile",
  "EXISTING_IMPLEMENTATION": {
    "backend_auth": "complete",
    "profile_storage": "complete",
    "skill_agents": "complete",
    "chatbot_ui": "complete",
    "onboarding_chatbot": "NOT_STARTED",
    "personalization": "NOT_STARTED"
  }
}
```

---

## Files to Create/Modify

### New Files
- `backend/auth/onboarding.py` - Onboarding state machine
- `backend/config/onboarding_questions.py` - Question flow config
- `my-ai-robotics-book/src/components/Chatbot/OnboardingChatbot.tsx` - Chatbot signup UI

### Modified Files
- `backend/auth/routes.py` - Add onboarding endpoints
- `backend/main.py` - Add profile context to chatbot
- `backend/skill_agents/base_agent.py` - Add personalization method
- `my-ai-robotics-book/src/pages/signup.tsx` - Use OnboardingChatbot
- `my-ai-robotics-book/src/components/Chatbot/index.tsx` - Send auth, personalized greeting
- `my-ai-robotics-book/src/theme/Root.tsx` - Wrap with AuthProvider

---

## Success Criteria Checklist

### Bonus Points (50 pts)
- [ ] Uses Better Auth compatible authentication
- [ ] Chatbot guides the signup conversation
- [ ] Profile data collected through conversation
- [ ] Account creation is atomic (user + profile)

### Core Innovation
- [ ] Chatbot knows user's background after login
- [ ] Responses are personalized to skill level
- [ ] Clear difference between guest and authenticated experience

### Demo Quality
- [ ] Flow works without errors
- [ ] Transitions are smooth
- [ ] Story is compelling
- [ ] Innovation is visible

---

## Notes

- All existing implementation is preserved and extended
- Focus on integration, not rewriting
- Demo-driven development: always keep end demo in mind
- Test frequently, commit often
