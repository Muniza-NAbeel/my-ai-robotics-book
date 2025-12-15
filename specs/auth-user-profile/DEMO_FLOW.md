# Demo Flow: AI-Native Textbook Platform

**Hackathon Demo Guide for Judges**

This document guides you through the core innovation: **Chatbot-Driven Signup with AI Personalization**.

---

## Quick Start

### Prerequisites
1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. Start the frontend:
   ```bash
   cd my-ai-robotics-book
   npm start
   ```

3. Open browser to: `http://localhost:3000`

---

## Demo Script (5 Minutes)

### Act 1: Guest Experience (30 seconds)

1. **Open Homepage** - Notice the clean landing page
2. **Click "Book" in navbar** - Browse content as guest
3. **Open Chatbot** (bottom-right corner) - See the prompt: "Sign up for a personalized learning experience"
4. **Notice navbar** - Shows "Sign In" and "Get Started" buttons

**Key Point**: Guests can browse but get limited experience.

---

### Act 2: Chatbot-Driven Signup (2 minutes) - THE WOW MOMENT

1. **Click "Get Started"** in navbar
2. **Enter credentials**:
   - Email: `demo@example.com`
   - Password: `Demo1234` (shows validation feedback)
   - Confirm password
3. **Click "Continue"** - Chatbot activates!

4. **Watch the magic**: Chatbot greets you and asks conversational questions:
   - "What's your programming experience?" (select one)
   - "Which languages do you know?" (select multiple)
   - "AI/ML experience level?" (select one)
   - "Web development experience?" (select one)
   - "Robotics experience?" (select one)
   - "Electronics familiarity?" (select one)
   - "Hardware access?" (select multiple)
   - "Learning goals?" (select multiple)

5. **Review profile summary** - Chatbot shows collected data
6. **Click "Create Account"** - Account created with full profile!
7. **Auto-redirect** to content area

**Key Innovation**: Instead of boring forms, users have a conversation with a friendly chatbot that naturally collects their background. This is engaging and ensures complete data collection.

---

### Act 3: Personalized Experience (1.5 minutes)

1. **Notice navbar change** - Now shows user name with dropdown
2. **Open Chatbot** - See personalized greeting based on your skill level:
   - Beginner: "Great to have you here! I'm here to guide you..."
   - Intermediate: "Welcome back! Let's dive into some interesting topics..."
   - Advanced: "Welcome! Ready to explore advanced concepts..."

3. **Ask a question** - e.g., "What is a neural network?"
4. **Notice personalized response**:
   - For beginners: Simple analogies, step-by-step explanations
   - For advanced: Technical terms, code examples, deep concepts

5. **Hover over name** in navbar - Shows dropdown with email and Sign Out

---

### Act 4: Session Recovery (30 seconds)

1. **Start signup again** (incognito or different email)
2. **Answer first 2-3 questions**
3. **Refresh the page** (F5)
4. **Notice**: Chatbot says "Welcome back! Let's continue where we left off"
5. **Your progress is preserved!**

**Key Feature**: No lost progress if user accidentally refreshes.

---

### Act 5: Sign Out / Sign In (30 seconds)

1. **Click user name dropdown** -> **Sign Out**
2. **Notice**: Redirected to home, navbar shows Sign In/Get Started
3. **Click "Sign In"**
4. **Enter credentials**: `demo@example.com` / `Demo1234`
5. **Instant access** - No need to redo onboarding!

---

## Technical Highlights for Judges

### Architecture
```
Frontend (React/Docusaurus)     Backend (FastAPI)
        |                              |
        v                              v
[AuthProvider Context] <----> [Better Auth Compatible]
        |                              |
        v                              v
[OnboardingChatbot] <-------> [Onboarding State Machine]
        |                              |
        v                              v
[Main Chatbot] <------------> [AI Agent Orchestrator]
                                       |
                                       v
                              [Personalization Service]
                              [TutorAgent, QuizAgent, etc.]
```

### Key Innovations

1. **Chatbot-Driven Signup**
   - State machine for question flow
   - Multi-select and single-select question types
   - Session persistence with 30-min expiry
   - Page refresh recovery via localStorage

2. **AI Personalization**
   - Dynamic system prompts based on user profile
   - Skill-level appropriate explanations
   - Hardware-aware project suggestions
   - Language-aware code examples

3. **Seamless UX**
   - Cookie-based authentication
   - Dropdown menu for authenticated users
   - Loading states and error handling
   - Responsive design

### API Endpoints

| Endpoint | Purpose |
|----------|---------|
| POST `/api/auth/onboarding/start` | Validate credentials, start session |
| GET `/api/auth/onboarding/question/{id}` | Get current question |
| POST `/api/auth/onboarding/answer` | Submit answer, get next |
| GET `/api/auth/onboarding/summary/{id}` | Get profile summary |
| POST `/api/auth/onboarding/complete` | Create account + profile |
| GET `/api/user/profile` | Get user profile for AI |
| GET `/api/chatbot/greeting` | Get personalized greeting |
| POST `/api/chatbot` | AI chat with personalization |

---

## Scoring Criteria Coverage

| Criteria | Implementation |
|----------|----------------|
| Innovation | Chatbot-driven signup (not forms!) |
| Technical Complexity | Multi-agent AI, state machine, personalization |
| User Experience | Conversational onboarding, session recovery |
| Completeness | Full auth cycle + AI personalization |
| Code Quality | TypeScript, Python typing, clean architecture |

---

## Fallback Demo (If Backend Issues)

If the backend isn't running:
1. Show the OnboardingChatbot.tsx code - explain the conversation flow
2. Show backend/config/onboarding_questions.py - explain question structure
3. Show backend/skill_agents/main_orchestrator.py - explain personalization logic
4. Walk through the spec.md and plan.md documents

---

## Questions Judges May Ask

**Q: Why chatbot instead of forms?**
A: Forms are boring. Conversation is engaging. Users feel like they're talking to a tutor from the start, and we ensure complete data collection.

**Q: How does personalization work?**
A: User profile is fetched via session cookie, passed to AI orchestrator, which generates dynamic system prompts based on skill level, experience, and goals.

**Q: What if user refreshes mid-signup?**
A: localStorage stores session ID, validates with backend on load, resumes from exact question.

**Q: Is this production-ready?**
A: Core functionality yes. Would add: rate limiting, email verification, password reset, and database persistence for sessions.

---

## Contact

Built for the AI-Native Textbook Platform Hackathon.

Core Innovation: **50 bonus points for chatbot-driven signup!**
