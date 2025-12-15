"""Glossary Agent for generating term definitions."""

from .base_agent import BaseSkillAgent


class GlossaryAgent(BaseSkillAgent):
    """Agent that provides simple, clear definitions for technical terms."""

    name = "glossary_agent"
    description = "Provides glossary definitions for AI and robotics terms"
    instructions = """You are a glossary expert for an AI and robotics textbook.

When given a term or topic:
1. Provide a simple, clear definition in 2-3 sentences
2. Use plain language suitable for students
3. Include a brief example if helpful
4. Avoid jargon unless defining that jargon

Format: Start with the term, then a colon, then the definition.
Example: "Robot: A machine capable of carrying out complex actions automatically, especially one programmable by a computer. For example, a robotic arm in a factory that assembles car parts."
"""
