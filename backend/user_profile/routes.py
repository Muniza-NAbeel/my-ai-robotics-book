"""Profile routes for retrieving user profile data."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from .schemas import UserProfileResponse, SkillsResponse, HardwareResponse, ProfileNotFoundError
from .service import ProfileService
from auth.middleware import require_auth
from auth.schemas import SoftwareBackground, HardwareBackground


profile_router = APIRouter(prefix="/user", tags=["User Profile"])


@profile_router.get(
    "/profile",
    response_model=UserProfileResponse,
    responses={
        401: {"description": "Authentication required"},
        404: {"model": ProfileNotFoundError, "description": "Profile not found"}
    }
)
async def get_profile(current_user: dict = Depends(require_auth)):
    """Get complete user profile.

    Requires authentication.

    Args:
        current_user: Current authenticated user from middleware

    Returns:
        Complete user profile with software and hardware backgrounds
    """
    profile = ProfileService.get_profile(current_user['user_id'])

    if not profile:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": "User profile not found"
            }
        )

    return UserProfileResponse(
        user_id=profile['user_id'],
        software_background=SoftwareBackground(**profile['software_background']),
        hardware_background=HardwareBackground(**profile['hardware_background']),
        created_at=profile['created_at']
    )


@profile_router.get(
    "/profile/skills",
    response_model=SkillsResponse,
    responses={
        401: {"description": "Authentication required"},
        404: {"model": ProfileNotFoundError, "description": "Profile not found"}
    }
)
async def get_skills(current_user: dict = Depends(require_auth)):
    """Get user skills summary for AI personalization.

    Returns computed skill tier based on programming, AI, and web dev experience.

    Args:
        current_user: Current authenticated user from middleware

    Returns:
        Skills summary with overall skill tier
    """
    skills = ProfileService.get_skills(current_user['user_id'])

    if not skills:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": "User profile not found"
            }
        )

    return SkillsResponse(**skills)


@profile_router.get(
    "/profile/hardware",
    response_model=HardwareResponse,
    responses={
        401: {"description": "Authentication required"},
        404: {"model": ProfileNotFoundError, "description": "Profile not found"}
    }
)
async def get_hardware(current_user: dict = Depends(require_auth)):
    """Get user hardware capabilities for AI personalization.

    Returns hardware access and computed capability to do hardware projects.

    Args:
        current_user: Current authenticated user from middleware

    Returns:
        Hardware capabilities with project feasibility indicator
    """
    hardware = ProfileService.get_hardware_capabilities(current_user['user_id'])

    if not hardware:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": "User profile not found"
            }
        )

    return HardwareResponse(**hardware)
