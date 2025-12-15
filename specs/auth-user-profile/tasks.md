# Tasks: Authentication & User Profiling System (Chatbot Onboarding)

**Input**: Design documents from `/specs/auth-user-profile/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)
**Branch**: `003-auth-user-profile`
**Generated**: 2025-12-14

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)

## User Story Mapping

| Story | Priority | Title |
|-------|----------|-------|
| US1 | P1 | New User Signup with Chatbot Onboarding |
| US2 | P1 | Chatbot Conversation Flow |
| US3 | P2 | Existing User Signin |
| US4 | P3 | User Logout |
| US5 | P2 | AI Agent Profile Access for Personalization |

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Better Auth configuration

- [x] T001 Create backend directory structure per plan.md (backend/auth/, backend/models/, backend/services/, backend/routes/)
- [x] T002 [P] Install Better Auth dependencies and configure in backend/auth/better_auth.py
- [x] T003 [P] Create .env file with Better Auth secrets and database configuration
- [x] T004 [P] Configure CORS in backend/main.py for frontend communication
- [x] T005 Setup SQLite database and SQLAlchemy connection in backend/database.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create UserProfile SQLAlchemy model in backend/models/user_profile.py with fields: id, user_id, software_background (JSON), hardware_background (JSON), learning_goals (JSON), created_at, updated_at
- [x] T007 [P] Create OnboardingSession model in backend/models/onboarding_session.py with fields: session_id, current_question_index, collected_answers (JSON), expiry_timestamp
- [x] T008 [P] Create Pydantic schemas for request/response validation in backend/schemas/profile_schemas.py
- [x] T009 Implement session validation middleware in backend/auth/middleware.py
- [x] T010 Create database migration script to initialize tables in backend/migrations/init_db.py
- [x] T011 [P] Create base error handling utilities in backend/utils/errors.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 & 2 - Signup with Chatbot Onboarding (Priority: P1) MVP

**Goal**: User can signup with email/password, then chatbot collects background info conversationally

**Independent Test**: Complete signup flow end-to-end, verify account creation in database, confirm chatbot collected all profile data

### Backend Implementation (US1 + US2)

- [x] T012 [US1] Implement credential validation endpoint POST /auth/validate-credentials in backend/auth/routes.py (checks email format, password strength, duplicate email)
- [x] T013 [US1] Implement onboarding session creation endpoint POST /auth/onboarding/start in backend/auth/routes.py (creates temp session after credentials validated)
- [x] T014 [P] [US2] Implement onboarding question retrieval GET /auth/onboarding/question in backend/auth/routes.py (returns current question based on session state)
- [x] T015 [P] [US2] Implement onboarding answer submission POST /auth/onboarding/answer in backend/auth/routes.py (stores answer, advances to next question)
- [x] T016 [US2] Implement onboarding summary GET /auth/onboarding/summary in backend/auth/routes.py (returns all collected answers for confirmation)
- [x] T017 [US1] Implement final signup endpoint POST /auth/signup/complete in backend/auth/routes.py (creates Better Auth user + UserProfile atomically)
- [x] T018 [P] [US2] Create chatbot question flow configuration in backend/config/onboarding_questions.py (defines question sequence, options, validation rules)
- [x] T019 [US1] Implement ProfileService.create_profile() in backend/services/profile_service.py

### Frontend Implementation (US1 + US2)

- [x] T020 [P] [US1] Create AuthProvider context in my-ai-robotics-book/src/components/Auth/AuthProvider.tsx
- [x] T021 [P] [US1] Create useAuth hook in my-ai-robotics-book/src/hooks/useAuth.ts
- [x] T022 [US1] Create SignupForm component (email/password only) in my-ai-robotics-book/src/components/Auth/SignupForm.tsx
- [x] T023 [US1] Create signup page that shows SignupForm in my-ai-robotics-book/src/pages/signup.tsx
- [x] T024 [US2] Create OnboardingChatbot component in my-ai-robotics-book/src/components/Chatbot/OnboardingChatbot.tsx
- [x] T025 [US2] Implement chatbot greeting message and question rendering with selectable options
- [x] T026 [US2] Implement chatbot answer acknowledgment and transition to next question
- [x] T027 [US2] Implement chatbot summary display with confirm/edit capability
- [x] T028 [US1] Integrate OnboardingChatbot into signup page - activate after credentials validated
- [x] T029 [US1] Handle signup completion - create account and redirect to /docs/intro-foundations/intro

**Checkpoint**: Users can signup via chatbot onboarding - MVP complete!

---

## Phase 4: User Story 3 - Existing User Signin (Priority: P2)

**Goal**: Returning users can sign in quickly and access their personalized experience

**Independent Test**: Sign in with existing credentials, verify session created, verify redirect to content area

### Backend Implementation (US3)

- [x] T030 [US3] Implement signin endpoint POST /auth/signin in backend/auth/routes.py
- [x] T031 [US3] Implement session creation and cookie handling for signin
- [x] T032 [P] [US3] Implement GET /auth/session endpoint to check current session status

### Frontend Implementation (US3)

- [x] T033 [P] [US3] Create SigninForm component in my-ai-robotics-book/src/components/Auth/SigninForm.tsx
- [x] T034 [US3] Create signin page in my-ai-robotics-book/src/pages/signin.tsx
- [x] T035 [US3] Implement signin success redirect to /docs/intro-foundations/intro
- [x] T036 [US3] Implement already-signed-in redirect (if user visits /signin while logged in)
- [x] T037 [US3] Update AuthProvider to load user profile on signin success

**Checkpoint**: Signin flow complete - users can return to their personalized experience

---

## Phase 5: User Story 4 - User Logout (Priority: P3)

**Goal**: Signed-in users can securely end their session

**Independent Test**: Click logout, verify session cleared, verify redirect to home, verify protected routes redirect to signin

### Backend Implementation (US4)

- [x] T038 [US4] Implement logout endpoint POST /auth/logout in backend/auth/routes.py
- [x] T039 [US4] Clear session cookie and invalidate server-side session

### Frontend Implementation (US4)

- [x] T040 [P] [US4] Create LogoutButton component in my-ai-robotics-book/src/components/Auth/LogoutButton.tsx
- [x] T041 [US4] Add LogoutButton to navbar for authenticated users in my-ai-robotics-book/src/theme/Navbar/
- [x] T042 [US4] Implement logout redirect to home page
- [x] T043 [US4] Update AuthProvider to clear auth state on logout

**Checkpoint**: Complete auth cycle (signup → signin → logout) working

---

## Phase 6: User Story 5 - AI Agent Profile Access for Personalization (Priority: P2)

**Goal**: AI Agents can retrieve user profile to personalize responses based on user background

**Independent Test**: Call profile API with valid auth, verify profile data returned; Call chatbot as authenticated user, verify response is personalized

### Backend Implementation (US5)

- [x] T044 [US5] Implement GET /user/profile endpoint in backend/routes/profile_routes.py (returns full profile)
- [x] T045 [P] [US5] Implement GET /user/profile/skills endpoint (returns programming/AI/web dev levels)
- [x] T046 [P] [US5] Implement GET /user/profile/hardware endpoint (returns hardware capabilities)
- [x] T047 [US5] Create PersonalizationService in backend/services/personalization.py with methods: get_skill_tier(), get_explanation_depth(), should_use_advanced_examples()
- [x] T048 [US5] Implement guest user detection and default profile fallback

### Frontend/Chatbot Integration (US5)

- [x] T049 [US5] Update existing chatbot to fetch user profile on initialization in my-ai-robotics-book/src/components/Chatbot/index.tsx
- [x] T050 [US5] Pass user profile context to AI agent requests
- [x] T051 [US5] Implement personalized greeting based on user's name and background
- [x] T052 [US5] Add "Sign up for personalized experience" prompt for guest users

**Checkpoint**: Full personalization loop complete - chatbot adapts to user background

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T053 [P] Add Login/Signup buttons to navbar for guest users in my-ai-robotics-book/src/theme/NavbarItem/
- [x] T054 [P] Create user dropdown menu showing email + logout for authenticated users
- [x] T055 Implement graceful error handling for network failures during onboarding
- [x] T056 [P] Add loading states and spinners for all async operations
- [x] T057 Implement onboarding session recovery on page refresh (FR-015)
- [x] T058 [P] Add input validation error messages with user-friendly text
- [x] T059 Security review: ensure passwords are never logged, sessions expire properly
- [x] T060 [P] Add console logging for debugging (remove before production)
- [x] T061 Create demo flow documentation for hackathon judges

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phase 3 (US1+US2)**: Depends on Phase 2 - MVP target
- **Phase 4 (US3)**: Depends on Phase 2, can run parallel with Phase 3 after foundational
- **Phase 5 (US4)**: Depends on Phase 3 or 4 (needs signin to test logout)
- **Phase 6 (US5)**: Depends on Phase 2, can run parallel after foundational
- **Phase 7 (Polish)**: After all desired user stories complete

### User Story Dependencies

```
Setup (Phase 1)
    ↓
Foundational (Phase 2)
    ↓
    ├─→ US1+US2 Signup + Chatbot (Phase 3) ─→ MVP!
    │       ↓
    │   US4 Logout (Phase 5)
    │
    ├─→ US3 Signin (Phase 4) ─────────────────→ Can test after US1 creates users
    │
    └─→ US5 AI Personalization (Phase 6) ────→ Can develop parallel, test after US1
            ↓
        Polish (Phase 7)
```

### Parallel Opportunities

**Within Phase 1:**
- T002, T003, T004 can run in parallel

**Within Phase 2:**
- T007, T008, T011 can run in parallel after T006

**Within Phase 3:**
- T014, T015, T018 (backend) can run in parallel
- T020, T021 (frontend) can run in parallel

**Within Phase 4:**
- T032, T033 can run in parallel

**Within Phase 6:**
- T045, T046 can run in parallel

---

## Parallel Example: Phase 3 (MVP)

```bash
# After T013 completes, launch backend API tasks in parallel:
Task: T014 "Implement onboarding question retrieval GET /auth/onboarding/question"
Task: T015 "Implement onboarding answer submission POST /auth/onboarding/answer"
Task: T018 "Create chatbot question flow configuration"

# After T019 completes, launch frontend tasks in parallel:
Task: T020 "Create AuthProvider context"
Task: T021 "Create useAuth hook"
```

---

## Implementation Strategy

### MVP First (Phases 1-3 Only) - RECOMMENDED FOR HACKATHON

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011)
3. Complete Phase 3: US1+US2 Signup with Chatbot (T012-T029)
4. **STOP and DEMO**: Chatbot-driven signup is the core innovation!

### Incremental Delivery (Full Implementation)

1. Setup + Foundational → Foundation ready
2. Add US1+US2 → Test signup with chatbot → Demo (MVP!)
3. Add US3 → Test signin → Demo
4. Add US4 → Test logout → Demo
5. Add US5 → Test personalization → Demo
6. Polish → Production ready

### Hackathon Demo Flow

1. Show guest user visiting the site
2. Click "Get Started" → Signup page
3. Enter credentials → Chatbot activates
4. Complete chatbot conversation (the WOW moment!)
5. Account created → Redirected to content
6. Chatbot now knows user's background
7. Ask chatbot a question → Personalized response!

---

## Task Summary

| Phase | Tasks | Parallel Tasks |
|-------|-------|----------------|
| Phase 1: Setup | 5 | 3 |
| Phase 2: Foundational | 6 | 3 |
| Phase 3: US1+US2 (MVP) | 18 | 6 |
| Phase 4: US3 Signin | 8 | 2 |
| Phase 5: US4 Logout | 6 | 1 |
| Phase 6: US5 Personalization | 9 | 2 |
| Phase 7: Polish | 9 | 5 |
| **Total** | **61** | **22** |

### MVP Scope (Recommended)

- **Tasks**: T001-T029 (29 tasks)
- **Core Innovation**: Chatbot-driven signup with profile collection
- **Demo-Ready**: Full signup experience with conversational onboarding

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- US1 and US2 are combined in Phase 3 because chatbot onboarding is integral to signup
- Commit after each task or logical group
- Stop at any checkpoint to validate and demo
- Hackathon judges will be impressed by the chatbot onboarding flow!
