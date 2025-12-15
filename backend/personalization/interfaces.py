"""Personalization interfaces for AI Agent integration.

This module defines clean abstractions that allow AI Agents to:
- Fetch user background data
- Determine skill levels and hardware capabilities
- Enable future personalization of content

NOTE: This module only defines interfaces/contracts.
Actual personalization logic should be implemented in AI Agents.
"""

from typing import Optional, Dict, Any, List, Protocol
from dataclasses import dataclass
from enum import Enum
from user_profile.service import ProfileService


class SkillTier(str, Enum):
    """User skill tier classification."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class ContentComplexity(str, Enum):
    """Content complexity levels for personalization."""
    BASIC = "basic"
    STANDARD = "standard"
    TECHNICAL = "technical"


@dataclass
class UserContext:
    """User context for AI Agent personalization.

    This dataclass provides a structured way to pass user information
    to AI Agents for content personalization.

    Attributes:
        user_id: Unique user identifier
        skill_tier: Overall skill classification
        programming_level: Programming proficiency level
        languages_known: List of known programming languages
        ai_experience: Level of AI/ML experience
        web_dev_experience: Level of web development experience
        has_robotics_background: Whether user has robotics experience
        electronics_familiarity: Level of electronics knowledge
        available_hardware: List of hardware user has access to
        can_do_hardware_projects: Whether user can perform hardware projects
    """
    user_id: str
    skill_tier: SkillTier
    programming_level: str
    languages_known: List[str]
    ai_experience: str
    web_dev_experience: str
    has_robotics_background: bool
    electronics_familiarity: str
    available_hardware: List[str]
    can_do_hardware_projects: bool


class PersonalizationInterface:
    """Interface for AI Agent personalization.

    This class provides methods for AI Agents to fetch user context
    and determine appropriate content personalization strategies.

    Usage by AI Agents:
        ```python
        from personalization import PersonalizationInterface

        # Get user context for personalization
        context = PersonalizationInterface.get_user_context(user_id)

        if context:
            if context.skill_tier == SkillTier.BEGINNER:
                # Use simpler explanations
                pass
            elif context.can_do_hardware_projects:
                # Include hardware project suggestions
                pass
        ```
    """

    @staticmethod
    def get_user_context(user_id: str) -> Optional[UserContext]:
        """Get complete user context for AI personalization.

        Args:
            user_id: User's unique identifier

        Returns:
            UserContext dataclass if user found, None otherwise
        """
        profile = ProfileService.get_profile(user_id)
        if not profile:
            return None

        skills = ProfileService.get_skills(user_id)
        hardware = ProfileService.get_hardware_capabilities(user_id)

        if not skills or not hardware:
            return None

        software = profile['software_background']

        return UserContext(
            user_id=user_id,
            skill_tier=SkillTier(skills['overall_skill_tier']),
            programming_level=software.get('programming_level', 'beginner'),
            languages_known=software.get('languages_known', []),
            ai_experience=software.get('ai_experience', 'none'),
            web_dev_experience=software.get('web_dev_experience', 'none'),
            has_robotics_background=hardware['robotics_experience'],
            electronics_familiarity=hardware['electronics_familiarity'],
            available_hardware=hardware['hardware_access'],
            can_do_hardware_projects=hardware['can_do_hardware_projects']
        )

    @staticmethod
    def get_skill_tier(user_id: str) -> Optional[SkillTier]:
        """Get user's overall skill tier.

        Args:
            user_id: User's unique identifier

        Returns:
            SkillTier enum value if user found, None otherwise
        """
        skills = ProfileService.get_skills(user_id)
        if not skills:
            return None

        return SkillTier(skills['overall_skill_tier'])

    @staticmethod
    def get_recommended_complexity(user_id: str) -> Optional[ContentComplexity]:
        """Get recommended content complexity for user.

        Maps skill tier to appropriate content complexity level.

        Args:
            user_id: User's unique identifier

        Returns:
            ContentComplexity enum value if user found, None otherwise
        """
        skill_tier = PersonalizationInterface.get_skill_tier(user_id)
        if not skill_tier:
            return None

        complexity_map = {
            SkillTier.BEGINNER: ContentComplexity.BASIC,
            SkillTier.INTERMEDIATE: ContentComplexity.STANDARD,
            SkillTier.ADVANCED: ContentComplexity.TECHNICAL
        }

        return complexity_map.get(skill_tier, ContentComplexity.STANDARD)

    @staticmethod
    def can_understand_code(user_id: str, language: str) -> bool:
        """Check if user can understand code in a specific language.

        Args:
            user_id: User's unique identifier
            language: Programming language to check

        Returns:
            True if user knows the language, False otherwise
        """
        profile = ProfileService.get_profile(user_id)
        if not profile:
            return False

        known_languages = profile['software_background'].get('languages_known', [])
        return language.lower() in [lang.lower() for lang in known_languages]

    @staticmethod
    def should_include_hardware_examples(user_id: str) -> bool:
        """Check if hardware examples should be included for user.

        Args:
            user_id: User's unique identifier

        Returns:
            True if user has hardware capabilities, False otherwise
        """
        hardware = ProfileService.get_hardware_capabilities(user_id)
        if not hardware:
            return False

        return hardware['can_do_hardware_projects']

    @staticmethod
    def get_personalization_hints(user_id: str) -> Optional[Dict[str, Any]]:
        """Get personalization hints for AI Agents.

        Returns a dictionary of hints that AI Agents can use to
        customize their responses.

        Args:
            user_id: User's unique identifier

        Returns:
            Dict with personalization hints if user found, None otherwise
        """
        context = PersonalizationInterface.get_user_context(user_id)
        if not context:
            return None

        return {
            'use_simple_language': context.skill_tier == SkillTier.BEGINNER,
            'include_code_examples': context.programming_level != 'beginner',
            'preferred_languages': context.languages_known,
            'include_ai_details': context.ai_experience not in ['none', 'basic'],
            'include_hardware_projects': context.can_do_hardware_projects,
            'robotics_context_available': context.has_robotics_background,
            'suggested_complexity': PersonalizationInterface.get_recommended_complexity(user_id)
        }
