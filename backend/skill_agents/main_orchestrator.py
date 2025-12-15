"""Main Orchestrator Agent that routes requests to sub-agents.

Supports user profile personalization for authenticated users.
When a user profile is provided, responses are tailored to their
skill level and background.
"""

import os
from typing import Dict, Optional, Any

from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from .glossary_agent import GlossaryAgent
from .diagram_agent import DiagramAgent
from .translation_agent import TranslationAgent
from .exercises_agent import ExercisesAgent


class MainOrchestratorAgent:
    """Routes requests to appropriate sub-agents based on skill parameter.

    Supports personalization via user_profile parameter.
    """

    def __init__(self):
        """Initialize orchestrator with all sub-agents."""
        self.agents = {
            "glossary": GlossaryAgent(),
            "diagram": DiagramAgent(),
            "translate": TranslationAgent(),
            "exercises": ExercisesAgent(),
        }
        self.provider = AsyncOpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url=os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
        )
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.provider
        )

    def _get_personalized_instructions(self, user_profile: Optional[Dict[str, Any]]) -> str:
        """Generate personalized instructions based on user profile.

        Args:
            user_profile: User's background data or None for guests

        Returns:
            Personalized system instructions string
        """
        base_instructions = """You are a helpful assistant for an AI and robotics textbook.
Answer questions about AI, robotics, and related topics in a clear, educational manner."""

        if not user_profile:
            return base_instructions + """
Since this is a guest user, provide general explanations suitable for beginners.
Mention that signing up enables personalized learning."""

        # Extract profile data
        software = user_profile.get("software_background", {})
        hardware = user_profile.get("hardware_background", {})

        prog_level = software.get("programming_level", "beginner")
        ai_exp = software.get("ai_experience", "none")
        languages = software.get("languages_known", [])
        robotics_exp = hardware.get("robotics_experience", False)
        hw_access = hardware.get("hardware_access", [])

        # Build personalized context
        personalization = f"""

USER PROFILE (use this to personalize your response):
- Programming Level: {prog_level}
- AI/ML Experience: {ai_exp}
- Known Languages: {', '.join(languages) if languages else 'None specified'}
- Robotics Experience: {'Yes' if robotics_exp else 'No'}
- Available Hardware: {', '.join(hw_access) if hw_access else 'Laptop only'}

PERSONALIZATION GUIDELINES:
"""

        # Add level-specific guidelines
        if prog_level == "beginner":
            personalization += """- Use simple explanations and avoid jargon
- Break down complex concepts into smaller steps
- Provide analogies to everyday experiences
- Include code examples only if they're very simple"""
        elif prog_level == "intermediate":
            personalization += """- Assume basic programming knowledge
- You can use technical terms but briefly explain new ones
- Include practical code examples when relevant
- Mention best practices and common patterns"""
        else:  # advanced
            personalization += """- Assume strong programming background
- Use technical terminology freely
- Focus on implementation details and edge cases
- Discuss trade-offs and advanced patterns
- Skip basic explanations unless asked"""

        # Add AI-specific guidance
        if ai_exp == "none" or ai_exp == "basic":
            personalization += """
- When discussing AI/ML, explain concepts from scratch
- Use intuitive examples before mathematical notation"""
        elif ai_exp == "intermediate" or ai_exp == "advanced":
            personalization += """
- Can assume familiarity with ML fundamentals
- Reference specific algorithms and techniques"""

        # Add language-specific hints
        if "python" in [l.lower() for l in languages]:
            personalization += """
- Prefer Python examples when showing code"""
        elif "javascript" in [l.lower() for l in languages] or "typescript" in [l.lower() for l in languages]:
            personalization += """
- Can use JavaScript/TypeScript for web-related examples"""

        # Add hardware context
        if robotics_exp or "raspberry_pi" in hw_access or "arduino" in hw_access:
            personalization += """
- Can include hands-on hardware project suggestions"""
        else:
            personalization += """
- Focus on simulation and software approaches
- Avoid assuming access to physical hardware"""

        return base_instructions + personalization

    def _create_personalized_agent(self, user_profile: Optional[Dict[str, Any]]) -> Agent:
        """Create an agent with personalized instructions.

        Args:
            user_profile: User's background data or None for guests

        Returns:
            Agent configured for the user's level
        """
        return Agent(
            name="personalized_assistant",
            instructions=self._get_personalized_instructions(user_profile),
            model=self.model
        )

    def route(
        self,
        query: str,
        skill: Optional[str] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """Route query to appropriate agent based on skill.

        Args:
            query: The user's input query
            skill: Optional skill identifier (glossary, diagram, translate, exercises)
            user_profile: Optional user profile for personalization

        Returns:
            Dict with 'response' key containing the generated output.
        """
        if not query or not query.strip():
            return {"response": "Please provide a question or topic."}

        # Route to specific skill agent if skill is provided
        if skill and skill in self.agents:
            return self.agents[skill].run(query)

        # Use personalized agent for general queries
        agent = self._create_personalized_agent(user_profile)
        result = Runner.run_sync(agent, input=query)
        return {"response": result.final_output}

    def get_personalized_greeting(self, user_profile: Optional[Dict[str, Any]]) -> str:
        """Generate a personalized greeting based on user profile.

        Args:
            user_profile: User's background data or None for guests

        Returns:
            Personalized greeting string
        """
        if not user_profile:
            return "Welcome! I'm here to help you learn about AI and Robotics. Sign up for a personalized experience!"

        software = user_profile.get("software_background", {})
        prog_level = software.get("programming_level", "beginner")
        ai_exp = software.get("ai_experience", "none")

        if prog_level == "advanced" and ai_exp in ["intermediate", "advanced"]:
            return "Welcome back! Ready to dive into advanced AI and robotics topics?"
        elif prog_level == "intermediate":
            return "Welcome back! Let's continue building your AI and robotics skills!"
        else:
            return "Welcome back! I'm excited to help you explore AI and robotics. What would you like to learn today?"
