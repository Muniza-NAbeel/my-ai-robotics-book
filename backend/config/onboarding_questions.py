"""Onboarding chatbot question configuration.

Defines the conversational flow for collecting user background data
during signup. Each question maps to a field in the user profile.
"""

from typing import Dict, List, Any, Optional

# Question types:
# - greeting: Welcome message, no input expected
# - single_select: User picks one option
# - multi_select: User picks multiple options
# - confirmation: Summary with confirm/edit choice

ONBOARDING_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "welcome",
        "type": "greeting",
        "bot_message": "Welcome! I'm excited to help you learn AI and Robotics. Let me ask a few questions to personalize your experience.",
        "next": "programming_level"
    },
    {
        "id": "programming_level",
        "type": "single_select",
        "bot_message": "First, how would you describe your programming experience?",
        "options": [
            {"value": "beginner", "label": "Beginner", "description": "New to coding or just started learning"},
            {"value": "intermediate", "label": "Intermediate", "description": "Can build basic projects independently"},
            {"value": "advanced", "label": "Advanced", "description": "Comfortable with complex systems and architectures"}
        ],
        "field": "software_background.programming_level",
        "next": "languages_known"
    },
    {
        "id": "languages_known",
        "type": "multi_select",
        "bot_message": "Which programming languages are you familiar with? (Select all that apply)",
        "options": [
            {"value": "python", "label": "Python"},
            {"value": "javascript", "label": "JavaScript"},
            {"value": "typescript", "label": "TypeScript"},
            {"value": "c_cpp", "label": "C/C++"},
            {"value": "java", "label": "Java"},
            {"value": "none", "label": "None yet"}
        ],
        "field": "software_background.languages_known",
        "next": "ai_experience"
    },
    {
        "id": "ai_experience",
        "type": "single_select",
        "bot_message": "How much experience do you have with AI/Machine Learning?",
        "options": [
            {"value": "none", "label": "No experience", "description": "Haven't worked with AI yet"},
            {"value": "basic", "label": "Basic", "description": "Used some AI tools or completed tutorials"},
            {"value": "intermediate", "label": "Intermediate", "description": "Built ML models or used AI APIs"},
            {"value": "advanced", "label": "Advanced", "description": "Professional experience with AI systems"}
        ],
        "field": "software_background.ai_experience",
        "next": "web_dev_experience"
    },
    {
        "id": "web_dev_experience",
        "type": "single_select",
        "bot_message": "What about web development experience?",
        "options": [
            {"value": "none", "label": "No experience"},
            {"value": "basic", "label": "Basic", "description": "HTML/CSS basics"},
            {"value": "intermediate", "label": "Intermediate", "description": "Can build frontend apps"},
            {"value": "advanced", "label": "Advanced", "description": "Full-stack development"}
        ],
        "field": "software_background.web_dev_experience",
        "next": "robotics_experience"
    },
    {
        "id": "robotics_experience",
        "type": "single_select",
        "bot_message": "Great! Now let's talk about hardware. Have you worked with robotics before?",
        "options": [
            {"value": "true", "label": "Yes", "description": "I have hands-on robotics experience"},
            {"value": "false", "label": "No", "description": "No robotics experience yet"}
        ],
        "field": "hardware_background.robotics_experience",
        "value_transform": "boolean",  # Convert string to boolean
        "next": "electronics_familiarity"
    },
    {
        "id": "electronics_familiarity",
        "type": "single_select",
        "bot_message": "How familiar are you with electronics and circuits?",
        "options": [
            {"value": "none", "label": "Not familiar", "description": "Never worked with electronics"},
            {"value": "basic", "label": "Basic", "description": "Know some basics, maybe LEDs and sensors"},
            {"value": "intermediate", "label": "Intermediate", "description": "Can design and build circuits"}
        ],
        "field": "hardware_background.electronics_familiarity",
        "next": "hardware_access"
    },
    {
        "id": "hardware_access",
        "type": "multi_select",
        "bot_message": "What hardware do you have access to? (Select all that apply)",
        "options": [
            {"value": "laptop_only", "label": "Laptop only"},
            {"value": "raspberry_pi", "label": "Raspberry Pi"},
            {"value": "arduino", "label": "Arduino"},
            {"value": "robotics_kits", "label": "Robotics kits"},
            {"value": "none", "label": "No hardware access"}
        ],
        "field": "hardware_background.hardware_access",
        "next": "learning_goals"
    },
    {
        "id": "learning_goals",
        "type": "single_select",
        "bot_message": "Last question! What's your primary learning goal?",
        "options": [
            {"value": "career", "label": "Career in AI/Robotics", "description": "Looking for job opportunities"},
            {"value": "hobby", "label": "Personal projects/Hobby", "description": "Building things for fun"},
            {"value": "academic", "label": "Academic research", "description": "Research or coursework"},
            {"value": "explore", "label": "Just exploring", "description": "Curious about the field"}
        ],
        "field": "learning_goals.primary_interest",
        "next": "summary"
    },
    {
        "id": "summary",
        "type": "confirmation",
        "bot_message": "Here's what I learned about you:",
        "next": None  # End of flow
    }
]


def get_question_by_id(question_id: str) -> Optional[Dict[str, Any]]:
    """Get a question by its ID."""
    for q in ONBOARDING_QUESTIONS:
        if q["id"] == question_id:
            return q
    return None


def get_next_question_id(current_id: str) -> Optional[str]:
    """Get the next question ID after the current one."""
    question = get_question_by_id(current_id)
    if question:
        return question.get("next")
    return None


def get_all_field_names() -> List[str]:
    """Get all field names that will be collected."""
    fields = []
    for q in ONBOARDING_QUESTIONS:
        if "field" in q:
            fields.append(q["field"])
    return fields


def format_summary(answers: Dict[str, Any]) -> str:
    """Format collected answers as a readable summary."""
    lines = []

    # Software background
    sw = answers.get("software_background", {})
    lines.append(f"Programming: {sw.get('programming_level', 'Not specified')}")

    languages = sw.get("languages_known", [])
    if languages:
        lines.append(f"Languages: {', '.join(languages)}")

    lines.append(f"AI Experience: {sw.get('ai_experience', 'Not specified')}")
    lines.append(f"Web Dev: {sw.get('web_dev_experience', 'Not specified')}")

    # Hardware background
    hw = answers.get("hardware_background", {})
    robotics = "Yes" if hw.get("robotics_experience") else "No"
    lines.append(f"Robotics Experience: {robotics}")
    lines.append(f"Electronics: {hw.get('electronics_familiarity', 'Not specified')}")

    hardware = hw.get("hardware_access", [])
    if hardware:
        lines.append(f"Hardware: {', '.join(hardware)}")

    # Learning goals
    goals = answers.get("learning_goals", {})
    lines.append(f"Goal: {goals.get('primary_interest', 'Not specified')}")

    return "\n".join(lines)
