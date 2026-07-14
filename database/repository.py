"""SQLite persistence functions for the Cloud Resume API."""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent / "database.db"


def get_connection() -> sqlite3.Connection:
    """Create a connection to the local SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    """Create the profile table and add its initial record if needed."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                career_goal TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            INSERT OR IGNORE INTO profile (id, name, course, career_goal)
            VALUES (1, 'Kian Wilson', 'Computing', 'Cloud Engineer')
            """
        )


def get_profile() -> dict[str, str]:
    """Return the single stored professional profile."""
    with get_connection() as connection:
        profile = connection.execute(
            "SELECT name, course, career_goal FROM profile WHERE id = 1"
        ).fetchone()

    if profile is None:
        raise RuntimeError("The profile has not been initialized.")

    return dict(profile)
