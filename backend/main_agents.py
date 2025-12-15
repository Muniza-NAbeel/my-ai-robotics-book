"""Main Agent - Unified skills interface for all sub-agents."""

from dataclasses import dataclass
from typing import Optional

from skill_agents import (
    GlossaryAgent,
    DiagramAgent,
    TranslationAgent,
    ExercisesAgent,
    BaseSkillAgent,
)


@dataclass
class Skills:
    """Unified access to all sub-agents.

    Provides type-safe access to all skill agents via dot notation.
    """
    glossary: GlossaryAgent
    diagrams: DiagramAgent
    translate: TranslationAgent
    exercises: ExercisesAgent


class MainAgent:
    """Main orchestrator that exposes all skills through a unified interface.

    Example usage:
        from main_agent import main_agent

        # Access via unified skills object
        result1 = main_agent.skills.glossary.run(term="Robot")
        result2 = main_agent.skills.diagrams.run(topic="Robot Architecture")
        result3 = main_agent.skills.translate.run(text="Hello world")
        result4 = main_agent.skills.exercises.run(chapter="Introduction to Sensors")

        # Each returns {"result": "...output string..."}
        print(result1["result"])
    """

    def __init__(self):
        """Initialize the main agent with all sub-agents."""
        self.skills = Skills(
            glossary=GlossaryAgent(),
            diagrams=DiagramAgent(),
            translate=TranslationAgent(),
            exercises=ExercisesAgent(),
        )

    def get_skill(self, name: str) -> Optional[BaseSkillAgent]:
        """Get a skill agent by name.

        Args:
            name: Name of the skill ('glossary', 'diagrams', 'translate', 'exercises')

        Returns:
            The corresponding skill agent, or None if not found
        """
        skill_map = {
            "glossary": self.skills.glossary,
            "diagrams": self.skills.diagrams,
            "diagram": self.skills.diagrams,  # Alias
            "translate": self.skills.translate,
            "translation": self.skills.translate,  # Alias
            "exercises": self.skills.exercises,
            "exercise": self.skills.exercises,  # Alias
        }
        return skill_map.get(name.lower())

    def list_skills(self) -> list:
        """List all available skills.

        Returns:
            List of skill names and descriptions
        """
        return [
            {"name": "glossary", "description": self.skills.glossary.description},
            {"name": "diagrams", "description": self.skills.diagrams.description},
            {"name": "translate", "description": self.skills.translate.description},
            {"name": "exercises", "description": self.skills.exercises.description},
        ]


# Singleton instance for easy import
main_agent = MainAgent()
