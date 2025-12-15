"""Onboarding session management for chatbot-driven signup.

Manages temporary state during the signup conversation flow.
Sessions store credentials and collected answers until signup completion.
"""

import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from config.onboarding_questions import (
    ONBOARDING_QUESTIONS,
    get_question_by_id,
    get_next_question_id,
    format_summary
)


class OnboardingSession:
    """Represents an active onboarding conversation session."""

    def __init__(self, session_id: str, email: str, password: str):
        self.session_id = session_id
        self.email = email
        self.password = password  # Stored temporarily until signup completes
        self.current_question_id = "welcome"
        self.collected_answers: Dict[str, Any] = {
            "software_background": {},
            "hardware_background": {},
            "learning_goals": {}
        }
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(minutes=30)

    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for API responses."""
        return {
            "session_id": self.session_id,
            "email": self.email,
            "current_question_id": self.current_question_id,
            "collected_answers": self.collected_answers,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat()
        }


class OnboardingService:
    """Service for managing onboarding sessions."""

    # In-memory session storage (replace with Redis in production)
    _sessions: Dict[str, OnboardingSession] = {}

    @classmethod
    def _generate_session_id(cls) -> str:
        """Generate unique session ID."""
        return secrets.token_urlsafe(24)

    @classmethod
    def create_session(cls, email: str, password: str) -> OnboardingSession:
        """Create a new onboarding session after credential validation.

        Args:
            email: User's email address
            password: User's password (stored temporarily)

        Returns:
            New OnboardingSession instance
        """
        session_id = cls._generate_session_id()
        session = OnboardingSession(session_id, email, password)
        cls._sessions[session_id] = session
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[OnboardingSession]:
        """Get an onboarding session by ID.

        Returns None if session doesn't exist or has expired.
        """
        session = cls._sessions.get(session_id)
        if session and session.is_expired():
            cls.delete_session(session_id)
            return None
        return session

    @classmethod
    def delete_session(cls, session_id: str) -> bool:
        """Delete an onboarding session."""
        if session_id in cls._sessions:
            del cls._sessions[session_id]
            return True
        return False

    @classmethod
    def get_current_question(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current question for a session.

        Returns the question definition including options.
        """
        session = cls.get_session(session_id)
        if not session:
            return None

        question = get_question_by_id(session.current_question_id)
        if not question:
            return None

        # For summary, include collected answers
        if question["type"] == "confirmation":
            return {
                **question,
                "summary": format_summary(session.collected_answers),
                "collected_answers": session.collected_answers
            }

        return question

    @classmethod
    def submit_answer(
        cls, session_id: str, answer: Any
    ) -> Optional[Dict[str, Any]]:
        """Submit an answer for the current question and advance.

        Args:
            session_id: The session ID
            answer: The user's answer (string for single_select, list for multi_select)

        Returns:
            Dict with next question or completion status, None if session invalid
        """
        session = cls.get_session(session_id)
        if not session:
            return None

        current_question = get_question_by_id(session.current_question_id)
        if not current_question:
            return None

        # Handle greeting - just advance to next
        if current_question["type"] == "greeting":
            session.current_question_id = current_question["next"]
            return {
                "status": "continue",
                "next_question": cls.get_current_question(session_id)
            }

        # Store the answer
        if "field" in current_question:
            field_path = current_question["field"]
            cls._store_answer(session, field_path, answer, current_question)

        # Advance to next question
        next_id = current_question.get("next")
        if next_id:
            session.current_question_id = next_id
            return {
                "status": "continue",
                "next_question": cls.get_current_question(session_id)
            }

        # No next question - onboarding complete
        return {
            "status": "complete",
            "collected_answers": session.collected_answers
        }

    @classmethod
    def _store_answer(
        cls,
        session: OnboardingSession,
        field_path: str,
        answer: Any,
        question: Dict[str, Any]
    ):
        """Store answer in the session's collected_answers.

        Handles nested paths like 'software_background.programming_level'.
        """
        parts = field_path.split(".")
        target = session.collected_answers

        # Navigate to parent
        for part in parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]

        # Apply value transformation if specified
        final_value = answer
        if question.get("value_transform") == "boolean":
            final_value = answer == "true" or answer is True

        # Store the value
        target[parts[-1]] = final_value

    @classmethod
    def get_summary(cls, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of all collected answers.

        Returns formatted summary for user confirmation.
        """
        session = cls.get_session(session_id)
        if not session:
            return None

        return {
            "email": session.email,
            "summary_text": format_summary(session.collected_answers),
            "collected_answers": session.collected_answers
        }

    @classmethod
    def get_credentials_and_profile(
        cls, session_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get credentials and profile data for final signup.

        This is called when user confirms the summary to create the account.
        """
        session = cls.get_session(session_id)
        if not session:
            return None

        return {
            "email": session.email,
            "password": session.password,
            "software_background": session.collected_answers.get("software_background", {}),
            "hardware_background": session.collected_answers.get("hardware_background", {}),
            "learning_goals": session.collected_answers.get("learning_goals", {})
        }

    @classmethod
    def cleanup_expired(cls) -> int:
        """Remove all expired sessions. Returns count of removed sessions."""
        expired = [
            sid for sid, session in cls._sessions.items()
            if session.is_expired()
        ]
        for sid in expired:
            del cls._sessions[sid]
        return len(expired)
