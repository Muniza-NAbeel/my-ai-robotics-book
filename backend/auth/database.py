"""SQLite database setup for authentication."""

import sqlite3
import os
from contextlib import contextmanager
from typing import Generator

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), "auth.db")


def get_db_connection() -> sqlite3.Connection:
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Context manager for database connections."""
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_database():
    """Initialize database with required tables."""
    with get_db() as conn:
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                password_hash TEXT NOT NULL,
                password_salt TEXT NOT NULL,
                email_verified INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        # Create sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                token TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Create index on email for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)
        """)

        # Create index on token for faster session lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token)
        """)

        # Create index on user_id for session cleanup
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)
        """)


# Initialize database on module import
init_database()
