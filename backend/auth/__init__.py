"""Authentication module for Better Auth integration with chatbot onboarding."""

from .routes import auth_router, api_auth_router
from .middleware import get_current_user, require_auth
from .service import AuthService
from .onboarding import OnboardingService

__all__ = [
    "auth_router",
    "api_auth_router",
    "get_current_user",
    "require_auth",
    "AuthService",
    "OnboardingService"
]
