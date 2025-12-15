"""Exercises Agent for generating practice questions."""

import json
import re
from typing import Dict
from agents import Runner
from .base_agent import BaseSkillAgent


class ExercisesAgent(BaseSkillAgent):
    """Agent that generates difficulty-graded MCQ questions."""

    name = "exercises_agent"
    description = "Generates multiple choice quiz questions for AI and robotics topics"
    instructions = """You generate multiple choice quiz questions for AI/robotics students.

OUTPUT FORMAT - Return ONLY valid JSON, no other text:
{
  "topic": "the topic name",
  "questions": {
    "easy": {
      "question": "A simple recall question about the topic?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 0
    },
    "medium": {
      "question": "An application-based question?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 2
    },
    "advanced": {
      "question": "A complex analysis question?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctIndex": 1
    }
  }
}

RULES:
- Return ONLY the JSON object, nothing else
- Each question MUST have exactly 4 options
- correctIndex is 0-based (0=first option, 1=second, etc.)
- Options should be plausible but only one is correct
- Questions should test understanding of the topic
- Randomize correctIndex position (don't always make it 0)
"""

    def run(self, query: str) -> Dict[str, str]:
        """Execute quiz generation and return structured response."""
        query = self.validate_input(query, "query")
        result = Runner.run_sync(self.agent, input=query)

        # Try to parse JSON from response
        try:
            response_text = result.final_output.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)

            quiz_data = json.loads(response_text)
            return {
                "response": json.dumps(quiz_data),
                "type": "quiz"
            }
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "response": result.final_output,
                "type": "text"
            }
        except Exception as e:
            return {
                "response": f"Error generating quiz: {str(e)}",
                "type": "text"
            }
