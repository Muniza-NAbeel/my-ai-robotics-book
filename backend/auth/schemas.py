"""Pydantic schemas for authentication requests and responses."""

from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from enum import Enum
import re


class ProgrammingLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ExperienceLevel(str, Enum):
    NONE = "none"
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ElectronicsFamiliarity(str, Enum):
    NONE = "none"
    BASIC = "basic"
    INTERMEDIATE = "intermediate"


class ProgrammingLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    C_CPP = "c_cpp"
    NONE = "none"


class HardwareAccess(str, Enum):
    LAPTOP_ONLY = "laptop_only"
    RASPBERRY_PI = "raspberry_pi"
    ARDUINO = "arduino"
    ROBOTICS_KITS = "robotics_kits"
    NONE = "none"


class SoftwareBackground(BaseModel):
    """Software background questionnaire data."""
    programming_level: ProgrammingLevel
    languages_known: List[ProgrammingLanguage]
    ai_experience: ExperienceLevel
    web_dev_experience: ExperienceLevel

    @field_validator('languages_known')
    @classmethod
    def validate_languages(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one programming language must be selected')
        return v


class HardwareBackground(BaseModel):
    """Hardware/robotics background questionnaire data."""
    robotics_experience: bool
    electronics_familiarity: ElectronicsFamiliarity
    hardware_access: List[HardwareAccess]

    @field_validator('hardware_access')
    @classmethod
    def validate_hardware(cls, v):
        if not v or len(v) == 0:
            raise ValueError('At least one hardware access option must be selected')
        return v


class SignupRequest(BaseModel):
    """Request schema for user signup."""
    email: EmailStr
    password: str
    software_background: SoftwareBackground
    hardware_background: HardwareBackground

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v


class SigninRequest(BaseModel):
    """Request schema for user signin."""
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    """Response schema for successful authentication."""
    user_id: str
    email: str
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Response schema for errors."""
    error: str
    message: str
    details: Optional[List[str]] = None


class LogoutResponse(BaseModel):
    """Response schema for logout."""
    message: str
