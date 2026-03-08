import tempfile
from pathlib import Path
from plugins.feedback.store import FeedbackStore, FeedbackEntry
from datetime import datetime


def test_store_and_retrieve_feedback():
    """Should store a feedback entry and retrieve it by ID."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FeedbackStore(db_path=Path(tmpdir) / "feedback.db")
        entry = FeedbackEntry(
            id="123",
            prompt="What is AI?",
            response="Artificial Intelligence...",
            rating=5,
            timestamp=datetime.now(),
            metadata={"user_id": "test"},
        )
        store.save(entry)
        retrieved = store.get("123")
        assert retrieved is not None
        assert retrieved.id == "123"
        assert retrieved.rating == 5


def test_store_with_complex_metadata():
    """Should handle nested dictionaries and lists in metadata."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FeedbackStore(db_path=Path(tmpdir) / "feedback.db")
        entry = FeedbackEntry(
            id="456",
            prompt="Test complex metadata",
            response="Response",
            rating=3,
            timestamp=datetime.now(),
            metadata={"nested": {"key": "value"}, "list": [1, 2, 3]},
        )
        store.save(entry)
        retrieved = store.get("456")
        assert retrieved.metadata["nested"]["key"] == "value"
        assert retrieved.metadata["list"][0] == 1


def test_get_nonexistent_returns_none():
    """Should return None when feedback ID does not exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FeedbackStore(db_path=Path(tmpdir) / "feedback.db")
        assert store.get("nonexistent") is None


def test_update_existing_feedback():
    """Should update an existing entry (INSERT OR REPLACE)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FeedbackStore(db_path=Path(tmpdir) / "feedback.db")
        entry1 = FeedbackEntry(
            id="789",
            prompt="Original",
            response="Original response",
            rating=2,
            timestamp=datetime.now(),
            metadata={},
        )
        store.save(entry1)
        entry2 = FeedbackEntry(
            id="789",
            prompt="Updated",
            response="Updated response",
            rating=4,
            timestamp=datetime.now(),
            metadata={"updated": True},
        )
        store.save(entry2)
        retrieved = store.get("789")
        assert retrieved.prompt == "Updated"
        assert retrieved.rating == 4
        assert retrieved.metadata["updated"] is True


def test_pii_redacted_on_save():
    """Should redact PII from prompt and response before storing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FeedbackStore(db_path=Path(tmpdir) / "feedback.db")
        entry = FeedbackEntry(
            id="pii_test",
            prompt="My email is john@doe.com and phone 555-123-4567",
            response="Contact me at jane@doe.com or 987-65-4321",
            rating=5,
            timestamp=datetime.now(),
            metadata={},
        )
        store.save(entry)
        retrieved = store.get("pii_test")
        assert "[REDACTED]" in retrieved.prompt
        assert "[REDACTED]" in retrieved.response
        assert "john@doe.com" not in retrieved.prompt
        assert "555-123-4567" not in retrieved.prompt
        assert "jane@doe.com" not in retrieved.response
        assert "987-65-4321" not in retrieved.response


def test_get_all_by_prompt():
    """Should retrieve all feedback entries for a given prompt."""
    with tempfile.TemporaryDirectory() as tmpdir:
        store = FeedbackStore(db_path=Path(tmpdir) / "feedback.db")
        now = datetime.now()
        store.save(
            FeedbackEntry(
                id="1",
                prompt="test prompt",
                response="response1",
                rating=5,
                timestamp=now,
                metadata={},
            )
        )
        store.save(
            FeedbackEntry(
                id="2",
                prompt="test prompt",
                response="response2",
                rating=3,
                timestamp=now,
                metadata={},
            )
        )
        store.save(
            FeedbackEntry(
                id="3",
                prompt="other prompt",
                response="response3",
                rating=4,
                timestamp=now,
                metadata={},
            )
        )
        results = store.get_all_by_prompt("test prompt")
        assert len(results) == 2
        assert {r.id for r in results} == {"1", "2"}
