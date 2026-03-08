import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from plugins.feedback.store import FeedbackStore, FeedbackEntry
from plugins.feedback.reranker import Reranker


def test_average_rating_for_prompt():
    """Should compute average rating for a given prompt."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "feedback.db"
        store = FeedbackStore(db_path)
        now = datetime.now()
        # Store two feedback entries with same prompt, different ratings
        store.save(
            FeedbackEntry(
                id="1",
                prompt="What is AI?",
                response="AI is...",
                rating=5,
                timestamp=now - timedelta(days=1),
                metadata={},
            )
        )
        store.save(
            FeedbackEntry(
                id="2",
                prompt="What is AI?",
                response="Artificial Intelligence...",
                rating=3,
                timestamp=now,
                metadata={},
            )
        )
        reranker = Reranker(store)
        avg = reranker.average_rating("What is AI?")
        assert avg == 4.0  # (5+3)/2


def test_average_rating_no_feedback():
    """Should return None if no feedback for prompt."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "feedback.db"
        store = FeedbackStore(db_path)
        reranker = Reranker(store)
        avg = reranker.average_rating("unknown prompt")
        assert avg is None
