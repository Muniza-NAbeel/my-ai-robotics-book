"""Profile service for managing user profile data."""

from datetime import datetime
from typing import Optional, Dict, Any, List


class ProfileService:
    """Service for handling user profile operations.

    Manages storage and retrieval of user background questionnaire data.
    """

    # In-memory storage for development (replace with database in production)
    _profiles: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def create_profile(
        cls,
        user_id: str,
        software_background: Dict[str, Any],
        hardware_background: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create a new user profile.

        Args:
            user_id: User's ID from authentication
            software_background: Software background questionnaire data
            hardware_background: Hardware background questionnaire data

        Returns:
            Profile data dict if successful, None if profile already exists
        """
        if user_id in cls._profiles:
            return None

        profile_data = {
            'user_id': user_id,
            'software_background': software_background,
            'hardware_background': hardware_background,
            'created_at': datetime.utcnow().isoformat()
        }

        cls._profiles[user_id] = profile_data
        return profile_data

    @classmethod
    def get_profile(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by user ID.

        Args:
            user_id: User's ID

        Returns:
            Profile data dict if found, None otherwise
        """
        return cls._profiles.get(user_id)

    @classmethod
    def get_skills(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user skills summary for AI personalization.

        Args:
            user_id: User's ID

        Returns:
            Skills summary dict if profile found, None otherwise
        """
        profile = cls._profiles.get(user_id)
        if not profile:
            return None

        software = profile['software_background']

        # Compute overall skill tier based on multiple factors
        skill_levels = {
            'beginner': 0,
            'basic': 1,
            'none': 0,
            'intermediate': 2,
            'advanced': 3
        }

        prog_score = skill_levels.get(software.get('programming_level', 'beginner'), 0)
        ai_score = skill_levels.get(software.get('ai_experience', 'none'), 0)
        web_score = skill_levels.get(software.get('web_dev_experience', 'none'), 0)

        avg_score = (prog_score + ai_score + web_score) / 3

        if avg_score < 1:
            overall_tier = 'beginner'
        elif avg_score < 2:
            overall_tier = 'intermediate'
        else:
            overall_tier = 'advanced'

        return {
            'programming_level': software.get('programming_level'),
            'ai_experience': software.get('ai_experience'),
            'web_dev_experience': software.get('web_dev_experience'),
            'overall_skill_tier': overall_tier
        }

    @classmethod
    def get_hardware_capabilities(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user hardware capabilities for AI personalization.

        Args:
            user_id: User's ID

        Returns:
            Hardware capabilities dict if profile found, None otherwise
        """
        profile = cls._profiles.get(user_id)
        if not profile:
            return None

        hardware = profile['hardware_background']
        hardware_access = hardware.get('hardware_access', [])

        # Determine if user can do hardware projects
        hardware_capable_items = ['raspberry_pi', 'arduino', 'robotics_kits']
        can_do_hardware = any(
            item in hardware_access for item in hardware_capable_items
        )

        return {
            'robotics_experience': hardware.get('robotics_experience', False),
            'electronics_familiarity': hardware.get('electronics_familiarity', 'none'),
            'hardware_access': hardware_access,
            'can_do_hardware_projects': can_do_hardware
        }

    @classmethod
    def profile_exists(cls, user_id: str) -> bool:
        """Check if profile exists for user.

        Args:
            user_id: User's ID

        Returns:
            True if profile exists, False otherwise
        """
        return user_id in cls._profiles

    @classmethod
    def delete_profile(cls, user_id: str) -> bool:
        """Delete user profile.

        Args:
            user_id: User's ID

        Returns:
            True if profile was deleted, False if not found
        """
        if user_id in cls._profiles:
            del cls._profiles[user_id]
            return True
        return False
