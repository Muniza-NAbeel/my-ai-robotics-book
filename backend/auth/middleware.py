"""Authentication middleware for session verification."""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any

from .service import AuthService

# Security scheme for bearer token
security = HTTPBearer(auto_error=False)


def get_session_token(request: Request) -> Optional[str]:
    """Extract session token from cookies or Authorization header."""
    # Check for session cookie
    token = request.cookies.get("session_token")
    if token:
        return token

    # Fallback to Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]

    return None


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """Get current authenticated user from session."""
    token = get_session_token(request)

    if not token:
        return None

    user = AuthService.validate_session(token)

    if user:
        return {
            "id": user.get("id"),
            "user_id": user.get("id"),  # For backward compatibility
            "email": user.get("email"),
            "name": user.get("name")
        }

    return None


async def require_auth(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Dependency that requires authentication."""
    user = await get_current_user(request, credentials)

    if not user:
        raise HTTPException(
            status_code=401,
            detail={"error": "unauthorized", "message": "Authentication required"}
        )

    return user
