# Implementation Plan: Authentication & User Profiling System

**Feature Branch**: `003-auth-user-profile`
**Created**: 2025-12-13
**Status**: Ready for Implementation

## Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Authentication**: Better Auth (https://www.better-auth.com/)
- **Database**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy with Pydantic models

### Frontend
- **Framework**: Docusaurus (React-based)
- **State Management**: React Context for auth state
- **HTTP Client**: Fetch API

### Infrastructure
- **Session Handling**: Cookie-based sessions via Better Auth
- **Environment**: dotenv for configuration

## Project Structure

### Backend Structure
```
backend/
├── auth/
│   ├── __init__.py
│   ├── better_auth.py        # Better Auth configuration
│   ├── routes.py             # Auth endpoints (signup, signin, logout)
│   └── middleware.py         # Session validation middleware
├── models/
│   ├── __init__.py
│   └── user_profile.py       # UserProfile SQLAlchemy model
├── services/
│   ├── __init__.py
│   ├── profile_service.py    # Profile CRUD operations
│   └── personalization.py    # AI Agent interfaces
├── routes/
│   ├── __init__.py
│   └── profile_routes.py     # Profile API endpoints
└── main.py                   # FastAPI app with routers
```

### Frontend Structure
```
my-ai-robotics-book/
├── src/
│   ├── components/
│   │   └── Auth/
│   │       ├── SignupForm.tsx
│   │       ├── SigninForm.tsx
│   │       ├── LogoutButton.tsx
│   │       ├── AuthProvider.tsx
│   │       └── Questionnaire.tsx
│   ├── pages/
│   │   ├── signup.tsx
│   │   └── signin.tsx
│   └── hooks/
│       └── useAuth.ts
```

## Architecture Decisions

### AD-001: Better Auth Integration
- Use Better Auth's email/password authentication
- Session tokens stored in HTTP-only cookies
- Backend validates sessions via Better Auth SDK

### AD-002: Profile Data Storage
- UserProfile stored in separate table linked to Better Auth user_id
- Software and hardware backgrounds stored as JSON columns
- Enables flexible schema evolution without migrations

### AD-003: Questionnaire as Part of Signup
- Single-page signup with credentials + questionnaire
- Atomic transaction: user + profile created together or not at all
- No partial user accounts

### AD-004: Personalization Interfaces
- Clean service layer abstracts profile data for AI Agents
- Returns normalized, typed responses
- Decouples AI logic from storage implementation

## API Contracts

### POST /auth/signup
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "software_background": {
    "programming_level": "intermediate",
    "languages_known": ["python", "javascript"],
    "ai_experience": "basic",
    "web_dev_experience": "intermediate"
  },
  "hardware_background": {
    "robotics_experience": false,
    "electronics_familiarity": "basic",
    "hardware_access": ["laptop_only", "raspberry_pi"]
  }
}

Response (201):
{
  "user_id": "uuid",
  "email": "user@example.com",
  "message": "Account created successfully"
}

Error (400):
{
  "error": "validation_error",
  "details": ["Password must be at least 8 characters"]
}
```

### POST /auth/signin
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response (200):
{
  "user_id": "uuid",
  "email": "user@example.com"
}
// Session cookie set automatically

Error (401):
{
  "error": "invalid_credentials",
  "message": "Invalid email or password"
}
```

### POST /auth/logout
```json
Response (200):
{
  "message": "Logged out successfully"
}
// Session cookie cleared
```

### GET /user/profile
```json
Response (200):
{
  "user_id": "uuid",
  "software_background": {
    "programming_level": "intermediate",
    "languages_known": ["python", "javascript"],
    "ai_experience": "basic",
    "web_dev_experience": "intermediate"
  },
  "hardware_background": {
    "robotics_experience": false,
    "electronics_familiarity": "basic",
    "hardware_access": ["laptop_only", "raspberry_pi"]
  },
  "created_at": "2025-12-13T10:00:00Z"
}

Error (401):
{
  "error": "unauthorized",
  "message": "Authentication required"
}
```

### GET /user/profile/skills
```json
Response (200):
{
  "programming_level": "intermediate",
  "ai_experience": "basic",
  "web_dev_experience": "intermediate",
  "overall_skill_tier": "intermediate"
}
```

### GET /user/profile/hardware
```json
Response (200):
{
  "robotics_experience": false,
  "electronics_familiarity": "basic",
  "hardware_access": ["laptop_only", "raspberry_pi"],
  "can_do_hardware_projects": true
}
```

## Data Model

### UserProfile Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY |
| user_id | VARCHAR | UNIQUE, NOT NULL, FK to Better Auth |
| software_background | JSON | NOT NULL |
| hardware_background | JSON | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() |

### Software Background Schema
```json
{
  "programming_level": "beginner" | "intermediate" | "advanced",
  "languages_known": ["python", "javascript", "typescript", "c_cpp", "none"],
  "ai_experience": "none" | "basic" | "intermediate" | "advanced",
  "web_dev_experience": "none" | "basic" | "intermediate" | "advanced"
}
```

### Hardware Background Schema
```json
{
  "robotics_experience": boolean,
  "electronics_familiarity": "none" | "basic" | "intermediate",
  "hardware_access": ["laptop_only", "raspberry_pi", "arduino", "robotics_kits", "none"]
}
```

## Implementation Phases

### Phase 1: Setup
- Configure Better Auth in FastAPI
- Set up environment variables
- Create database migration for UserProfile

### Phase 2: Foundational
- Implement auth middleware
- Create base models and schemas

### Phase 3: User Story 1 - Signup (P1)
- Implement signup endpoint with questionnaire
- Create signup UI in Docusaurus
- Validate and store profile data

### Phase 4: User Story 2 - Signin (P2)
- Implement signin endpoint
- Create signin UI
- Handle session management

### Phase 5: User Story 3 - Logout (P3)
- Implement logout endpoint
- Add logout button to UI
- Clear session properly

### Phase 6: User Story 4 - AI Agent Access (P4)
- Implement profile retrieval endpoints
- Create personalization service interfaces
- Document API for AI Agents

### Phase 7: Polish
- Security review
- Error handling improvements
- Production readiness check

## Dependencies

- User Story 2 (Signin) depends on User Story 1 (Signup) for test data
- User Story 3 (Logout) depends on User Story 2 (Signin) for session to clear
- User Story 4 (AI Access) depends on User Story 1 (Signup) for profile data

## MVP Scope

**Minimum Viable Product**: User Story 1 (Signup with Profile)
- Users can create accounts with background questionnaire
- Profile data is persisted
- Foundation for all subsequent stories
