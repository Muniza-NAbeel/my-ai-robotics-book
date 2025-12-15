"""Pydantic schemas for user profile requests and responses."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from auth.schemas import (
    SoftwareBackground, HardwareBackground,
    ProgrammingLevel, ExperienceLevel, ElectronicsFamiliarity,
    ProgrammingLanguage, HardwareAccess
)


class UserProfileResponse(BaseModel):
    """Complete user profile response."""
    user_id: str
    software_background: SoftwareBackground
    hardware_background: HardwareBackground
    created_at: str


class SkillsResponse(BaseModel):
    """User skills summary for AI personalization."""
    programming_level: ProgrammingLevel
    ai_experience: ExperienceLevel
    web_dev_experience: ExperienceLevel
    overall_skill_tier: str  # Computed: beginner, intermediate, advanced


class HardwareResponse(BaseModel):
    """User hardware capabilities for AI personalization."""
    robotics_experience: bool
    electronics_familiarity: ElectronicsFamiliarity
    hardware_access: List[HardwareAccess]
    can_do_hardware_projects: bool  # Computed based on hardware_access


class ProfileNotFoundError(BaseModel):
    """Error response when profile is not found."""
    error: str = "not_found"
    message: str = "User profile not found"
