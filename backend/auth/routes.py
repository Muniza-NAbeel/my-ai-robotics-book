"""Authentication routes for signup, signin, logout, and chatbot onboarding."""

from fastapi import APIRouter, Response, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, field_validator
import re

from .schemas import (
    SignupRequest, SigninRequest, AuthResponse,
    ErrorResponse, LogoutResponse
)
from .service import AuthService
from .middleware import get_current_user, get_session_token
from .onboarding import OnboardingService
from user_profile.service import ProfileService


# Router for legacy endpoints (/auth/*)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# Router for Better Auth compatible endpoints (/api/auth/*)
api_auth_router = APIRouter(prefix="/api/auth", tags=["Authentication API"])


# ==================== Better Auth Compatible Schemas ====================

class BetterAuthSignupRequest(BaseModel):
    """Better Auth compatible signup request."""
    email: EmailStr
    password: str
    name: Optional[str] = None


class BetterAuthSigninRequest(BaseModel):
    """Better Auth compatible signin request."""
    email: EmailStr
    password: str


class BetterAuthUserResponse(BaseModel):
    """Better Auth compatible user response."""
    id: str
    email: str
    name: Optional[str] = None
    emailVerified: bool = False
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None


class BetterAuthSessionResponse(BaseModel):
    """Better Auth compatible session response."""
    user: BetterAuthUserResponse
    session: dict


# ==================== Better Auth Compatible Endpoints ====================

@api_auth_router.post("/sign-up/email")
async def better_auth_signup(request: BetterAuthSignupRequest, response: Response):
    """Better Auth compatible signup endpoint."""
    # Check if email exists
    if AuthService.email_exists(request.email):
        return JSONResponse(
            status_code=400,
            content={"error": {"message": "User already exists"}}
        )

    # Create user
    user = AuthService.create_user(request.email, request.password, request.name)
    if not user:
        return JSONResponse(
            status_code=400,
            content={"error": {"message": "Failed to create account"}}
        )

    # Create session
    session_token = AuthService.create_session(user['id'])

    # Set session cookie (Better Auth format)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400
    )

    return {
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user.get('name', user['email'].split('@')[0]),
            "emailVerified": False,
            "createdAt": user.get('createdAt'),
            "updatedAt": user.get('createdAt')
        },
        "session": {
            "token": session_token,
            "expiresAt": None
        }
    }


@api_auth_router.post("/sign-in/email")
async def better_auth_signin(request: BetterAuthSigninRequest, response: Response):
    """Better Auth compatible signin endpoint."""
    user = AuthService.authenticate(request.email, request.password)

    if not user:
        return JSONResponse(
            status_code=401,
            content={"error": {"message": "Invalid email or password"}}
        )

    # Create session
    session_token = AuthService.create_session(user['id'])

    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400
    )

    return {
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user.get('name', user['email'].split('@')[0]),
            "emailVerified": False
        },
        "session": {
            "token": session_token,
            "expiresAt": None
        }
    }


@api_auth_router.post("/sign-out")
async def better_auth_signout(request: Request, response: Response):
    """Better Auth compatible signout endpoint."""
    token = get_session_token(request)

    if token:
        AuthService.invalidate_session(token)

    response.delete_cookie(key="session_token", httponly=True, secure=False, samesite="lax")

    return {"success": True}


@api_auth_router.get("/get-session")
async def better_auth_get_session(request: Request):
    """Better Auth compatible get session endpoint."""
    token = get_session_token(request)

    if not token:
        return JSONResponse(
            status_code=200,
            content={"session": None, "user": None}
        )

    user = AuthService.validate_session(token)

    if not user:
        return JSONResponse(
            status_code=200,
            content={"session": None, "user": None}
        )

    return {
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user.get('name', user['email'].split('@')[0]),
            "emailVerified": False
        },
        "session": {
            "token": token,
            "expiresAt": None
        }
    }


# ==================== Legacy Endpoints ====================

@auth_router.post(
    "/signup",
    response_model=AuthResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "Email already registered"}
    }
)
async def signup(request: SignupRequest, response: Response):
    """Register a new user with profile questionnaire."""
    if AuthService.email_exists(request.email):
        raise HTTPException(
            status_code=409,
            detail={"error": "email_exists", "message": "This email is already registered"}
        )

    user = AuthService.create_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=409,
            detail={"error": "registration_failed", "message": "Failed to create account"}
        )

    profile = ProfileService.create_profile(
        user_id=user['id'],
        software_background=request.software_background.model_dump(),
        hardware_background=request.hardware_background.model_dump()
    )

    if not profile:
        raise HTTPException(
            status_code=500,
            detail={"error": "profile_creation_failed", "message": "Failed to save profile data"}
        )

    session_token = AuthService.create_session(user['id'])

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400
    )

    return AuthResponse(user_id=user['id'], email=user['email'], message="Account created successfully")


@auth_router.post(
    "/signin",
    response_model=AuthResponse,
    responses={401: {"model": ErrorResponse, "description": "Invalid credentials"}}
)
async def signin(request: SigninRequest, response: Response):
    """Sign in an existing user."""
    user = AuthService.authenticate(request.email, request.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": "invalid_credentials", "message": "Invalid email or password"}
        )

    session_token = AuthService.create_session(user['id'])

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400
    )

    return AuthResponse(user_id=user['id'], email=user['email'])


@auth_router.post("/logout", response_model=LogoutResponse)
async def logout(request: Request, response: Response):
    """Log out the current user."""
    token = get_session_token(request)

    if token:
        AuthService.invalidate_session(token)

    response.delete_cookie(key="session_token", httponly=True, secure=False, samesite="lax")

    return LogoutResponse(message="Logged out successfully")


@auth_router.get("/me", response_model=AuthResponse)
async def get_current_user_info(current_user: Optional[dict] = Depends(get_current_user)):
    """Get current authenticated user info."""
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail={"error": "unauthorized", "message": "Not authenticated"}
        )

    return AuthResponse(user_id=current_user['id'], email=current_user['email'])


# ==================== Chatbot Onboarding Endpoints ====================

class OnboardingStartRequest(BaseModel):
    """Request to start chatbot onboarding after credential validation."""
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets minimum requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v


class OnboardingAnswerRequest(BaseModel):
    """Request to submit an answer during onboarding."""
    session_id: str
    answer: Any  # Can be string or list depending on question type


class OnboardingCompleteRequest(BaseModel):
    """Request to complete signup after onboarding."""
    session_id: str


@api_auth_router.post("/onboarding/start")
async def start_onboarding(request: OnboardingStartRequest):
    """Start chatbot onboarding after validating credentials.

    This endpoint validates email/password then creates a temporary
    onboarding session. The chatbot will guide the user through
    background questions before account creation.

    Returns:
        session_id: Use this for subsequent onboarding API calls
        first_question: The welcome/first question to display
    """
    # Check if email already exists
    if AuthService.email_exists(request.email):
        return JSONResponse(
            status_code=400,
            content={
                "error": "email_exists",
                "message": "This email is already registered. Please sign in instead."
            }
        )

    # Create onboarding session with validated credentials
    session = OnboardingService.create_session(request.email, request.password)

    # Get the first question (welcome message)
    first_question = OnboardingService.get_current_question(session.session_id)

    return {
        "session_id": session.session_id,
        "current_question": first_question,
        "message": "Onboarding started. Answer questions to complete signup."
    }


@api_auth_router.get("/onboarding/question/{session_id}")
async def get_onboarding_question(session_id: str):
    """Get the current question for an onboarding session.

    Returns the current question with options for the chatbot to display.
    """
    question = OnboardingService.get_current_question(session_id)

    if not question:
        return JSONResponse(
            status_code=404,
            content={
                "error": "session_not_found",
                "message": "Onboarding session not found or expired. Please start over."
            }
        )

    return {"current_question": question}


@api_auth_router.post("/onboarding/answer")
async def submit_onboarding_answer(request: OnboardingAnswerRequest):
    """Submit an answer for the current onboarding question.

    The chatbot sends user's selection here. Returns the next question
    or signals completion when all questions are answered.
    """
    result = OnboardingService.submit_answer(request.session_id, request.answer)

    if not result:
        return JSONResponse(
            status_code=404,
            content={
                "error": "session_not_found",
                "message": "Onboarding session not found or expired. Please start over."
            }
        )

    return result


@api_auth_router.get("/onboarding/summary/{session_id}")
async def get_onboarding_summary(session_id: str):
    """Get summary of all collected answers for confirmation.

    Called before final account creation so user can review their answers.
    """
    summary = OnboardingService.get_summary(session_id)

    if not summary:
        return JSONResponse(
            status_code=404,
            content={
                "error": "session_not_found",
                "message": "Onboarding session not found or expired. Please start over."
            }
        )

    return summary


@api_auth_router.post("/onboarding/complete")
async def complete_onboarding(request: OnboardingCompleteRequest, response: Response):
    """Complete signup after chatbot onboarding.

    Creates the user account and profile atomically using the
    credentials and answers collected during onboarding.

    Returns:
        user: The created user data
        session: Active session token for immediate login
    """
    # Get credentials and profile data from onboarding session
    data = OnboardingService.get_credentials_and_profile(request.session_id)

    if not data:
        return JSONResponse(
            status_code=404,
            content={
                "error": "session_not_found",
                "message": "Onboarding session not found or expired. Please start over."
            }
        )

    # Double-check email isn't taken (race condition protection)
    if AuthService.email_exists(data['email']):
        OnboardingService.delete_session(request.session_id)
        return JSONResponse(
            status_code=400,
            content={
                "error": "email_exists",
                "message": "This email is already registered."
            }
        )

    # Create user account
    user = AuthService.create_user(
        data['email'],
        data['password'],
        data['email'].split('@')[0]  # Use email prefix as name
    )

    if not user:
        return JSONResponse(
            status_code=500,
            content={
                "error": "user_creation_failed",
                "message": "Failed to create account. Please try again."
            }
        )

    # Create user profile with collected background data
    profile = ProfileService.create_profile(
        user_id=user['id'],
        software_background=data.get('software_background', {}),
        hardware_background=data.get('hardware_background', {})
    )

    if not profile:
        # Log but don't fail - user was created
        print(f"Warning: Failed to create profile for user {user['id']}")

    # Create auth session
    session_token = AuthService.create_session(user['id'])

    # Set session cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=86400
    )

    # Clean up onboarding session
    OnboardingService.delete_session(request.session_id)

    return {
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user.get('name', user['email'].split('@')[0]),
            "emailVerified": False,
            "createdAt": user.get('createdAt')
        },
        "session": {
            "token": session_token,
            "expiresAt": None
        },
        "profile": {
            "software_background": data.get('software_background', {}),
            "hardware_background": data.get('hardware_background', {})
        },
        "message": "Account created successfully! Welcome aboard."
    }
