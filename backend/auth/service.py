"""Authentication service for user management with SQLite storage."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from .database import get_db


class AuthService:
    """Service for handling authentication operations with SQLite database."""

    # Session configuration
    SESSION_DURATION_HOURS = 24

    @classmethod
    def _hash_password(cls, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash password with salt using SHA-256."""
        if salt is None:
            salt = secrets.token_hex(32)

        salted = f"{salt}{password}".encode('utf-8')
        hashed = hashlib.sha256(salted).hexdigest()
        return hashed, salt

    @classmethod
    def _verify_password(cls, password: str, hashed: str, salt: str) -> bool:
        """Verify password against stored hash."""
        check_hash, _ = cls._hash_password(password, salt)
        return secrets.compare_digest(check_hash, hashed)

    @classmethod
    def _generate_user_id(cls) -> str:
        """Generate unique user ID."""
        return secrets.token_hex(16)

    @classmethod
    def _generate_session_token(cls) -> str:
        """Generate secure session token."""
        return secrets.token_urlsafe(32)

    @classmethod
    def _generate_session_id(cls) -> str:
        """Generate unique session ID."""
        return secrets.token_hex(16)

    @classmethod
    def create_user(cls, email: str, password: str, name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create a new user account."""
        with get_db() as conn:
            cursor = conn.cursor()

            # Check for existing user
            cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (email,))
            if cursor.fetchone():
                return None

            # Hash password and create user
            hashed_password, salt = cls._hash_password(password)
            user_id = cls._generate_user_id()
            now = datetime.utcnow().isoformat()

            cursor.execute("""
                INSERT INTO users (id, email, name, password_hash, password_salt, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, email, name or email.split('@')[0], hashed_password, salt, now, now))

            return {
                'id': user_id,
                'email': email,
                'name': name or email.split('@')[0],
                'createdAt': now
            }

    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with email and password."""
        with get_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, email, name, password_hash, password_salt
                FROM users WHERE LOWER(email) = LOWER(?)
            """, (email,))
            row = cursor.fetchone()

            if row and cls._verify_password(password, row['password_hash'], row['password_salt']):
                return {
                    'id': row['id'],
                    'email': row['email'],
                    'name': row['name']
                }

            return None

    @classmethod
    def create_session(cls, user_id: str, ip_address: Optional[str] = None,
                       user_agent: Optional[str] = None) -> str:
        """Create a new session for user."""
        with get_db() as conn:
            cursor = conn.cursor()

            session_id = cls._generate_session_id()
            token = cls._generate_session_token()
            now = datetime.utcnow()
            expires_at = now + timedelta(hours=cls.SESSION_DURATION_HOURS)

            cursor.execute("""
                INSERT INTO sessions (id, token, user_id, expires_at, created_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, token, user_id, expires_at.isoformat(), now.isoformat(), ip_address, user_agent))

            return token

    @classmethod
    def validate_session(cls, token: str) -> Optional[Dict[str, Any]]:
        """Validate session token and return user data if valid."""
        with get_db() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT s.user_id, s.expires_at, u.email, u.name
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.token = ?
            """, (token,))
            row = cursor.fetchone()

            if not row:
                return None

            expires_at = datetime.fromisoformat(row['expires_at'])
            if datetime.utcnow() > expires_at:
                # Session expired, remove it
                cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
                return None

            return {
                'id': row['user_id'],
                'email': row['email'],
                'name': row['name']
            }

    @classmethod
    def invalidate_session(cls, token: str) -> bool:
        """Invalidate a session token."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
            return cursor.rowcount > 0

    @classmethod
    def invalidate_all_user_sessions(cls, user_id: str) -> int:
        """Invalidate all sessions for a user."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
            return cursor.rowcount

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user data by ID."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, email, name, created_at, email_verified
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()

            if row:
                return {
                    'id': row['id'],
                    'email': row['email'],
                    'name': row['name'],
                    'createdAt': row['created_at'],
                    'emailVerified': bool(row['email_verified'])
                }
            return None

    @classmethod
    def email_exists(cls, email: str) -> bool:
        """Check if email is already registered."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE LOWER(email) = LOWER(?)", (email,))
            return cursor.fetchone() is not None

    @classmethod
    def cleanup_expired_sessions(cls) -> int:
        """Remove all expired sessions."""
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE expires_at < ?", (datetime.utcnow().isoformat(),))
            return cursor.rowcount
