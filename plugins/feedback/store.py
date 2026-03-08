import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from .privacy import PrivacyFilter


class FeedbackEntry(BaseModel):
    """A single feedback entry."""

    id: str
    prompt: str
    response: str
    rating: int  # 1-5
    timestamp: datetime
    metadata: dict = {}


class FeedbackStore:
    """SQLite-backed storage for feedback entries with PII redaction."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Create the feedback table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id TEXT PRIMARY KEY,
                    prompt TEXT,
                    response TEXT,
                    rating INTEGER,
                    timestamp TEXT,
                    metadata TEXT
                )
            """)

    def save(self, entry: FeedbackEntry) -> None:
        """Store a feedback entry after redacting PII."""
        redacted_prompt = PrivacyFilter.redact_pii(entry.prompt)
        redacted_response = PrivacyFilter.redact_pii(entry.response)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO feedback VALUES (?, ?, ?, ?, ?, ?)",
                (
                    entry.id,
                    redacted_prompt,
                    redacted_response,
                    entry.rating,
                    entry.timestamp.isoformat(),
                    json.dumps(entry.metadata),
                ),
            )

    def get(self, feedback_id: str) -> Optional[FeedbackEntry]:
        """Retrieve a feedback entry by ID."""
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT id, prompt, response, rating, timestamp, metadata FROM feedback WHERE id = ?",
                (feedback_id,),
            ).fetchone()
            if row is None:
                return None
            return FeedbackEntry(
                id=row[0],
                prompt=row[1],
                response=row[2],
                rating=row[3],
                timestamp=datetime.fromisoformat(row[4]),
                metadata=json.loads(row[5]),
            )

    def get_all_by_prompt(self, prompt: str) -> list[FeedbackEntry]:
        """Retrieve all feedback entries with the exact prompt."""
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT id, prompt, response, rating, timestamp, metadata FROM feedback WHERE prompt = ?",
                (prompt,),
            ).fetchall()
            entries = []
            for row in rows:
                entries.append(
                    FeedbackEntry(
                        id=row[0],
                        prompt=row[1],
                        response=row[2],
                        rating=row[3],
                        timestamp=datetime.fromisoformat(row[4]),
                        metadata=json.loads(row[5]),
                    )
                )
            return entries
