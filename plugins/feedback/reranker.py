from typing import Optional
from .store import FeedbackStore


class Reranker:
    """Uses stored feedback to compute prompt quality scores."""

    def __init__(self, store: FeedbackStore):
        self.store = store

    def average_rating(self, prompt: str) -> Optional[float]:
        """Compute average rating for all entries with the exact prompt."""
        entries = self.store.get_all_by_prompt(prompt)
        if not entries:
            return None
        total = sum(e.rating for e in entries)
        return total / len(entries)
